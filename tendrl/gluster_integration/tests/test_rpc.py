import json
from mock import MagicMock
import sys
sys.modules['tendrl.gluster_integration.config'] = MagicMock()
from tendrl.gluster_integration.manager import rpc
del sys.modules['tendrl.gluster_integration.config']
import uuid


class TestEtcdThread(object):
    def setup_method(self, method):
        rpc.gevent = MagicMock()
        self.count = 0
        rpc.utils.get_tendrl_context = MagicMock(
            return_value='c1367d08-6d44-4645-b101-bb5a666c44db')
        self.etcdthread = rpc.EtcdThread(MagicMock())
        self.etcdthread._complete = self

    def test_etcdthread(self, monkeypatch):
        def Mock_read(param):
            if param == '/queue':
                self.children = [Mock_Job()]
                return self
            if param == '/clusters/c1367d08-6d44-4645-b101-bb5a666c44db' \
                '/definitions/data':
                return (Mock_Job())
        monkeypatch.setattr(
            self.etcdthread._server.client, "read", Mock_read)

        def Mock_write(key, raw_job):
            self.raw_job = json.loads(raw_job)
        monkeypatch.setattr(
            self.etcdthread._server.client, "write", Mock_write)

        def Mock_uuid4():
            return 'aa22a6fe-87f0-45cf-8b70-2d0ff4c02af6'
        monkeypatch.setattr(uuid, 'uuid4', Mock_uuid4)
        self.etcdthread._server.integration_id = \
            'c1367d08-6d44-4645-b101-bb5a666c44db'

        def Mock_definitions():
            return (
                {
                    "tendrl.gluster_integration": {
                        "flows": {
                            "StartVolume": {
                                "atoms": "atoms",
                                "pre_run": "pre_run",
                                "post_run": "post_run",
                                "uuid": "uuid"
                                }
                            }
                        }
                    })

        rpc.DefinitionsSchemaValidator = MagicMock(return_value=self)
        self.sanitize_definitions = None
        monkeypatch.setattr(self, 'sanitize_definitions', Mock_definitions)
        self.etcdthread._complete = self
        sys.modules[
            'tendrl.gluster_integration.flows.start_volume'] = MagicMock()
        self.etcdthread._run()
        del sys.modules[
            'tendrl.gluster_integration.flows.start_volume']
        assert self.raw_job['status'] == 'finished'

    def test_etcdthread_failed(self, monkeypatch):
        def Mock_read(param):
            if param == '/queue':
                self.children = [Mock_Job()]
                return self
            if param == '/clusters/c1367d08-6d44-4645-b101-bb5a666c44db' \
                '/definitions/data':
                return (Mock_Job())
        monkeypatch.setattr(
            self.etcdthread._server.client, "read", Mock_read)

        def Mock_write(key, raw_job):
            self.raw_job = json.loads(raw_job)
        monkeypatch.setattr(
            self.etcdthread._server.client, "write", Mock_write)

        def Mock_uuid4():
            return 'aa22a6fe-87f0-45cf-8b70-2d0ff4c02af6'
        monkeypatch.setattr(uuid, 'uuid4', Mock_uuid4)
        self.etcdthread._server.integration_id = \
            'c1367d08-6d44-4645-b101-bb5a666c44db'

        def Mock_definitions():
            raise rpc.FlowExecutionFailedError

        rpc.DefinitionsSchemaValidator = MagicMock(return_value=self)
        self.sanitize_definitions = None
        monkeypatch.setattr(self, 'sanitize_definitions', Mock_definitions)
        self.etcdthread._complete = self
        self.etcdthread._run()
        assert self.raw_job['status'] == 'failed'

    def test_stop(self):
        self.etcdthread._complete.set = MagicMock()
        self.etcdthread.stop()
        self.etcdthread._complete.set.assert_called()

    def wait(self, *args):
        return

    def is_set(self):
        if self.count < 2:
            self.count = self.count + 1
            return False
        else:
            return True


class Mock_Job(object):
    def __init__(self):
        str = '{"action": "get", \
        "node": { \
        "key": "/queue/92d69be7-8b5d-4678-9fe7-8fc59f85c4c7", \
        "value": "", \
        "modifiedIndex": 3081, \
        "createdIndex": 3081}}'
        result = json.loads(str.decode('utf-8'))
        result["node"]["value"] = '{\
        "status": "new", \
        "run": "tendrl.gluster_integration.flows.start_volume.StartVolume", \
        "parameters":{ \
        "Config.file_path":"/temp/", "log": [], \
        "Package.state": "installed", "Node.cmd_str": "tendrl", "fqdn": "", \
        "Tendrl_context.cluster_id": "", "Package.pkg_type" : "yum",\
        "Tendrl_context.sds_version": "3.8.3", "Config.data": "",\
        "Package.name": "tendrl-gluster-integration", \
        "Tendrl_context.sds_name": "gluster", "Node[]":[], \
        "etcd_client": ""}, "parent":"",\
        "node_id": "0a9b801e-8e2e-4cef-8ceb-ad16f8b440c5", \
        "cluster_id": "c1367d08-6d44-4645-b101-bb5a666c44db", \
        "request_id": "0a9b801e-8e2e-4cef-8ceb-ad16f8b440c5", \
        "type": "sds"}'
        self.value = result['node']['value']
        self.key = result['node']['key']
        self.modifiedIndex = result['node']['modifiedIndex']
        self.createdIndex = result['node']['createdIndex']
        self.action = result['action']
