from tendrl.commons.etcdobj import EtcdObj
from tendrl.gluster_integration import objects


class Utilization(objects.GlusterIntegrationBaseObject):
    def __init__(self, raw_capacity=None, usable_capacity=None,
                 used_capacity=None, pcnt_used=None, *args, **kwargs):
        super(Utilization, self).__init__(*args, **kwargs)

        self.value = 'clusters/%s/Utilization'
        self.raw_capacity = raw_capacity
        self.usable_capacity = usable_capacity
        self.used_capacity = used_capacity
        self.pcnt_used = pcnt_used
        self._etcd_cls = _Utilization


class _Utilization(EtcdObj):
    """A table of the Utilization, lazily updated
    """
    __name__ = 'clusters/%s/Utilization'
    _tendrl_cls = Utilization

    def render(self):
        self.__name__ = self.__name__ %tendrl_ns.tendrl_context.integration_id
        return super(_Utilization, self).render()
