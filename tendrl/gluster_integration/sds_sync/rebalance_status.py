from tendrl.gluster_integration.sds_sync import event_utils


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
                new_rebal_status = "in_progress"
            elif all(item == "completed" for item in rebal_status_list):
                new_rebal_status = "completed"
            elif all(item == "not_started" for item in rebal_status_list):
                new_rebal_status = "not_started"

            if volume.rebal_status != "" and \
                new_rebal_status != volume.rebal_status:
                msg = ("Rebalance status of volume: %s "
                       "changed from %s to %s") % (
                           volume.name,
                           volume.rebal_status,
                           new_rebal_status)
                instance = "volume_%s" % volume.name
                event_utils.emit_event(
                    "rebalance_status",
                    new_rebal_status,
                    msg,
                    instance,
                    'INFO'
                )

            volume.rebal_status = new_rebal_status
            volume.save()
