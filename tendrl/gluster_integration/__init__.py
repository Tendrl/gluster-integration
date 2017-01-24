# flake8: noqa
__version__ = '1.2'
try:
    from gevent import monkey
except ImportError:
    pass
else:
    monkey.patch_all()

from tendrl.commons import CommonNS
from tendrl.commons import etcdobj
from tendrl.commons import log

from tendrl.gluster_integration.objects.brick import Brick
from tendrl.gluster_integration.objects.config import Config
from tendrl.gluster_integration.objects.definition import Definition
from tendrl.gluster_integration.objects.peer import Peer
from tendrl.gluster_integration.objects.sync_object import SyncObject
from tendrl.gluster_integration.objects.tendrl_context import TendrlContext
from tendrl.gluster_integration.objects.volume import Volume
from tendrl.gluster_integration.objects.volume_options import VolumeOptions

from tendrl.gluster_integration.objects.volume.atoms.create import Create
from tendrl.gluster_integration.objects.volume.atoms.delete import Delete
from tendrl.gluster_integration.objects.volume.atoms.start import Start
from tendrl.gluster_integration.objects.volume.atoms.stop import Stop
from tendrl.gluster_integration.objects.volume.atoms.volume_exists \
    import VolumeExists
from tendrl.gluster_integration.objects.volume.atoms.volume_not_exists \
    import VolumeNotExists
from tendrl.gluster_integration.objects.volume.atoms.volume_started \
    import VolumeStarted
from tendrl.gluster_integration.objects.volume.atoms.volume_stopped \
    import VolumeStopped

from tendrl.gluster_integration.objects.volume.flows.delete_volume \
    import DeleteVolume
from tendrl.gluster_integration.objects.volume.flows.start_volume \
    import StartVolume
from tendrl.gluster_integration.objects.volume.flows.stop_volume \
    import StopVolume


class GlusterIntegrationNS(CommonNS):
    def __init__(self):

        # Create the "tendrl_ns.gluster_integration" namespace
        self.to_str = "tendrl.gluster_integration"
        self.type = 'sds'
        super(GlusterIntegrationNS, self).__init__()

    def setup_initial_objects(self):
        # Definitions
        tendrl_ns.definitions = tendrl_ns.gluster_integration.\
            objects.Definition()

        # Config
        tendrl_ns.config = tendrl_ns.gluster_integration.objects.Config()

        # etcd_orm
        etcd_kwargs = {
            'port': tendrl_ns.config.data['etcd_port'],
            'host': tendrl_ns.config.data["etcd_connection"]
        }
        tendrl_ns.etcd_orm = etcdobj.Server(etcd_kwargs=etcd_kwargs)

        tendrl_ns.tendrl_context = tendrl_ns.gluster_integration.\
            objects.TendrlContext()

        log.setup_logging(
            tendrl_ns.config.data['log_cfg_path'],
        )

import __builtin__
__builtin__.tendrl_ns = GlusterIntegrationNS()
