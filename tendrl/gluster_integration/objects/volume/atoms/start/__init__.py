import subprocess

from tendrl.gluster_integration import objects
from tendrl.gluster_integration.objects.volume import Volume


class Start(objects.GlusterIntegrationBaseAtom):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(Start, self).__init__(*args, **kwargs)

    def run(self):
        subprocess.call(
            [
                'gluster',
                'volume',
                'start',
                self.parameters.get('Volume.volname'),
                '--mode=script'
            ]
        )
        return True
