from oslo_log import log as logging
from gluster_bridge import config

LOG = logging.getLogger(__name__)

def setup_logging():
    logging.register_options(config.CONF)
    logging_format = "%(asctime)s.%(msecs)03d %(process)d %(levelname)s" \
                     "%(pathname)s.%(name)s [-] %(instance)s%(message)s"

    config.CONF.set_default("log_dir", default="/var/log/tendrl/")
    config.CONF.set_default("log_file", default="tendrl_gluster_bridge.log")
    config.CONF.set_default("logging_default_format_string",
                     default=logging_format)

