from etcdobj import EtcdObj
from etcdobj import fields


class SyncObject(EtcdObj):
    """A table for storing a FIFO of ClusterMonitor 'sync objects', i.e.

    cluster maps.

    """
    __name__ = 'gluster/raw_map'

    data = fields.StrField("data")
    updated = fields.StrField("updated")
