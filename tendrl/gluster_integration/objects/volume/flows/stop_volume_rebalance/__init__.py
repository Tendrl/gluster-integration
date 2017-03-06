from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.gluster_integration import flows
from tendrl.gluster_integration.objects.volume import Volume


class StopVolumeRebalance(flows.BaseFlow):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(StopVolumeRebalance, self).__init__(*args, **kwargs)

    def run(self):
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Stopping rebalance for volume %s" %
                    self.parameters['Volume.volname']
                },
                request_id=self.parameters["request_id"],
                flow_id=self.parameters["flow_id"],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        super(StopVolumeRebalance, self).run()
