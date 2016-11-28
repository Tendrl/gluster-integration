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
sys.modules['tendrl.gluster_integration.persistence.servers'] = MagicMock()
sys.modules['tendrl.gluster_integration.config'] = MagicMock()
sys.modules['tendrl.gluster_integration.manager.rpc'] = MagicMock()
sys.modules['tendrl.gluster_integration.persistence.persister'] = MagicMock()
sys.modules['logging'] = MagicMock()
from tendrl.gluster_integration.manager import manager
del sys.modules['tendrl.gluster_integration.manager.rpc']
del sys.modules['tendrl.gluster_integration.persistence.persister']
del sys.modules['logging']
del sys.modules['tendrl.gluster_integration.config']
del sys.modules['tendrl.common']
del sys.modules['tendrl.gluster_integration.persistence.servers']


class TestGluster_integration(object):
    def setup_method(self, method):
        manager.gevent.sleep = MagicMock()
        manager.Peer = MagicMock()
        manager.Brick = MagicMock()
        manager.Volume = MagicMock()
        manager.log = MagicMock()
        self.managerobj = manager.Manager()
        self.Manager = manager
        self.tempdir = tempfile.mkdtemp()

    def teardown_method(self, method):
        shutil.rmtree(self.tempdir)

    def _makeFile(self, filename, text):
        filename = os.path.join(self.tempdir, filename)
        f = open(filename, 'w')
        f.write(text)
        return filename
