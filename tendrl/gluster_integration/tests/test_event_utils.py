import maps
import mock

from tendrl.commons.utils import log_utils
from tendrl.gluster_integration.tests.test_init import init


@mock.patch(
    'tendrl.commons.utils.log_utils.log',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.gluster_integration.sds_sync.__init__',
    mock.Mock(return_value=None)
)
def test_emit_event_with_volume_resource():
    init()
    setattr(NS, "tendrl_context", maps.NamedDict())
    NS.tendrl_context["integration_id"] = "int-id"
    NS.tendrl_context["cluster_name"] = "cluster1"
    NS.tendrl_context["sds_name"] = "gluster"
    NS.publisher_id = "gluster-integration"
    setattr(NS, "node_context", maps.NamedDict())
    NS.node_context["node_id"] = "node-id"
    NS.node_context["fqdn"] = "fqdn"

    from tendrl.gluster_integration.sds_sync import event_utils
    event_utils.emit_event(
        "volume_status",
        "stopped",
        "Status of vol1 changed to stopped from started",
        "volume_vol1",
        "WARNING",
        tags={"entity_type": "volume", "volume_name": "vol1"}
    )

    with mock.patch.object(log_utils, 'log') as logger:
        logger.assert_called


@mock.patch(
    'tendrl.commons.utils.log_utils.log',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.gluster_integration.sds_sync.__init__',
    mock.Mock(return_value=None)
)
def test_emit_event_with_brick_resource():
    init()
    setattr(NS, "tendrl_context", maps.NamedDict())
    NS.tendrl_context["integration_id"] = "int-id"
    NS.tendrl_context["cluster_name"] = "cluster1"
    NS.tendrl_context["sds_name"] = "gluster"
    NS.publisher_id = "gluster-integration"
    setattr(NS, "node_context", maps.NamedDict())
    NS.node_context["node_id"] = "node-id"
    NS.node_context["fqdn"] = "fqdn"

    from tendrl.gluster_integration.sds_sync import event_utils
    event_utils.emit_event(
        "brick_status",
        "stopped",
        "Status of brick1 of vol1 changed to stopped from started",
        "volume_vol1|brick_path1",
        "WARNING",
        tags={"entity_type": "brick", "volume_name": "vol1"}
    )

    with mock.patch.object(log_utils, 'log') as logger:
        logger.assert_called
