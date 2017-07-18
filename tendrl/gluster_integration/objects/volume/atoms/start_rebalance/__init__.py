from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects


class StartRebalance(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(StartRebalance, self).__init__(*args, **kwargs)

    def run(self):
        if NS.gdeploy_plugin.rebalance_volume(
                self.parameters.get('Volume.volname'),
                "start",
                force=self.parameters.get('Volume.force'),
                fix_layout=self.parameters.get('Volume.fix_layout')
        ):
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Started the rebalance for volume %s" %
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
                        "message": "Failed to start rebalance for volume %s" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False

        return True
