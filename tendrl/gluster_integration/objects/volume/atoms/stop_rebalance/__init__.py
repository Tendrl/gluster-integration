import subprocess

from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.gluster_integration import objects
from tendrl.gluster_integration.objects.volume import Volume


class StopRebalance(objects.BaseAtom):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(StopRebalance, self).__init__(*args, **kwargs)

    def run(self):
        if NS.gdeploy_plugin.rebalance_volume(
                self.parameters.get('Volume.volname'),
                "stop",
                force=self.parameters['Volume.force'],
                fix_layout=self.parameters['Volume.fix_layout']
        ):
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Stopped the rebalance for volume %s" %
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
                        "message": "Failed to stop rebalance for volume %s" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False

        return True
