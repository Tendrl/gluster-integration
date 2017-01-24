from tendrl.gluster_integration import objects
from tendrl.gluster_integration.objects.volume import Volume


class VolumeNotExists(objects.GlusterIntegrationBaseAtom):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(VolumeNotexists, self).__init__(*args, **kwargs)

    def run(self):
        return True

