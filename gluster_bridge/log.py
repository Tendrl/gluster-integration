from gluster_bridge.config import CONF
from oslo_log import log as logging

DOMAIN = "Tendrl"
logging.register_options(CONF)
logging_format = "%(asctime)s.%(msecs)03d %(process)d %(levelname)s" \
                 "%(pathname)s.%(name)s [-] %(instance)s%(message)s"

CONF.set_default("log_dir", default="/var/log/tendrl/")
CONF.set_default("log_file", default="tendrl_gluster_bridge.log")
CONF.set_default("logging_default_format_string",
                 default=logging_format)


logging.setup(CONF, DOMAIN)
LOG = logging.getLogger(__name__)
