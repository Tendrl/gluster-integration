import logging

from tendrl.gluster_bridge.common.config import tendrlConfig
config = tendrlConfig()


FORMAT = "%(asctime)s - %(levelname)s - %(name)s %(message)s"
log = logging.getLogger('gluster_bridge')
handler = logging.FileHandler(config.get('bridge', 'log_path'))
handler.setFormatter(logging.Formatter(FORMAT))
log.addHandler(handler)
log.setLevel(logging.getLevelName(config.get('bridge', 'log_level')))
