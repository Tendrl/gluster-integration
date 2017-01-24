import logging
import os

from tendrl.commons.etcdobj import EtcdObj
from tendrl.gluster_integration import objects

LOG = logging.getLogger(__name__)


class TendrlContext(objects.GlusterIntegrationBaseObject):
    def __init__(self, integration_id=None, *args, **kwargs):
        super(TendrlContext, self).__init__(*args, **kwargs)

        self.value = 'clusters/%s/TendrlContext'

        # integration_id is the Tendrl generated cluster UUID
        self.integration_id = integration_id or self._get_local_integration_id()
        self._etcd_cls = _TendrlContextEtcd

    def create_local_integration_id(self):
        tendrl_context_path = "/etc/tendrl/gluster-integration/integration_id"
        with open(tendrl_context_path, 'wb+') as f:
            f.write(self.integration_id)
            LOG.info("SET_LOCAL: "
                     "tendrl_ns.gluster_integration.objects.TendrlContext.integration_id"
                     "==%s" %
                     self.integration_id)

    def _get_local_integration_id(self):
        try:
            tendrl_context_path = "/etc/tendrl/gluster-integration/integration_id"
            if os.path.isfile(tendrl_context_path):
                with open(tendrl_context_path) as f:
                    integration_id = f.read()
                    if integration_id:
                        LOG.info(
                            "GET_LOCAL: "
                            "tendrl_ns.gluster_integration.objects.TendrlContext"
                            ".integration_id==%s" % integration_id)
                        return integration_id
        except AttributeError:
            return None


class _TendrlContextEtcd(EtcdObj):
    """A table of the node context, lazily updated
    """
    __name__ = 'clusters/%s/TendrlContext'
    _tendrl_cls = TendrlContext

    def render(self):
        self.__name__ = self.__name__ % self.integration_id
        return super(_TendrlContextEtcd, self).render()
