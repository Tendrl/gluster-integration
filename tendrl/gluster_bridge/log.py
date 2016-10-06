import logging

from tendrl.gluster_bridge.config import TendrlConfig
config = TendrlConfig()


FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
root = logging.getLogger()
handler = logging.FileHandler(config.get('gluster_bridge', 'log_path'))
handler.setFormatter(logging.Formatter(FORMAT))
root.addHandler(handler)
root.setLevel(logging.getLevelName(config.get('gluster_bridge', 'log_level')))
