import json
import os
import subprocess

from tendrl.commons.utils import log_utils as logger


def sync_utilization_details(volumes):
    cluster_used_capacity = 0
    cluster_usable_capacity = 0
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
        cmd = subprocess.Popen(
            "vol_utilization %s" % volume.name,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=open(os.devnull, "r"),
            close_fds=True
        )
        out, err = cmd.communicate()
        if err == '':
            util_det = json.loads(out)
            volume.usable_capacity = int(util_det['total'])
            volume.used_capacity = int(util_det['used'])
            volume.pcnt_used = str(util_det['pcnt_used'])
            volume.save()
            cluster_used_capacity += volume.used_capacity
            cluster_usable_capacity += volume.usable_capacity
        else:
            logger.log(
                "error",
                NS.publisher_id,
                {
                    "message": "Error getting utilization of "
                    "volume: %s. Error: %s" % (volume.name, err)
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
