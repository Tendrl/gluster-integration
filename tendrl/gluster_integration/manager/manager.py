import gevent.event
import json
import logging
import signal
import subprocess
import sys
import time

from tendrl.common.config import TendrlConfig
from tendrl.common import log
from tendrl.common.manager.manager import Manager
from tendrl.common.manager.manager import SyncStateThread

from tendrl.gluster_integration import ini2json
from tendrl.gluster_integration.manager.tendrl_definitions_gluster \
    import data as def_data
from tendrl.gluster_integration.manager import utils
from tendrl.gluster_integration.persistence.persister \
    import GlusterIntegrationEtcdPersister
from tendrl.gluster_integration.persistence.servers import Brick
from tendrl.gluster_integration.persistence.servers import Peer
from tendrl.gluster_integration.persistence.servers import Volume
from tendrl.gluster_integration.persistence.tendrl_context import TendrlContext
from tendrl.gluster_integration.persistence.tendrl_definitions import \
    TendrlDefinitions

config = TendrlConfig("gluster_integration", "/etc/tendrl/tendrl.conf")

LOG = logging.getLogger(__name__)


class GlusterIntegrationSyncStateThread(SyncStateThread):

    def __init__(self, manager, cluster_id):
        super(GlusterIntegrationSyncStateThread, self).__init__(manager)

        self._manager = manager
        self._complete = gevent.event.Event()
        self.cluster_id = cluster_id

    def _run(self):
        LOG.info("%s running" % self.__class__.__name__)

        while not self._complete.is_set():
            try:
                gevent.sleep(3)
                subprocess.call(
                    [
                        'gluster',
                        'get-state',
                        'glusterd',
                        'odir',
                        '/var/run',
                        'file',
                        'glusterd-state'
                    ]
                )
                raw_data = ini2json.ini_to_dict('/var/run/glusterd-state')
                subprocess.call(['rm', '-rf', '/var/run/glusterd-state'])
                self._manager.on_pull(raw_data, self.cluster_id)
            except Exception as ex:
                LOG.error(ex)

        LOG.info("%s complete" % self.__class__.__name__)


class GlusterIntegrationManager(Manager):
    def __init__(self, cluster_id):
        self._complete = gevent.event.Event()
        super(
            GlusterIntegrationManager,
            self
        ).__init__(
            "sds",
            cluster_id,
            config,
            GlusterIntegrationSyncStateThread(self, cluster_id),
            GlusterIntegrationEtcdPersister(config),
            "clusters/%s/definitions/data" % cluster_id
        )
        self.register_to_cluster(cluster_id)

    def on_pull(self, raw_data, cluster_id):
        LOG.info("on_pull")
        self.persister_thread.update_sync_object(
            str(time.time()),
            cluster_id,
            json.dumps(raw_data)
        )
        if "Peers" in raw_data:
            LOG.info("on_pull, Updating Peers data")
            index = 1
            peers = raw_data['Peers']
            while True:
                try:
                    self.persister_thread.update_peer(
                        Peer(
                            updated=str(time.time()),
                            cluster_id=cluster_id,
                            peer_uuid=peers['peer%s.uuid' % index],
                            hostname=peers[
                                'peer%s.primary_hostname' % index],
                            state=peers['peer%s.state' % index])
                    )
                    LOG.info("on_pull, Updating Peer %s/%s" %
                             (peers['peer%s.uuid' % index],
                              peers['peer%s.primary_hostname' % index])
                             )
                    index += 1
                except KeyError:
                    break
        if "Volumes" in raw_data:
            LOG.info("on_pull, Updating Volumes data")
            index = 1
            volumes = raw_data['Volumes']
            while True:
                try:
                    self.persister_thread.update_volume(
                        Volume(
                            cluster_id=cluster_id,
                            vol_id=volumes['volume%s.id' % index],
                            vol_type=volumes['volume%s.type' % index],
                            name=volumes['volume%s.name' % index],
                            status=volumes['volume%s.status' % index],
                            brick_count=volumes['volume%s.brickcount' % index])
                    )
                    LOG.info("on_pull, Updating Volume %s" %
                             volumes['volume%s.id' % index])

                    b_index = 1
                    # populate brick data for this volume
                    while True:
                        try:
                            self.persister_thread.update_brick(
                                Brick(
                                    cluster_id=cluster_id,
                                    vol_id=volumes['volume%s.id' % index],
                                    path=volumes[
                                        'volume%s.brick%s.path' % (
                                            index, b_index)],
                                    hostname=volumes.get(
                                        'volume%s.brick%s.hostname' % (
                                            index, b_index)),
                                    port=volumes.get(
                                        'volume%s.brick%s.port' % (
                                            index, b_index)),
                                    status=volumes.get(
                                        'volume%s.brick%s.status' % (
                                            index, b_index)),
                                    filesystem_type=volumes.get(
                                        'volume%s.brick%s.filesystem_type' % (
                                            index, b_index)),
                                    mount_options=volumes.get(
                                        'volume%s.brick%s.mount_options' % (
                                            index, b_index))
                                )
                            )
                            LOG.info(
                                "on_pull, Updating Brick %s for Volume %s" % (
                                    volumes[
                                        'volume%s.brick%s.path' % (
                                            index, b_index)],
                                    volumes['volume%s.id' % index])
                            )
                            b_index += 1
                        except KeyError:
                            break

                    index += 1
                except KeyError:
                    break

    def register_to_cluster(self, cluster_id):
        self.persister_thread.update_tendrl_context(
            TendrlContext(
                updated=str(time.time()),
                cluster_id=cluster_id,
                sds_name="gluster",
                sds_version=utils.get_sds_version()
            )
        )

        self.persister_thread.update_tendrl_definitions(
            TendrlDefinitions(
                updated=str(time.time()),
                data=def_data,
                cluster_id=cluster_id
            )
        )


def main():
    log.setup_logging(
        config.get('gluster_integration', 'log_cfg_path'),
        config.get('gluster_integration', 'log_level')
    )

    if sys.argv:
        if len(sys.argv) > 1:
            if "cluster-id" in sys.argv[1]:
                cluster_id = sys.argv[2]
                utils.set_tendrl_context(cluster_id)

    m = GlusterIntegrationManager(utils.get_tendrl_context())
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
