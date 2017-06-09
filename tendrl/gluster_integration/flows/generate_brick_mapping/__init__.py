from tendrl.commons import flows
from tendrl.commons.event import Event
from tendrl.commons.message import Message

# This flow will be invoked only after cluster is available
# in the tendrl (either by creation/import)
class GenerateBrickMapping(flows.BaseFlow):
    def run(self):
        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Starting flow for brick mapping generation"
                },
                job_id=self.job_id,
                flow_id=self.parameters['flow_id'],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        super(GenerateBrickMapping, self).run()
