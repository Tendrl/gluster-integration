from tendrl.commons.utils import log_utils as logger
from tendrl.gluster_integration.sds_sync.vol_utilization import \
    showVolumeUtilization


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
        util_det = showVolumeUtilization(
            volume.name
        )
        if util_det:
            volume.usable_capacity = int(util_det['total'])
            volume.used_capacity = int(util_det['used'])
            volume.pcnt_used = str(util_det['pcnt_used'])
            volume.total_inode_capacity = int(util_det['total_inode'])
            volume.used_inode_capacity = int(util_det['used_inode'])
            volume.pcnt_inode_used = str(util_det['pcnt_inode_used'])
            volume.save()
            cluster_used_capacity += volume.used_capacity
            cluster_usable_capacity += volume.usable_capacity
        else:
            logger.log(
                "error",
                NS.publisher_id,
                {
                    "message": "Error getting utilization of "
                    "volume: %s" % (volume.name)
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
