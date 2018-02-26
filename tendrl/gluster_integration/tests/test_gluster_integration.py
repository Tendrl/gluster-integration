# flake8: noqa

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

sys.modules['tendrl.gluster_integration.sds_sync.blivet'] = MagicMock()

from tendrl.gluster_integration import manager

del sys.modules['tendrl.gluster_integration.sds_sync.blivet']

from tendrl.gluster_integration.tests.test_init import init

class TestGluster_integration(object):
    @classmethod
    def setup_method(self, method):
        init()
        self.tempdir = tempfile.mkdtemp()

    @classmethod
    def teardown_method(self, method):
        shutil.rmtree(self.tempdir)

    def _makeFile(self, filename, text):
        filename = os.path.join(self.tempdir, filename)
        f = open(filename, 'w')
        f.write(text)
        return filename
