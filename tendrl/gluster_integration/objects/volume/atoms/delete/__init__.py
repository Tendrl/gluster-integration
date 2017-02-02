import subprocess

from tendrl.gluster_integration import objects
from tendrl.gluster_integration.objects.volume import Volume


class Delete(objects.GlusterIntegrationBaseAtom):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(Delete, self).__init__(*args, **kwargs)

    def run(self):
        cluster_id = self.parameters['TendrlContext.cluster_id']
        vol_id = self.parameters['Volume.vol_id']
        subprocess.call(
            [
                'gluster',
                'volume',
                'stop',
                self.parameters.get('Volume.volname'),
                '--mode=script'
            ]
        )
        subprocess.call(
            [
                'gluster',
                'volume',
                'delete',
                self.parameters.get('Volume.volname'),
                '--mode=script'
            ]
        )
        volume = tendrl_ns.gluster_integration.objects.Volume(
            cluster_id=cluster_id,
            vol_id=vol_id,
            deleted="True"
        )
        volume.save(tendrl_ns.etcd_orm)
        return True

