import logging

import gevent.event
import gevent.greenlet
import gevent.queue
from tendrl.bridge_common.etcdobj.etcdobj import Server as etcd_server


from tendrl.gluster_bridge.config import TendrlConfig
from tendrl.gluster_bridge.persistence.sync_objects import SyncObject


config = TendrlConfig()
LOG = logging.getLogger(__name__)


class deferred_call(object):

    def __init__(self, fn, args, kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def call_it(self):
        self.fn(*self.args, **self.kwargs)


class Persister(gevent.greenlet.Greenlet):
    """Asynchronously persist a queue of updates.  This is for use by classes

    that maintain the primary copy of state in memory, but also lazily update

    the DB so that they can recover from it on restart.

    """

    def __init__(self):
        super(Persister, self).__init__()

        self._queue = gevent.queue.Queue()
        self._complete = gevent.event.Event()

        self._store = self.get_store()

    def __getattribute__(self, item):
        """Wrap functions with LOGging

        """
        if item.startswith('_'):
            return object.__getattribute__(self, item)
        else:
            try:
                return object.__getattribute__(self, item)
            except AttributeError:
                try:
                    attr = object.__getattribute__(self, "_%s" % item)
                    if callable(attr):
                        def defer(*args, **kwargs):
                            dc = deferred_call(attr, args, kwargs)
                            try:
                                dc.call_it()
                            except Exception as ex:
                                LOG.exception(
                                    "Persister exception persisting "
                                    "data: %s" % (dc.fn,)
                                )
                                LOG.exception(ex)
                        return defer
                    else:
                        return object.__getattribute__(self, item)
                except AttributeError:
                    return object.__getattribute__(self, item)

    def update_sync_object(self, updated, cluster_id, data):
        self._store.save(SyncObject(updated=updated, cluster_id=cluster_id, data=data))

    def _update_peer(self, peer):
        self._store.save(peer)

    def _update_volume(self, vol):
        self._store.save(vol)

    def _update_brick(self, brick):
        self._store.save(brick)

    def _save_events(self, events):
        for event in events:
            self._store.save(event)

    def _run(self):
        LOG.info("Persister listening")

        while not self._complete.is_set():
            gevent.sleep(0.1)
            pass

    def stop(self):
        self._complete.set()

    def get_store(self):
        etcd_kwargs = {'port': int(config.get("bridge_common", "etcd_port")),
                       'host': config.get("bridge_common", "etcd_connection")}
        return etcd_server(etcd_kwargs=etcd_kwargs)
