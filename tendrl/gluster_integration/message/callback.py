# The callback function names below should match(in small case)
# the event_type field of gluster native events as documented
# at: https://gluster.readthedocs.io/en/latest/Administrator%20Guide/
# Events%20APIs/ .
# Whenever gluster-integration receives a gluster native event,
# event handler checks if there is a callback function defined for
# that event in this file, If it finds then that callback function
# will be invoked

from tendrl.commons.utils import log_utils as logger
from tendrl.commons.utils import monitoring_utils

RESOURCE_TYPE_BRICK = "brick"
RESOURCE_TYPE_PEER = "host"
RESOURCE_TYPE_VOLUME = "volume"


class Callback(object):
    def quorum_lost(self, event):
        context = "quorum|" + event['message']['name']
        message = "Quorum of volume: {0} is lost".format(
            event['message']['name']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="quorum_lost"
        )
        native_event.save()

    def quorum_regained(self, event):
        context = "quorum|" + event['message']['name']
        message = "Quorum of volume: {0} is regained".format(
            event['message']['name']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="recovery",
            current_value="quorum_gained"
        )
        native_event.save()

    def svc_connected(self, event):
        context = "svc_connecion|" + event['message']['svc_name']
        volname = event['message'].get('volume', '')
        if volname:
            context += volname

        message = "Service: {0} is connected".format(
            event['message']['svc_name']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="recovery",
            current_value="service_connected"
        )
        native_event.save()

    def svc_disconnected(self, event):
        context = "svc_connection|" + event['message']['svc_name']
        volname = event['message'].get('volume', '')
        if volname:
            context += volname

        message = "Service: {0} is disconnected".format(
            event['message']['svc_name']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="service_disconnected"
        )
        native_event.save()

    def ec_min_bricks_not_up(self, event):
        context = "ec_min_bricks_up|" + event['message']['subvol']
        message = "Minimum number of bricks not up in EC subvolume" \
                  ": {0}".format(
                      event['message']['subvol']
                  )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="ec_min_bricks_not_up"
        )
        native_event.save()

    def ec_min_bricks_up(self, event):
        context = "ec_min_bricks_up|" + event['message']['subvol']
        message = "Minimum number of bricks back online " \
                  "in EC subvolume: {0}".format(
                      event['message']['subvol']
                  )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="recovery",
            current_value="ec_min_bricks_up"
        )
        native_event.save()

    def afr_quorum_met(self, event):
        context = "afr_quorum_state|" + event['message']['subvol']
        message = "Afr quorum is met for subvolume: {0}".format(
            event['message']['subvol']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="recovery",
            current_value="afr_quorum_met"
        )
        native_event.save()

    def afr_quorum_fail(self, event):
        context = "afr_quorum_state|" + event['message']['subvol']
        message = "Afr quorum has failed for subvolume: {0}".format(
            event['message']['subvol']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="afr_quorum_failed"
        )
        native_event.save()

    def afr_subvol_up(self, event):
        context = "afr_subvol_state|" + event['message']['subvol']
        message = "Afr subvolume: {0} is back up".format(
            event['message']['subvol']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="recovery",
            current_value="afr_subvol_up"
        )
        native_event.save()

    def afr_subvols_down(self, event):
        context = "afr_subvol_state|" + event['message']['subvol']
        message = "Afr subvolume: {0} is down".format(
            event['message']['subvol']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="afr_subvol_down"
        )
        native_event.save()

    def unknown_peer(self, event):
        context = "unknown_peer|" + event['message']['peer']
        message = "Peer {0} has moved to unknown state".format(
            event['message']['peer']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="unknown_peer",
            alert_notify=True
        )
        native_event.save()

    def brickpath_resolve_failed(self, event):
        context = "brickpath_resolve_failed|" + event['message'][
            "peer"] + event['message']["volume"] + event['message']["brick"]
        message = "Brick path resolution failed for brick: {0} . Volume: {1}" \
                  ".Peer: {2}".format(
                      event['message']["brick"],
                      event['message']["volume"],
                      event['message']['peer']
                  )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="brick_path_resolve_failed",
            alert_notify=True
        )
        native_event.save()

    def quota_crossed_soft_limit(self, event):
        context = "quota_crossed_soft_limit|" + event[
            "message"]["volume"] + event["message"]["path"]
        message = "Quota soft limit crossed in volume: {0} for path: {1}" \
                  ". Current usage: {2}".format(
                      event['message']['volume'],
                      event['message']['path'],
                      event['message']['usage'],
                  )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="quota_crossed_soft_limit",
            alert_notify=True
        )
        native_event.save()

    def bitrot_bad_file(self, event):
        context = "bitrot_bad_file|" + event['message'][
            "brick"] + event['message']["path"] + event['message']["gfid"]
        message = "File with gfid: {0} is corrupted due to bitrot." \
                  "  Brick: {1}. Path: {2}".format(
                      event['message']['gfid'],
                      event['message']['brick'],
                      event['message']['path'],
                  )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="bitrot_bad_file",
            alert_notify=True
        )
        native_event.save()

    def afr_split_brain(self, event):
        context = "afr_split_brain|" + event['message']["subvol"]
        message = "Subvolume: {0} is affected by split-brain. Some of the" \
                  "replicated files in the volume might be divergent".format(
                      event['message']['subvol']
                  )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="afr_split_brain",
            alert_notify=True
        )
        native_event.save()

    def snapshot_soft_limit_reached(self, event):
        context = "snapshot_soft_limit_reached|" + event[
            'message']['volume_name']
        message = "Snapshot soft limit reached for volume: {0}".format(
            event['message']['volume_name']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="snapshot_soft_limit_reached",
            alert_notify=True
        )
        native_event.save()

    def snapshot_hard_limit_reached(self, event):
        context = "snapshot_hard_limit_reached|" + event[
            'message']['volume_name']
        message = "Snapshot hard limit reached for volume: {0}".format(
            event['message']['volume_name']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="snapshot_hard_limit_reached",
            alert_notify=True
        )
        native_event.save()

    def compare_friend_volume_failed(self, event):
        context = "compare_friend_volume_failed|" + event['message']['volume']
        message = "Compare friend volume failed for volume: {0}".format(
            event['message']['volume']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="compare_friend_volume_failed",
            alert_notify=True
        )
        native_event.save()

    def posix_health_check_failed(self, event):
        context = "posix_health_check_failed|" + event[
            'message']["brick"] + event['message']["path"]
        message = "Posix health check failed for brick: {}. Path: {1}" \
                  ". Error: {2}. op: {3}".format(
                      event['message']["brick"],
                      event['message']["path"],
                      event['message']["error"],
                      event['message']["op"],
                  )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="posix_health_check_failed",
            alert_notify=True
        )
        native_event.save()

    def peer_reject(self, event):
        context = "peer_reject|" + event['message']['peer']
        message = "Peer: {0} is rejected".format(
            event['message']['peer']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="peer_reject",
            alert_notify=True
        )
        native_event.save()

    def rebalance_status_update_failed(self, event):
        context = "rebalance_status_update_failed|" + event[
            'message']["volume"]
        message = "Rebalance status update failed for volume: {0}".format(
            event['message']["volume"]
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="rebalance_status_update_failed",
            alert_notify=True
        )
        native_event.save()

    def svc_reconfigure_failed(self, event):
        context = "svc_reconfigure_failed|" + event['message']["service"]
        volname = event['message'].get('volume', '')
        if volname:
            context += volname

        message = "Service reconfigure failed for service: {0}".format(
            event['message']['svc_name']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="warning",
            current_value="svc_reconfigure_failed",
            alert_notify=True
        )
        native_event.save()

    def georep_checkpoint_completed(self, event):
        # TODO(darshan) json content not known yet
        context = "georep_checkpoint_completed|" + event['message']["session"]
        message = "Georeplication checkpoint completed for session {0}".format(
            event['message']['session']
        )
        native_event = NS.gluster.objects.NativeEvents(
            context,
            message=message,
            severity="info",
            current_value="georep_checkpoint_completed",
            alert_notify=True
        )
        native_event.save()

    def peer_connect(self, event):
        job_id = monitoring_utils.update_dashboard(
            event['message']['host'],
            RESOURCE_TYPE_PEER,
            NS.tendrl_context.integration_id,
            "add"
        )
        logger.log(
            "debug",
            NS.publisher_id,
            {
                "message": "Update dashboard job %s "
                "created" % job_id
            }
        )

    def peer_disconnect(self, event):
        job_id = monitoring_utils.update_dashboard(
            event['message']['host'],
            RESOURCE_TYPE_PEER,
            NS.tendrl_context.integration_id,
            "delete"
        )
        logger.log(
            "debug",
            NS.publisher_id,
            {
                "message": "Update dashboard job %s "
                "created" % job_id
            }
        )

    def volume_create(self, event):
        job_id = monitoring_utils.update_dashboard(
            event['message']['name'],
            RESOURCE_TYPE_VOLUME,
            NS.tendrl_context.integration_id,
            "add"
        )
        logger.log(
            "debug",
            NS.publisher_id,
            {
                "message": "Update dashboard job %s "
                "created" % job_id
            }
        )

    def volume_delete(self, event):
        job_id = monitoring_utils.update_dashboard(
            event['message']['name'],
            RESOURCE_TYPE_VOLUME,
            NS.tendrl_context.integration_id,
            "delete"
        )
        logger.log(
            "debug",
            NS.publisher_id,
            {
                "message": "Update dashboard job %s "
                "created" % job_id
            }
        )

    def volume_add_brick(self, event):
        # Event returns bricks list as space separated single string
        added_bricks = event['message']['bricks'].split(" ")
        for brick in added_bricks:
            job_id = monitoring_utils.update_dashboard(
                "%s|%s" % (event['message']['volume'], brick),
                RESOURCE_TYPE_BRICK,
                NS.tendrl_context.integration_id,
                "add"
            )
            logger.log(
                "debug",
                NS.publisher_id,
                {
                    "message": "Update dashboard job %s "
                    "created" % job_id
                }
            )

    def volume_remove_brick_force(self, event):
        # Event returns bricks list as space separated single string
        bricks = event['message']['bricks'].split(" ")
        for brick in bricks:
            job_id = monitoring_utils.update_dashboard(
                "%s|%s" % (event['message']['volume'], brick),
                RESOURCE_TYPE_BRICK,
                NS.tendrl_context.integration_id,
                "delete"
            )
            logger.log(
                "debug",
                NS.publisher_id,
                {
                    "message": "Update dashboard job %s "
                    "created" % job_id
                }
            )

    def volume_remove_brick_commit(self, event):
        self.volume_remove_brick_force(event)
