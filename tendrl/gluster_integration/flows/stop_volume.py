from tendrl.gluster_integration.flows.flow import Flow


class StopVolume(Flow):
    def run(self):
        super(StopVolume, self).run()
