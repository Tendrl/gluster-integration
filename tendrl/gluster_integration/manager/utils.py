import logging
import os
import os.path
import subprocess

LOG = logging.getLogger(__name__)
TENDRL_CONTEXT = "/etc/tendrl/gluster-integration/tendrl_context"
NODE_CONTEXT = "/etc/tendrl/node_agent/node_context"


def get_tendrl_context():
    if os.path.isfile(TENDRL_CONTEXT):
        with open(TENDRL_CONTEXT) as f:
            cluster_id = f.read()
            LOG.info("Tendrl_context.cluster_id=%s found!" % cluster_id)
            return cluster_id
    else:
        return None


def get_sds_version():
    res = subprocess.check_output(['gluster', '--version'])
    return res.split()[1]
