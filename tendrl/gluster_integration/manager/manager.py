import gevent.event
import logging
import signal

from tendrl.commons.config import load_config
from tendrl.commons.log import setup_logging
from tendrl.gluster_integration import central_store
from tendrl.gluster_integration import manager
from tendrl.gluster_integration import sds_sync
from tendrl.gluster_integration.manager import utils

LOG = logging.getLogger(__name__)

config = load_config(
    "gluster-integration",
    "/etc/tendrl/gluster-integration/gluster-integration.conf.yaml"
)


def main():
    tendrl_ns.register_subclasses_to_ns()
    tendrl_ns.setup_initial_objects()

    setup_logging(config['log_cfg_path'])

    tendrl_ns.central_store_thread = central_store.GlusterIntegrationEtcdCentralStore()
    tendrl_ns.state_sync_thread = sds_sync.GlusterIntegrationSdsSyncStateThread()

    tendrl_ns.tendrl_context.save()
    tendrl_ns.definitions.save()
    tendrl_ns.config.save()

    m = manager.GlusterIntegrationManager()
    m.start()

    complete = gevent.event.Event()

    def shutdown():
        LOG.info("Signal handler: stopping")
        complete.set()

    gevent.signal(signal.SIGTERM, shutdown)
    gevent.signal(signal.SIGINT, shutdown)

    while not complete.is_set():
        complete.wait(timeout=1)


if __name__ == "__main__":
    main()
