import json
import os
import subprocess

from tendrl.commons.utils import log_utils as logger


def sync_utilization_details(volumes):
    cluster_used_capacity = 0
    cluster_usable_capacity = 0
    volnames = ''
    voldict = {}
    for volume in volumes:
        if volume.status != "Started":
            logger.log(
                "error",
                NS.publisher_id,
                {
                    "message": "Volume: %s is stopped."
                               "Cannot get utilization data" % volume.name
                }
            )
            continue
        volnames += volume.name + ','
        voldict[volume.name] = volume

    # IMPORTANT: This calculation of volume utilization is being done
    # through a subprocess call intentionally and should not not be
    # changed to in process call. This is done due to memory leak issues
    # with gfapi (which is used underneath this tool). Keep this logic
    # as is
    cmd = subprocess.Popen(
        "tendrl-gluster-vol-utilization %s" % volnames,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=open(os.devnull, "r"),
        close_fds=True
    )
    out = ''
    try:
        out, err = cmd.communicate()
        if err == '':
            util_det = json.loads(out)
            for k, v in util_det.iteritems():
                volume = voldict[k]
                volume.usable_capacity = int(v['total'])
                volume.used_capacity = int(v['used'])
                volume.pcnt_used = str(v['pcnt_used'])
                volume.total_inode_capacity = int(v['total_inode'])
                volume.used_inode_capacity = int(v['used_inode'])
                volume.pcnt_inode_used = str(v['pcnt_inode_used'])
                volume.save()
                cluster_used_capacity += volume.used_capacity
                cluster_usable_capacity += volume.usable_capacity
        else:
            logger.log(
                "error",
                NS.publisher_id,
                {
                    "message": "Error getting utilization of "
                    "volumes %s" % volnames
                }
            )
    except(KeyError, TypeError, ValueError):
        logger.log(
            "error",
            NS.publisher_id,
            {
                "message": "Error getting utilization of "
                "volumes %s . err: %s" % (volnames, out)
            }
        )
    cluster_pcnt_used = 0
    if cluster_usable_capacity > 0:
        cluster_pcnt_used = (
            cluster_used_capacity / float(cluster_usable_capacity)
        ) * 100

    NS.gluster.objects.Utilization(
        used_capacity=int(cluster_used_capacity),
        usable_capacity=int(cluster_usable_capacity),
        pcnt_used=str(cluster_pcnt_used)
    ).save()
