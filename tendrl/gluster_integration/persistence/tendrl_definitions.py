from tendrl.common.etcdobj.etcdobj import EtcdObj
from tendrl.common.etcdobj import fields


class TendrlDefinitions(EtcdObj):
    """A table of the Os, lazily updated

    """
    # TODO(rohan) add the definitions in etcd at startup
    __name__ = '/clusters/%s/tendrl_definitions_gluster'

    data = fields.StrField("data")
    cluster_id = fields.StrField("cluster_id")

    def render(self):
        self.__name__ = self.__name__ % self.cluster_id
        return super(TendrlDefinitions, self).render()
