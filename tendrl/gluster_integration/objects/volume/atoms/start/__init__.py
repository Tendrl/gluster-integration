from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects


class Start(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(Start, self).__init__(*args, **kwargs)

    def run(self):
        if NS.gdeploy_plugin.start_volume(
                self.parameters.get('Volume.volname')
        ):
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Started the volume %s successfully" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
        else:
            Event(
                Message(
                    priority="error",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Failed to start the volume %s" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False

        return True
