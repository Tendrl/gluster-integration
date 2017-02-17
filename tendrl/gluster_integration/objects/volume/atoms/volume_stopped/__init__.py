from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.gluster_integration import objects
from tendrl.gluster_integration.objects.volume import Volume


class VolumeStopped(objects.GlusterIntegrationBaseAtom):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(VolumeStopped, self).__init__(*args, **kwargs)

    def run(self):
        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Checking if volume %s stopped" %
                    self.parameters['Volume.volname']
                },
                request_id=self.parameters["request_id"],
                flow_id=self.parameters["flow_id"],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        return True
