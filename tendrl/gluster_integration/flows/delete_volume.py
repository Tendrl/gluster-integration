from tendrl.gluster_integration.flows.flow import Flow


class DeleteVolume(Flow):
    def run(self):
        super(DeleteVolume, self).run()
