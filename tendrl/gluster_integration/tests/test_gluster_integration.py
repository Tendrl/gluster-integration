"""
test_gluster_integration
----------------------------------

Tests for `gluster_integration` module.
"""
from mock import MagicMock
import os
import shutil
import sys
import tempfile
sys.modules['tendrl.common'] = MagicMock()
sys.modules[
    'tendrl.gluster_integration.persistence.tendrl_definitions'] = MagicMock()
sys.modules['tendrl.gluster_integration.persistence.servers'] = MagicMock()
sys.modules['tendrl.gluster_integration.config'] = MagicMock()
sys.modules['tendrl.gluster_integration.manager.rpc'] = MagicMock()
sys.modules['tendrl.gluster_integration.persistence.persister'] = MagicMock()
sys.modules[
    'tendrl.gluster_integration.persistence.tendrl_context'] = MagicMock()
sys.modules['logging'] = MagicMock()
from tendrl.gluster_integration.manager import manager
del sys.modules['logging']
del sys.modules['tendrl.gluster_integration.persistence.tendrl_context']
del sys.modules['tendrl.gluster_integration.manager.rpc']
del sys.modules['tendrl.gluster_integration.persistence.persister']
del sys.modules['tendrl.gluster_integration.config']
del sys.modules['tendrl.gluster_integration.persistence.servers']
del sys.modules['tendrl.gluster_integration.persistence.tendrl_definitions']
del sys.modules['tendrl.common']


class TestGluster_integration(object):
    def setup_method(self, method):
        manager.gevent.sleep = MagicMock()
        manager.Peer = MagicMock()
        manager.Brick = MagicMock()
        manager.Volume = MagicMock()
        manager.log = MagicMock()
        manager.utils.get_sds_version = MagicMock(return_value=0.1)
        self.clusterid = "e859cb15-2851-43d1-896c-1d9e845c0721"
        self.managerobj = manager.Manager(self.clusterid)
        self.Manager = manager
        self.tempdir = tempfile.mkdtemp()

    def teardown_method(self, method):
        shutil.rmtree(self.tempdir)

    def _makeFile(self, filename, text):
        filename = os.path.join(self.tempdir, filename)
        f = open(filename, 'w')
        f.write(text)
        return filename
