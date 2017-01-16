import os
from tendrl.gluster_integration.manager import utils
import uuid


class TestManagerUtils(object):
    def test_get_tendrl_context_positive(self, monkeypatch):
        DUMMY_CLUSTER_ID_FILE = "/tmp/sample_cluster_id"
        monkeypatch.setattr(utils, "TENDRL_CONTEXT", DUMMY_CLUSTER_ID_FILE)

        c_id = str(uuid.uuid4())
        with open(DUMMY_CLUSTER_ID_FILE, "w") as f:
            f.write(c_id)

        cluster_id = utils.get_tendrl_context()

        os.remove(DUMMY_CLUSTER_ID_FILE)
        assert cluster_id == c_id

    def test_get_tendrl_context_negative(self, monkeypatch):
        DUMMY_CLUSTER_ID_FILE = "/tmp/random_file_that_does_not_exist"
        monkeypatch.setattr(utils, "TENDRL_CONTEXT", DUMMY_CLUSTER_ID_FILE)
        cluster_id = utils.get_tendrl_context()

        assert cluster_id is None
