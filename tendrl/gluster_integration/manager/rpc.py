import json
import logging
import traceback
import uuid

import etcd
import gevent.event
import yaml

from tendrl.common.definitions.validator import DefinitionsSchemaValidator
from tendrl.gluster_integration.config import TendrlConfig
from tendrl.gluster_integration.flows.flow_execution_exception import \
    FlowExecutionFailedError
from tendrl.gluster_integration.manager import utils


config = TendrlConfig()
LOG = logging.getLogger(__name__)


class EtcdRPC(object):

    def __init__(self, Etcdthread):
        etcd_kwargs = {'port': int(config.get("common", "etcd_port")),
                       'host': config.get("common", "etcd_connection")}

        self.client = etcd.Client(**etcd_kwargs)
        self.integration_id = utils.get_tendrl_context()
        self.Etcdthread = Etcdthread

    def _process_job(self, raw_job, job_key):
        # Pick up the "new" job that is not locked by any other integration
        if raw_job['status'] == "new" and raw_job["type"] == "sds" and \
                raw_job['cluster_id'] == self.integration_id:
                raw_job['status'] = "processing"
                # Generate a request ID for tracking this job
                # further by tendrl-api
                req_id = str(uuid.uuid4())
                raw_job['request_id'] = "%s/flow_%s" % (
                    self.integration_id, req_id)
                self.client.write(job_key, json.dumps(raw_job))
                LOG.info("Processing JOB %s" % raw_job[
                    'request_id'])
                try:
                    definitions = self.validate_flow(raw_job)
                    if definitions:
                        self.invoke_flow(raw_job['run'], raw_job, definitions)
                except FlowExecutionFailedError as e:
                    # TODO(rohan) print more of this error msg here
                    LOG.error(e)
                    raw_job['status'] = "failed"
                else:
                    raw_job['status'] = "finished"

                return raw_job, True
        else:
            return raw_job, False

    def _acceptor(self):
        while not self.Etcdthread._complete.is_set():
            jobs = self.client.read("/queue")
            for job in jobs.children:
                executed = False
                if job.value is None:
                    LOG.info("JOB /queue is empty!!")
                    continue
                raw_job = json.loads(job.value.decode('utf-8'))
                try:
                    raw_job, executed = self._process_job(raw_job, job.key)
                    if "etcd_client" in raw_job['parameters']:
                        del raw_job['parameters']['etcd_client']
                except FlowExecutionFailedError as e:
                    LOG.error(
                        "Failed to execute job: %s. Error: %s" %
                        (str(job), str(e))
                    )
                if executed:
                    self.client.write(job.key, json.dumps(raw_job))
                    break
            gevent.sleep(2)

    def run(self):
        self._acceptor()

    def stop(self):
        pass

    def validate_flow(self, raw_job):
        LOG.info("Validating flow %s for %s" % (raw_job['run'],
                                                raw_job['request_id']))
        definitions = yaml.load(
            self.client.read('/clusters/%s/definitions/data' % raw_job[
                'cluster_id']).
            value.decode("utf-8")
        )
        definitions = DefinitionsSchemaValidator(
            definitions).sanitize_definitions()
        # resp, msg = JobValidator(definitions).validateApi(raw_job)
        # if resp:
        #    msg = "Successfull Validation flow %s for %s" %\
        #          (raw_job['run'], raw_job['request_id'])
        #    LOG.info(msg)

        return definitions
        # else:
        #    msg = "Failed Validation flow %s for %s" % (raw_job['run'],
        #                                               raw_job['request_id'])
        #    LOG.error(msg)
        #    return False

    def invoke_flow(self, flow_name, job, definitions):
        atoms, pre_run, post_run, uuid = self.extract_flow_details(
            flow_name,
            definitions
        )
        the_flow = None
        flow_path = flow_name.split('.')
        flow_module = ".".join([a.encode("ascii", "ignore") for a in
                                flow_path[:-1]])
        kls_name = ".".join([a.encode("ascii", "ignore") for a in
                             flow_path[-1:]])
        if "tendrl" in flow_path and "flows" in flow_path:
            exec("from %s import %s as the_flow" % (flow_module, kls_name))
            return the_flow(flow_name, job, atoms, pre_run, post_run,
                            uuid).run()

    def extract_flow_details(self, flow_name, definitions):
        namespace = flow_name.split(".flows.")[0]
        flow = definitions[namespace]['flows'][flow_name.split(".")[-1]]
        return flow['atoms'], flow['pre_run'], flow['post_run'], flow['uuid']


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
        self._server = EtcdRPC(self)

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
