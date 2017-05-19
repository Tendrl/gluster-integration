import subprocess

from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects
from tendrl.gluster_integration.objects.volume import Volume


class Create(objects.BaseAtom):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(Create, self).__init__(*args, **kwargs)

    def run(self):
        args = {}
        if self.parameters.get('Volume.replica_count') is not None:
            args.update({
                "replica_count": self.parameters.get('Volume.replica_count')
            })
        if self.parameters.get('Volume.transport') is not None:
            args.update({
                "transport": self.parameters.get('Volume.transport')
            })
        if self.parameters.get('Volume.disperse_count') is not None:
            args.update({
                "disperse_count": self.parameters.get('Volume.disperse_count')
            })
        if self.parameters.get('Volume.redundancy_count') is not None:
            args.update({
                "redundancy_count": self.parameters.get(
                    'Volume.redundancy_count'
                )
            })
        if self.parameters.get('Volume.tuned_profile') is not None:
            args.update({
                "tuned_profile": self.parameters.get('Volume.tuned_profile')
            })
        if self.parameters.get('Volume.force') is not None:
            args.update({
                "force": self.parameters.get('Volume.force')
            })

        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Creating the volume %s" %
                    self.parameters['Volume.volname']
                },
                job_id=self.parameters["job_id"],
                flow_id=self.parameters["flow_id"],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        if NS.gdeploy_plugin.create_volume(
                self.parameters.get('Volume.volname'),
                self.parameters.get('Volume.bricks'),
                **args
        ):
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Created the volume %s" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )

            # mark the bricks that were used to create this volume as
            # used bricks so that they are not consumed again
            for sub_vol in self.parameters.get('Volume.bricks'):
                for brick in sub_vol:
                    ip = brick.keys()[0]
                    brick_path = brick.values()[0]
                    node_id = NS._int.client.read("indexes/ip/%s" % ip).value
                    key = "nodes/%s/NodeContext/fqdn" % node_id
                    host = NS._int.client.read(key).value
                    brick_path = host + ":" + brick_path
                    NS._int.wclient.delete(
                        ("clusters/%s/nodes/%s/GlusterBricks/free/%s") % (
                            NS.tendrl_context.integration_id,
                            node_id,
                            brick_path.replace("/","_")
                        )
                    )
                    NS._int.wclient.write(
                        ("clusters/%s/nodes/%s/GlusterBricks/used/%s") % (
                            NS.tendrl_context.integration_id,
                            node_id,
                            brick_path.replace("/","_")
                        ),
                        ""
                    )
                    NS._int.wclient.write(
                        ("clusters/%s/nodes/%s/GlusterBricks/all/%s/volume_name") % (
                            NS.tendrl_context.integration_id,
                            node_id,
                            brick_path.replace("/","_")
                        ),
                        self.parameters['Volume.volname']
                    )
        else:
            Event(
                Message(
                    priority="error",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Volume creation failed for volume %s" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False
        return True
