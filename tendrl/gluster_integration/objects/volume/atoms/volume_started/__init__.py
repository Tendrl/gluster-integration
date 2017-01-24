from tendrl.gluster_integration import objects
from tendrl.gluster_integration.objects.volume import Volume


class VolumeStarted(objects.GlusterIntegrationBaseAtom):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(VolumeStarted, self).__init__(*args, **kwargs)

    def run(self):
        return True

