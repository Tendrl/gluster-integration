import argparse
import hashlib
import logging
import os
import gc
import re
import subprocess
import time
import signal
import traceback
import json
import sys

import gevent.event
import gevent.socket as socket
import greenlet
from dateutil.tz import tzutc
import gevent.greenlet


from tendrl.gluster_bridge.log import log
import tendrl.gluster_bridge.log
from tendrl.gluster_bridge.util import Ticker
from tendrl.gluster_bridge.manager.eventer import Eventer
from tendrl.gluster_bridge.manager.rpc import EtcdThread
from tendrl.gluster_bridge.manager import config, salt_config


from tendrl.gluster_bridge.persistence.sync_objects import SyncObject
from tendrl.gluster_bridge.persistence.persister import Persister
from tendrl.gluster_bridge.persistence.servers import Peer, Volume, Brick


from tendrl.gluster_bridge.common import ini2json

# Manhole module optional for debugging.
try:
    import manhole
except ImportError:
    manhole = None


class TopLevelEvents(gevent.greenlet.Greenlet):
    def __init__(self, manager):
        super(TopLevelEvents, self).__init__()

        self._manager = manager
        self._complete = gevent.event.Event()

    def stop(self):
        self._complete.set()

    def _run(self):
        log.info("%s running" % self.__class__.__name__)

        while not self._complete.is_set():
            try:
                gevent.sleep(3)
                subprocess.call(['gluster', 'daemon', 'get-state', 'odir', '/tmp/'])
                raw_data = ini2json.ini_to_dict('/tmp/glusterd-state')
                subprocess.call(['rm', '-rf', '/tmp/glusterd-state'])
                self._manager.on_pull(raw_data)
            except Exception as ex:
                log.error(ex)

        log.info("%s complete" % self.__class__.__name__)


class Manager(object):
    """
    Manage a collection of ClusterMonitors.

    Subscribe to ceph/cluster events, and create a ClusterMonitor
    for any FSID we haven't seen before.
    """

    def __init__(self):
        self._complete = gevent.event.Event()

        self._user_request_thread = EtcdThread(self)
        self._discovery_thread = TopLevelEvents(self)
        self.persister = Persister()


    def stop(self):
        log.info("%s stopping" % self.__class__.__name__)
        self._user_request_thread.stop()
        self._discovery_thread.stop()

    def _recover(self):
        log.debug("Recovered server")
        pass

    def start(self):
        log.info("%s starting" % self.__class__.__name__)
        self._user_request_thread.start()
        self._discovery_thread.start()
        self.persister.start()

    def join(self):
        log.info("%s joining" % self.__class__.__name__)
        self._user_request_thread.join()
        self._discovery_thread.join()
        self.persister.join()


    def on_pull(self, raw_data):
        log.info("on_pull")
        self.persister.update_sync_object(updated=str(time.time()), data=json.dumps(raw_data))
        if "Peers" in raw_data:
            log.info("on_pull, Updating Peers data")
            index = 1
            peers = raw_data['Peers']
            while True:
                try:
                    self.persister.update_peer(Peer(updated=str(time.time()), peer_uuid=peers['peer%s.uuid' % index],
                                               hostname=peers['peer%s.hostname' % index],
                                               state=peers['peer%s.state' % index]))
                    log.info("on_pull, Updating Peer %s/%s" % (peers['peer%s.uuid' % index], peers['peer%s.hostname' % index]))
                    index += 1
                except KeyError:
                    break
        if "Volumes" in raw_data:
            log.info("on_pull, Updating Volumes data")
            index = 1
            volumes = raw_data['Volumes']
            while True:
                try:
                    self.persister.update_volume(Volume(vol_id=volumes['volume%s.id' % index], vol_type=volumes['volume%s.type' % index], name=volumes['volume%s.name' % index],
                                 status=volumes['volume%s.status' % index], brick_count=volumes['volume%s.brickcount' % index]))
                    log.info("on_pull, Updating Volume %s" % volumes['volume%s.id' % index])

                    b_index = 1
                    # populate brick data for this volume
                    while True:
                        try:
                            self.persister.update_brick(Brick(vol_id=volumes['volume%s.id' % index], path=volumes['volume%s.brick%s.path' % (index, b_index)], hostname=volumes.get('volume%s.brick%s.hostname' % (index, b_index)),
                                                port=volumes.get('volume%s.brick%s.port' % (index, b_index)), status=volumes.get('volume%s.brick%s.status' % (index, b_index)),
                                                filesystem_type=volumes.get('volume%s.brick%s.filesystem_type' % (index, b_index)),
                                                mount_options=volumes.get('volume%s.brick%s.mount_options' % (index, b_index))))
                            log.info("on_pull, Updating Brick %s for Volume %s" % (volumes['volume%s.brick%s.path' % (index, b_index)], volumes['volume%s.id' % index]))
                            b_index += 1
                        except KeyError:
                            break

                    index += 1
                except KeyError:
                    break





def dump_stacks():
    """
    This is for use in debugging, especially using manhole
    """
    for ob in gc.get_objects():
        if not isinstance(ob, greenlet.greenlet):
            continue
        if not ob:
            continue
        log.error(''.join(traceback.format_stack(ob.gr_frame)))


def main():
    parser = argparse.ArgumentParser(description='tendrl gluster_bridge Bridge')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='print log to stdout')

    args = parser.parse_args()
    if args.debug:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(tendrl.log.FORMAT))
        log.addHandler(handler)


    if manhole is not None:
        # Enable manhole for debugging.  Use oneshot mode
        # for gevent compatibility
        manhole.cry = lambda message: log.info("MANHOLE: %s" % message)
        manhole.install(oneshot_on=signal.SIGUSR1)

    m = Manager()
    m.start()

    complete = gevent.event.Event()

    def shutdown():
        log.info("Signal handler: stopping")
        complete.set()

    gevent.signal(signal.SIGTERM, shutdown)
    gevent.signal(signal.SIGINT, shutdown)

    while not complete.is_set():
        complete.wait(timeout=1)
