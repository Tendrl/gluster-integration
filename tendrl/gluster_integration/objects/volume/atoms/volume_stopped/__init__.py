from tendrl.gluster_integration import objects
from tendrl.gluster_integration.objects.volume import Volume


class VolumeStopped(objects.GlusterIntegrationBaseAtom):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(VolumeStopped, self).__init__(*args, **kwargs)

    def run(self):
        return True

