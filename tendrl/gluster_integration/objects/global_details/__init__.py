from tendrl.commons.etcdobj import EtcdObj
from tendrl.gluster_integration import objects


class GlobalDetails(objects.GlusterIntegrationBaseObject):
    def __init__(self, status=None, *args, **kwargs):
        super(GlobalDetails, self).__init__(*args, **kwargs)

        self.value = 'clusters/%s/GlobalDetails'
        self.status = status
        self._etcd_cls = _GlobalDetails


class _GlobalDetails(EtcdObj):
    __name__ = 'clusters/%s/GlobalDetails'
    _tendrl_cls = GlobalDetails

    def render(self):
        self.__name__ = self.__name__ %\
            tendrl_ns.tendrl_context.integration_id
        return super(_GlobalDetails, self).render()
