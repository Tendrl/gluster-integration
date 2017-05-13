from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects
from tendrl.gluster_integration.objects.gluster_brick import GlusterBrick


class Create(objects.BaseAtom):
    obj = GlusterBrick
    def __init__(self, *args, **kwargs):
        super(Create, self).__init__(*args, **kwargs)

    def run(self):
        bricks = self.parameters.get('Cluster.node_configuration')
        brick_dict = {}
        brick_prefix = NS.config.data.get('gluster_bricks_dir', "/tendrl_gluster_bricks")
        for k, v in bricks.iteritems():
            key = "nodes/%s/NodeContext/fqdn" % k
            host = NS._int.client.read(key).value
            brick_dict[host] = {}
            for dev_name, details in v.iteritems():
                mount_path = brick_prefix + "/" + details["brick_name"] + "_mount"
                brick_path = mount_path + "/" + details["brick_name"]
                brick_dict[host].update({
                    dev_name: {
                        "node_id": k,
                        "mount_path": mount_path,
                        "brick_path": brick_path,
                        "lv": "tendrl" + brick_path.replace("/", "_") + "_lv",
                        "pv": "tendrl" + brick_path.replace("/", "_") + "_pv",
                        "pool": "tendrl" + brick_path.replace("/", "_") + "_pool",
                        "vg": "tendrl" + brick_path.replace("/", "_") + "_vg",
                    }
                })
        
        args = {}
        if self.parameters.get('GlusterBrick.disk_type') is not None:
            disk_type = self.parameters.get('GlusterBrick.disk_type')
            args.update({"disk_type": disk_type})
        if self.parameters.get('GlusterBrick.disk_count') is not None:
            disk_count = self.parameters.get('GlusterBrick.disk_count')
            args.update({"disk_count": disk_count})
        if self.parameters.get('GlusterBrick.stripe_size') is not None:
            stripe_size = self.parameters.get('GlusterBrick.stripe_size')
            args.update({"stripe_size": stripe_size})

        Event(
            Message(
                priority="info",
                publisher=NS.publisher_id,
                payload={
                    "message": "Creating the gluster bricks"
                },
                job_id=self.parameters["job_id"],
                flow_id=self.parameters["flow_id"],
                cluster_id=NS.tendrl_context.integration_id,
            )
        )

        if NS.gdeploy_plugin.gluster_provision_bricks(
                brick_dict,
                **args
        ):
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Created the gluster bricks successfully"
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )

            for k, v in brick_dict.iteritems():
                for key, val in v.iteritems():
                    brick_name = k + ":" + val["brick_path"].replace("/", "_")
                    NS.gluster.objects.GlusterBrick(
                        brick_name,
                        key,
                        val["brick_path"],
                        val["mount_path"],
                        val["node_id"],
                        lv=val["lv"],
                        vg=val["vg"],
                        pool=val["pool"],
                        pv=val["pv"],
                        **args
                    ).save(update=False)

            return True
        else:
            Event(
                Message(
                    priority="error",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "brick creation failed"
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False
