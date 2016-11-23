import gc
import greenlet
import json
import logging
import signal
import subprocess
import sys
import time
import traceback

import gevent.event
import gevent.greenlet

from tendrl.common import log

from tendrl.gluster_integration.manager.rpc import EtcdThread
from tendrl.gluster_integration.manager.tendrl_definitions_gluster import data as \
    def_data
from tendrl.gluster_integration.manager import utils

from tendrl.gluster_integration.persistence.persister import Persister
from tendrl.gluster_integration.persistence.servers import Brick
from tendrl.gluster_integration.persistence.servers import Peer
from tendrl.gluster_integration.persistence.servers import Volume

from tendrl.gluster_integration import ini2json

from tendrl.gluster_integration.config import TendrlConfig
from tendrl.gluster_integration.persistence.tendrl_context import TendrlContext
from tendrl.gluster_integration.persistence.tendrl_definitions import \
    TendrlDefinitions

config = TendrlConfig()

LOG = logging.getLogger(__name__)


class TopLevelEvents(gevent.greenlet.Greenlet):

    def __init__(self, manager, cluster_id):
        super(TopLevelEvents, self).__init__()

        self._manager = manager
        self._complete = gevent.event.Event()
        self.cluster_id = cluster_id

    def stop(self):
        self._complete.set()

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


class Manager(object):
    """Manage a collection of ClusterMonitors.

    Subscribe to ceph/cluster events, and create a ClusterMonitor

    for any FSID we haven't seen before.

    """

    def __init__(self, cluster_id):
        self._complete = gevent.event.Event()

        self._user_request_thread = EtcdThread(self)
        self._discovery_thread = TopLevelEvents(self, cluster_id)
        self.persister = Persister()
        self.register_to_cluster(cluster_id)

    def stop(self):
        LOG.info("%s stopping" % self.__class__.__name__)
        self._user_request_thread.stop()
        self._discovery_thread.stop()

    def _recover(self):
        LOG.debug("Recovered server")
        pass

    def start(self):
        LOG.info("%s starting" % self.__class__.__name__)
        self._user_request_thread.start()
        self._discovery_thread.start()
        self.persister.start()

    def join(self):
        LOG.info("%s joining" % self.__class__.__name__)
        self._user_request_thread.join()
        self._discovery_thread.join()
        self.persister.join()

    def on_pull(self, raw_data, cluster_id):
        LOG.info("on_pull")
        self.persister.update_sync_object(
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
                    self.persister.update_peer(
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
                    self.persister.update_volume(
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
                            self.persister.update_brick(
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
        self.persister.update_tendrl_context(
            TendrlContext(
                updated=str(time.time()),
                cluster_id=cluster_id,
                sds_name="gluster",
                sds_version=utils.get_sds_version()
            )
        )

        self.persister.update_tendrl_definitions(
            TendrlDefinitions(
                updated=str(time.time()),
                data=def_data,
                cluster_id=cluster_id
            )
        )


def dump_stacks():
    """This is for use in debugging, especially using manhole

    """
    for ob in gc.get_objects():
        if not isinstance(ob, greenlet.greenlet):
            continue
        if not ob:
            continue
        LOG.error(''.join(traceback.format_stack(ob.gr_frame)))


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

    m = Manager(utils.get_tendrl_context())
    m.start()

    complete = gevent.event.Event()

    def shutdown():
        LOG.info("Signal handler: stopping")
        complete.set()

    gevent.signal(signal.SIGTERM, shutdown)
    gevent.signal(signal.SIGINT, shutdown)

    while not complete.is_set():
        complete.wait(timeout=1)
