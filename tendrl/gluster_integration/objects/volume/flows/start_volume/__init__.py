from tendrl.gluster_integration import flows
from tendrl.gluster_integration.objects.volume import Volume


class StartVolume(flows.GlusterIntegrationBaseFlow):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(StartVolume, self).__init__(*args, **kwargs)

    def run(self):
        super(StartVolume, self).run()

