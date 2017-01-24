import gevent.event

from tendrl.commons import manager as common_manager
from tendrl.gluster_integration.sds_sync import GlusterIntegrationSdsSyncStateThread
from tendrl.gluster_integration.objects.tendrl_context import TendrlContext

from tendrl.gluster_integration import central_store


class GlusterIntegrationManager(common_manager.Manager):
    def __init__(self):
        self._complete = gevent.event.Event()
        super(
            GlusterIntegrationManager,
            self
        ).__init__(
            tendrl_ns.state_sync_thread,
            tendrl_ns.central_store_thread
        )
        self.register_to_cluster(tendrl_ns.tendrl_context.integration_id)

    def register_to_cluster(self, cluster_id):
        tendrl_ns.tendrl_context = tendrl_ns.gluster_integration.objects.TendrlContext()

        tendrl_ns.tendrl_context.save()

