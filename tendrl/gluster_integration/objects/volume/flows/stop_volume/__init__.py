from tendrl.commons.event import Event
from tendrl.commons import flows
from tendrl.commons.message import Message


class StopVolume(flows.BaseFlow):
    def __init__(self, *args, **kwargs):
        super(StopVolume, self).__init__(*args, **kwargs)

    def run(self):
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Starting stop volume flow for volume %s" %
                    self.parameters['Volume.volname']
                },
                job_id=self.parameters["job_id"],
                flow_id=self.parameters["flow_id"],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        super(StopVolume, self).run()
