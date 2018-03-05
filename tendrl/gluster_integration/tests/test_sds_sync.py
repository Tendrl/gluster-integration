import etcd
import importlib
import maps
import mock
from mock import MagicMock
from mock import patch
import os

from tendrl.commons.objects import BaseObject
from tendrl.commons.objects import node_context
from tendrl.commons.utils import etcd_utils
from tendrl.commons.utils import event_utils
from tendrl.gluster_integration import ini2json
from tendrl.gluster_integration.sds_sync import brick_device_details
from tendrl.gluster_integration.sds_sync import brick_utilization
from tendrl.gluster_integration.tests.test_init import init


def read(param):
    if "Volumes/3c4b48cc-1a61-4c64-90d6-eba840c00081/status" in param:
        return maps.NamedDict(value="Stopped")
    elif "alert_counters" in param:
        raise etcd.EtcdKeyNotFound
    elif "Networks" in param:
        raise etcd.EtcdKeyNotFound
    elif "Bricks" in param and "status" in param:
        return maps.NamedDict(value="Stopped")


@mock.patch("tendrl.gluster_integration.sds_sync.blivet")
@patch.object(BaseObject, "load")
@patch.object(BaseObject, "save")
@patch.object(BaseObject, "hash_compare_with_central_store")
@patch.object(event_utils, "emit_event")
@patch.object(etcd_utils, "refresh")
def test_sync_volumes(refresh, emit_event, compare, save, load, blivet):
    init()
    refresh.return_value = True
    compare.return_value = True
    save.return_value = True
    emit_event.return_value = True
    NS.node_context = node_context.NodeContext
    obj = node_context.NodeContext(
        node_id="eeebe9f5-6e43-4cf8-b321-37d648eb0510",
        fqdn="dhcp12-12.lab.abc.com",
        tags=["provisioner/%s" % NS.tendrl_context.integration_id],
        ipv4_addr="127.0.0.1"
    )
    NS.node_context = obj
    load.return_value = obj
    sds_sync = importlib.import_module(
        'tendrl.gluster_integration.sds_sync'
    )
    raw_data = ini2json.ini_to_dict(
        os.path.join(os.path.dirname(__file__),
                     "gluster-state.yaml")
    )
    raw_data_options = ini2json.ini_to_dict(
        os.path.join(os.path.dirname(__file__),
                     "gluster-volume-option.yaml")
    )
    sds_sync.Event = MagicMock()
    sds_sync.Message = MagicMock()
    with patch.object(NS._int.client, "read", read):
        with patch.object(
            brick_device_details,
            "update_brick_device_details"
        ) as update:
            update.return_value = True
            with patch.object(
                brick_utilization,
                "brick_utilization"
            ) as utilization:
                utilization.return_value = 10
                sds_sync.sync_volumes(
                    raw_data['Volumes'],
                    1,
                    raw_data_options.get('Volume Options'),
                    10
                )


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
    obj = NS.gluster.objects.Brick(
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
                    'Status of brick: /gluster/b1 under '
                    'volume v1 in cluster '
                    '77deef29-b8e5-4dc5-8247-21e2a409a66a '
                    'changed from Started to Stopped',
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
