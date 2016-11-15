from tendrl.common.etcdobj.etcdobj import EtcdObj
from tendrl.common.etcdobj import fields


class Peer(EtcdObj):
    """A table of the peers seen by the pull, lazily updated

    """
    __name__ = 'clusters/%s/Peers/%s'

    cluster_id = fields.StrField("cluster_id")
    state = fields.StrField("state")
    hostname = fields.StrField("hostname")
    peer_uuid = fields.StrField("peer_uuid")
    updated = fields.StrField("updated")

    def render(self):
        self.__name__ = self.__name__ % (self.cluster_id, self.peer_uuid)
        return super(Peer, self).render()


class Volume(EtcdObj):
    """A table of the volumes seen by the pull.

    """
    __name__ = 'clusters/%s/Volumes/%s'

    cluster_id = fields.StrField("cluster_id")
    vol_id = fields.StrField("vol_id")
    vol_type = fields.StrField("vol_type")
    name = fields.StrField("name")
    status = fields.StrField("status")
    brick_count = fields.StrField("brick_count")
    deleted = fields.StrField("deleted")

    def render(self):
        self.__name__ = self.__name__ % (self.cluster_id, self.vol_id)
        return super(Volume, self).render()


class Brick(EtcdObj):
    """A table of the volumes seen by the pull.

    """
    __name__ = 'clusters/%s/Volumes/%s/Bricks/%s'

    cluster_id = fields.StrField("cluster_id")
    vol_id = fields.StrField("vol_id")
    path = fields.StrField("path")
    hostname = fields.StrField("hostname")
    port = fields.StrField("port")
    status = fields.StrField("status")
    filesystem_type = fields.StrField("fs_type")
    mount_opts = fields.StrField("mount_opts")

    def render(self):
        self.__name__ = self.__name__ % (
            self.cluster_id,
            self.vol_id,
            self.path.replace("/", "_")
        )
        return super(Brick, self).render()
