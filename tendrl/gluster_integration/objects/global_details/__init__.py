from tendrl.commons.etcdobj import EtcdObj
from tendrl.commons import objects


class GlobalDetails(objects.BaseObject):
    def __init__(self, status=None, connection_count=None,
                 connection_active=None, volume_up_degraded=None,
                 *args, **kwargs):
        super(GlobalDetails, self).__init__(*args, **kwargs)

        self.value = 'clusters/%s/GlobalDetails'
        self.status = status
        self.connection_count = connection_count
        self.connection_active = connection_active
        self.volume_up_degraded = volume_up_degraded
        self._etcd_cls = _GlobalDetails


class _GlobalDetails(EtcdObj):
    __name__ = 'clusters/%s/GlobalDetails'
    _tendrl_cls = GlobalDetails

    def render(self):
        self.__name__ = self.__name__ %\
            NS.tendrl_context.integration_id
        return super(_GlobalDetails, self).render()
