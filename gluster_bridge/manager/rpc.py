import etcd
import gevent.event
import json
import subprocess
import time
import traceback
import uuid

from gluster_bridge.config import CONF
from gluster_bridge.log import LOG


class RpcInterface(object):

    def __init__(self, manager):
        self._manager = manager

    def __getattribute__(self, item):
        """Wrap functions with LOGging

        """
        if item.startswith('_'):
            return object.__getattribute__(self, item)
        else:
            attr = object.__getattribute__(self, item)
            if callable(attr):
                def wrap(*args, **kwargs):
                    LOG.debug("RpcInterface >> %s(%s, %s)" %
                              (item, args, kwargs))
                    try:
                        rc = attr(*args, **kwargs)
                        LOG.debug("RpcInterface << %s" % item)
                    except Exception:
                        LOG.exception("RpcInterface !! %s" % item)
                        raise
                    return rc
                return wrap
            else:
                return attr

    def create_volume(self, name, bricks):
        LOG.info("create_volume %s" % name)
        subprocess.call(['gluster', 'volume', 'create',
                         name, ' '.join(bricks), ' force'])
        subprocess.call(['gluster', 'volume', 'start', name])

    def delete_volume(self, name):
        LOG.info("delete_volume %s" % name)
        subprocess.Popen(['gluster', 'volume', 'stop', name],
                         stdin=subprocess.PIPE).communicate(input="y\n")
        subprocess.Popen(['gluster', 'volume', 'delete', name],
                         stdin=subprocess.PIPE).communicate(input="y\n")


class EtcdRPC(object):

    def __init__(self, methods):
        self._methods = self._filter_methods(EtcdRPC, self, methods)
        etcd_kwargs = {'port': CONF.bridge.etcd_port,
                       'host': CONF.bridge.etcd_connection}

        self.client = etcd.Client(**etcd_kwargs)
        self.bridge_id = str(uuid.uuid4())

    @staticmethod
    def _filter_methods(cls, self, methods):
        if hasattr(methods, '__getitem__'):
            return methods
        server_methods = set(getattr(self, k) for k in dir(cls) if not
                             k.startswith('_'))
        return dict((k, getattr(methods, k))
                    for k in dir(methods)
                    if callable(
            getattr(methods, k)) and not k.startswith('_') and getattr(
            methods, k) not in server_methods
        )

    def __call__(self, method, kwargs=None, *args):
        if method not in self._methods:
            raise NameError(method)
        return self._methods[method](*args, **kwargs)

    def _acceptor(self):
        while True:
            raw_jobs = self.client.read("/rawops/jobs")
            jobs = sorted(json.loads(raw_jobs.value),
                          key=lambda k: int(k['updated']))
            # Pick up the oldest job that is not locked by any other bridge
            try:
                for job in jobs:

                    if not job['locked_by']:
                        # First lock the job

                        LOG.info("%s found new job_%s" %
                                 (self.__class__.__name__, job['job_id']))
                        LOG.debug(job['msg'])
                        job['locked_by'] = self.bridge_id
                        job['status'] = "in-progress"
                        job['updated'] = int(time.time())
                        raw_jobs.value = json.dumps(jobs)
                        self.client.write("/rawops/jobs", raw_jobs.value)
                        LOG.info("%s Running new job_%s" %
                                 (self.__class__.__name__, job['job_id']))
                        self.__call__(job['msg']['func'],
                                      kwargs=job['msg']['kwargs'])
                        job['updated'] = int(time.time())
                        job['status'] = "complete"
                        raw_jobs.value = json.dumps(jobs)
                        self.client.write("/rawops/jobs", raw_jobs.value)
                        LOG.info("%s Completed job_%s" %
                                 (self.__class__.__name__, job['job_id']))

                        break
            except Exception as ex:
                LOG.error(ex)
            gevent.sleep(1)

    def run(self):
        self._acceptor()

    def stop(self):
        pass


class EtcdThread(gevent.greenlet.Greenlet):
    """Present a ZeroRPC API for users

    to request state changes.

    """

    # In case server.run throws an exception, prevent
    # really aggressive spinning
    EXCEPTION_BACKOFF = 5

    def __init__(self, manager):
        super(EtcdThread, self).__init__()
        self._manager = manager
        self._complete = gevent.event.Event()
        self._server = EtcdRPC(RpcInterface(manager))

    def stop(self):
        LOG.info("%s stopping" % self.__class__.__name__)

        self._complete.set()
        if self._server:
            self._server.stop()

    def _run(self):

        while not self._complete.is_set():
            try:
                LOG.info("%s run..." % self.__class__.__name__)
                self._server.run()
            except Exception:
                LOG.error(traceback.format_exc())
                self._complete.wait(self.EXCEPTION_BACKOFF)

        LOG.info("%s complete..." % self.__class__.__name__)
