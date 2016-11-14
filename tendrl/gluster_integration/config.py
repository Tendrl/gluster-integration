import ConfigParser
import logging
import os


LOG = logging.getLogger(__name__)


class ConfigNotFound(Exception):
    pass


DEFAULT_CONFIG_PATH = "/etc/tendrl/tendrl.conf"
CONFIG_PATH_VAR = "TENDRL_CONFIG"


class TendrlConfig(ConfigParser.SafeConfigParser):
    def __init__(self):
        ConfigParser.SafeConfigParser.__init__(self)

        try:
            self.path = os.environ[CONFIG_PATH_VAR]
        except KeyError:
            self.path = DEFAULT_CONFIG_PATH

        if not os.path.exists(self.path):
            err = ConfigNotFound("Tendrl Gluster Bridge Configuration not "
                                 "found at "
                                 "%s" % self.path)
            LOG.error(err, exc_info=True)
            raise err

        self.read(self.path)
