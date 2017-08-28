import gevent

from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons.utils import cmd_utils
import xml.etree.cElementTree as etree


def sync_volume_rebalance_estimated_time(volumes):
    for volume in volumes:
        rebal_estimated_time = 0
        vol_rebal_details = NS.gluster.objects.RebalanceDetails(
            vol_id=volume.vol_id
        ).load_all()
        for entry in vol_rebal_details:
            if entry.time_left and \
                int(entry.time_left) > rebal_estimated_time:
                rebal_estimated_time = int(entry.time_left)
        volume.rebal_estimated_time = rebal_estimated_time
        volume.save()


def sync_volume_rebalance_status(volumes):
    for volume in volumes:
        rebal_status_list = []
        if "Distribute" in volume.vol_type:
            vol_rebal_details = NS.gluster.objects.RebalanceDetails(
                vol_id=volume.vol_id
            ).load_all()
            for entry in vol_rebal_details:
                rebal_status_list.append(entry.rebal_status)
            if "in_progress" in rebal_status_list:
                volume.rebal_status = "in_progress"
            elif all(item == "completed" for item in rebal_status_list):
                volume.rebal_status = "completed"
            elif all(item == "not_started" for item in rebal_status_list):
                volume.rebal_status = "not_started"
            volume.save()
