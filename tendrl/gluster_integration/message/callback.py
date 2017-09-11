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
                brick,
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
                brick,
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
