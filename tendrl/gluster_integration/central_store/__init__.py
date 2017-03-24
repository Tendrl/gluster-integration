from tendrl.commons import central_store


class GlusterIntegrationEtcdCentralStore(central_store.EtcdCentralStore):
    def __init__(self):
        super(GlusterIntegrationEtcdCentralStore, self).__init__()

    def save_syncobject(self, sync_object):
        NS.etcd_orm.save(sync_object)

    def save_globaldetails(self, details):
        NS.etcd_orm.save(details)

    def save_config(self, config):
        NS.etcd_orm.save(config)

    def save_definition(self, definition):
        NS.etcd_orm.save(definition)

    def save_peer(self, peer):
        NS.etcd_orm.save(peer)

    def save_volume(self, vol):
        NS.etcd_orm.save(vol)

    def save_brick(self, brick):
        NS.etcd_orm.save(brick)

    def save_volumeoptions(self, vol_options):
        NS.etcd_orm.save(vol_options)

    def save_utilization(self, utilization):
        NS.etcd_orm.save(utilization)
