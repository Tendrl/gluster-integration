from tendrl.gluster_integration import flows
from tendrl.gluster_integration.objects.volume import Volume


class DeleteVolume(flows.GlusterIntegrationBaseFlow):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(DeleteVolume, self).__init__(*args, **kwargs)

    def run(self):
        super(DeleteVolume, self).run()
