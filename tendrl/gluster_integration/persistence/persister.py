from tendrl.common.persistence.etcd_persister import EtcdPersister
from tendrl.common.persistence.file_persister import FilePersister

from tendrl.gluster_integration.persistence.sync_objects import SyncObject


class GlusterIntegrationEtcdPersister(EtcdPersister):
    def __init__(self, config):
        super(GlusterIntegrationEtcdPersister, self).__init__(config)
        self._store = self.get_store()

    def update_sync_object(self, updated, cluster_id, data):
        self._store.save(
            SyncObject(
                updated=updated,
                cluster_id=cluster_id,
                data=data
            )
        )

    def update_peer(self, peer):
        self._store.save(peer)

    def update_volume(self, vol):
        self._store.save(vol)

    def update_brick(self, brick):
        self._store.save(brick)

    def save_events(self, events):
        for event in events:
            self._store.save(event)

    def update_tendrl_context(self, context):
        self._store.save(context)

    def update_tendrl_definitions(self, definition):
        self._store.save(definition)


class GlusterIntegrationFilePersister(FilePersister):
    def __init__(self, config):
        super(GlusterIntegrationFilePersister, self).__init__(config)
        self._doc_location = "%s/gluster_integration" % \
            config.get("gluster_integration", "doc_persist_location")

    def update_sync_object(self, updated, cluster_id, data):
        obj = SyncObject(
            updated=updated,
            cluster_id=cluster_id,
            data=data
        )

        f = open(
            "%s/%s" % (self._doc_location, cluster_id),
            "w"
        )
        f.write(obj.json())
        f.close()

    def update_peer(self, peer):
        f = open(
            "%s/%s" % (self._doc_location, peer.__name__),
            "w"
        )
        f.write(peer.json())
        f.close()

    def update_volume(self, vol):
        f = open(
            "%s/%s" % (self._doc_location, vol.__name__),
            "w"
        )
        f.write(vol.json())
        f.close()

    def update_brick(self, brick):
        f = open(
            "%s/%s" % (self._doc_location, brick.__name__),
            "w"
        )
        f.write(brick.json())
        f.close()

    def save_events(self, events):
        for event in events:
            f = open(
                "%s/%s" % (self._doc_location, event.__name__),
                "w"
            )
            f.write(event.json())
            f.close()

    def update_tendrl_context(self, context):
        f = open(
            "%s/%s" % (self._doc_location, context.__name__),
            "w"
        )
        f.write(context.json())
        f.close()

    def update_tendrl_definitions(self, definition):
        f = open(
            "%s/%s" % (self._doc_location, definition.__name__),
            "w"
        )
        f.write(definition)
        f.close()
