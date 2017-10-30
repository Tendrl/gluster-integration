from tendrl.commons import flows
from tendrl.commons.utils import log_utils as logger


class UpdateBrickStatus(flows.BaseFlow):
    def run(self):
        logger.log(
            "info",
            NS.publisher_id,
            {"message": "starting flow for updating brick status"}
        )
        super(UpdateBrickStatus, self).run()
        node = self.parameters.get("Node.fqdn")
        cluster_id = self.parameters.get("TendrlContext.integration_id")
        status = self.parameters.get("Brick.status")
        self.update_brick_status(node, cluster_id, status)

    def update_brick_status(self, node, cluster_id, status):
        bricks = NS.gluster.objects.Brick(fqdn=node).load_all()
        for brick in bricks:
            brick.status = status
            brick.save()
        return
