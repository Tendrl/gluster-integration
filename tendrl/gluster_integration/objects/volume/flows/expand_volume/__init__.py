from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import flows
from tendrl.gluster_integration.objects.volume import Volume


class ExpandVolume(flows.BaseFlow):
    def __init__(self, *args, **kwargs):
        super(ExpandVolume, self).__init__(*args, **kwargs)

    def run(self):
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Starting Expansion flow for volume %s" %
                    self.parameters['Volume.volname']
                },
                job_id=self.parameters["job_id"],
                flow_id=self.parameters["flow_id"],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )
        super(ExpandVolume, self).run()
