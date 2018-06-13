import etcd
import importlib
from mock import MagicMock
from mock import patch

from tendrl.commons.objects import BaseObject
from tendrl.commons.utils import etcd_utils
from tendrl.commons.utils import event_utils


@patch.object(BaseObject, "save")
@patch.object(BaseObject, "load_all")
@patch.object(event_utils, "emit_event")
@patch.object(BaseObject, "hash_compare_with_central_store")
@patch.object(etcd_utils, "refresh")
def test_brick_status_alert(
    compare, refresh, emit_event, load_all, save
):
    compare.return_value = True
    refresh.return_value = True
    save.return_value = True
    obj = NS.tendrl.objects.GlusterBrick(
        integration_id="77deef29-b8e5-4dc5-8247-21e2a409a66a",
        fqdn="dhcp12-12.lab.abc.com",
        hostname="dhcp12-12.lab.abc.com",
        status="started",
        vol_name="v1",
        brick_path="/gluster/b1",
        node_id="3c4b48cc-1a61-4c64-90d6-eba840c00081"
    )
    load_all.return_value = [obj]
    sds_sync = importlib.import_module(
        'tendrl.gluster_integration.sds_sync'
    )
    sds_sync.Event = MagicMock()
    sds_sync.ExceptionMessage = MagicMock()
    with patch.object(
        etcd.Lock, 'acquire'
    ) as mock_acquire:
        mock_acquire.return_value = True
        with patch.object(
            etcd.Lock, 'is_acquired'
        ) as mock_is_acq:
            mock_is_acq.return_value = True
            with patch.object(
                etcd.Lock, 'release'
            ) as mock_rel:
                mock_rel.return_value = True
                sds_sync.brick_status_alert(
                    "dhcp12-12.lab.abc.com"
                )
                emit_event.assert_called_with(
                    'brick_status',
                    'Stopped',
                    'Brick:/gluster/b1 in '
                    'volume:v1 '
                    'has Stopped',
                    'volume_v1|brick_/gluster/b1',
                    'WARNING',
                    tags={'node_id': '3c4b48cc-1a61-4c64-90d6-eba840c00081',
                          'volume_name': 'v1',
                          'fqdn': 'dhcp12-12.lab.abc.com',
                          'entity_type': 'brick'
                          }
                )
    sds_sync.brick_status_alert(
        "dhcp12-12.lab.abc.com"
    )
