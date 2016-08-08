
from tendrl.gluster_bridge.common.salt_wrapper import client_config
from tendrl.gluster_bridge.common.config import tendrlConfig

# A config instance for use from within the manager service
config = tendrlConfig()

# A salt config instance for places we'll need the sock_dir
salt_config = client_config(config.get('bridge', 'salt_config_path'))
