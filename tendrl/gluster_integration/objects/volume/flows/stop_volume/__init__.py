from tendrl.gluster_integration import flows
from tendrl.gluster_integration.objects.volume import Volume


class StopVolume(flows.GlusterIntegrationBaseFlow):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(StopVolume, self).__init__(*args, **kwargs)

    def run(self):
        super(StopVolume, self).run()

