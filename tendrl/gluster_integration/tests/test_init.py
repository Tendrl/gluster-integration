import __builtin__
import etcd
from etcd import Client
import maps
import mock
from mock import patch


import tendrl.commons.objects.node_context as node
from tendrl.commons import TendrlNS


@patch.object(etcd, "Client")
@patch.object(Client, "read")
@patch.object(node.NodeContext, '_get_node_id')
def init(patch_get_node_id, patch_read, patch_client):
    patch_get_node_id.return_value = 1
    patch_read.return_value = etcd.Client()
    patch_client.return_value = etcd.Client()
    setattr(__builtin__, "NS", maps.NamedDict())
    setattr(NS, "_int", maps.NamedDict())
    NS._int.etcd_kwargs = {
        'port': 1,
        'host': 2,
        'allow_reconnect': True}
    NS._int.client = etcd.Client(**NS._int.etcd_kwargs)
    NS["config"] = maps.NamedDict()
    NS.config["data"] = maps.NamedDict()
    NS.config.data['tags'] = "test"
    NS.state_sync_thread = mock.MagicMock()
    NS.sds_sync_thread = mock.MagicMock()
    NS.message_handler_thread = mock.MagicMock()
    tendrlNS = TendrlNS()
    return tendrlNS
