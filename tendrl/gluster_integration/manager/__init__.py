import signal
import threading

from tendrl.commons import manager as common_manager
from tendrl.commons import TendrlNS
from tendrl.commons.utils import log_utils as logger
from tendrl import gluster_integration
from tendrl.gluster_integration.gdeploy_wrapper.manager import \
    ProvisioningManager
from tendrl.gluster_integration.message.gluster_native_message_handler\
    import GlusterNativeMessageHandler
from tendrl.gluster_integration import sds_sync


class GlusterIntegrationManager(common_manager.Manager):
    def __init__(self):
        self._complete = threading.Event()
        super(
            GlusterIntegrationManager,
            self
        ).__init__(
            NS.state_sync_thread,
            message_handler_thread=NS.message_handler_thread
        )


def main():
    gluster_integration.GlusterIntegrationNS()
    TendrlNS()

    NS.type = "sds"
    NS.publisher_id = "gluster_integration"

    NS.state_sync_thread = sds_sync.GlusterIntegrationSdsSyncStateThread()

    NS.message_handler_thread = GlusterNativeMessageHandler()

    while NS.tendrl_context.integration_id is None or \
        NS.tendrl_context.integration_id == "":
        logger.log(
            "debug",
            NS.publisher_id,
            {
                "message": "Waiting for tendrl-node-agent %s to "
                "detect sds cluster (integration_id not found)" %
                NS.node_context.node_id
            }
        )
        NS.tendrl_context = NS.tendrl_context.load()

    logger.log(
        "debug",
        NS.publisher_id,
        {
            "message": "Integration %s is part of sds cluster" %
            NS.tendrl_context.integration_id
        }
    )

    NS.gluster.definitions.save()
    NS.gluster.config.save()

    pm = ProvisioningManager("GdeployPlugin")
    NS.gdeploy_plugin = pm.get_plugin()
    if NS.config.data.get("with_internal_profiling", False):
        from tendrl.commons import profiler
        profiler.start()

    m = GlusterIntegrationManager()
    m.start()

    complete = threading.Event()

    def shutdown(signum, frame):
        logger.log(
            "debug",
            NS.publisher_id,
            {"message": "Signal handler: stopping"}
        )
        complete.set()
        m.stop()

    def reload_config(signum, frame):
        logger.log(
            "debug",
            NS.publisher_id,
            {
                "message": "Signal handler: SIGHUP,"
                " reload service config"
            }
        )
        NS.gluster.ns.setup_common_objects()

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGHUP, reload_config)

    while not complete.is_set():
        complete.wait(timeout=1)


if __name__ == "__main__":
    main()
