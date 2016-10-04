import etcd
import gevent.event
import json
import subprocess
import re
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
            jobs = self.client.read("/api_job_queue")
            for job in jobs.children:
                raw_job = json.loads(job.value.decode('utf-8'))
                # Pick up the "new" job that is not locked by any other bridge
                if raw_job['status'] == "new":
                    try:
                        raw_job['status'] = "processing"
                        # Generate a request ID for tracking this job
                        # further by tendrl-api
                        req_id = str(uuid.uuid4())
                        raw_job['request_id'] = "%s/%s" % (self.bridge_id, req_id)
                        self.client.write(job.key, json.dumps(raw_job))
                        gevent.sleep(2)
                        LOG.info("Processing API-JOB %s" % raw_job[
                            'request_id'])
                        self.invoke_flow(raw_job['flow'], raw_job)
                        break
                    except Exception as ex:
                        LOG.error(ex)


    def run(self):
        self._acceptor()

    def stop(self):
        pass

    def invoke_flow(self, flow_name, api_job):
        # TODO (rohan) parse sds_operations_gluster.yaml and correlate here
        flow_module = 'gluster_bridge.flows.%s' % self.convert_flow_name(flow_name)
        mod = __import__(flow_module, fromlist=[
            flow_name])
        klass = getattr(mod, flow_name)
        klass(api_job)
        klass.start()

    def convert_flow_name(self, flow_name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', flow_name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


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
