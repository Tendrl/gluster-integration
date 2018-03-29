import maps
import mock
import threading

from tendrl.gluster_integration import manager
from tendrl.gluster_integration.manager import \
    GlusterIntegrationManager
from tendrl.gluster_integration.objects.config import \
    Config
from tendrl.gluster_integration.objects.definition import \
    Definition


def test_constructor(monkeypatch):
    """Test for constructor involves if all the needed

    variables are initialized
    """

    manager = GlusterIntegrationManager()
    assert isinstance(manager._message_handler_thread, mock.MagicMock)
    assert isinstance(manager._sds_sync_thread, mock.MagicMock)


@mock.patch(
    'tendrl.gluster_integration.manager.GlusterIntegrationManager.start',
    mock.Mock()
)
@mock.patch(
    'tendrl.gluster_integration.manager.GlusterIntegrationManager.stop',
    mock.Mock()
)
@mock.patch(
    'threading.Event', mock.Mock(return_value=threading.Event())
)
@mock.patch(
    'tendrl.gluster_integration.GlusterIntegrationNS.__init__',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.commons.TendrlNS.__init__',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.commons.message.Message.__init__',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.commons.utils.log_utils.log',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.gluster_integration.objects.definition.Definition.save',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.gluster_integration.objects.config.Config.save',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.gluster_integration.objects.definition.Definition.__init__',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.gluster_integration.objects.config.Config.__init__',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.gluster_integration.sds_sync'
    '.GlusterIntegrationSdsSyncStateThread.__init__',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.gluster_integration.message'
    '.gluster_native_message_handler.GlusterNativeMessageHandler.__init__',
    mock.Mock(return_value=None)
)
@mock.patch(
    'tendrl.commons.jobs.JobConsumerThread.__init__',
    mock.Mock(return_value=None)
)
@mock.patch(
    'signal.signal', mock.Mock(return_value=None)
)
def test_main(monkeypatch):
    NS.tendrl_context = mock.MagicMock()
    NS.tendrl_context.integration_id = "int-id"
    NS.message_handler_thread = mock.MagicMock()

    defs = Definition()
    defs.data = mock.MagicMock()
    cfgs = Config()
    cfgs.data = {"with_internal_profiling": False}
    setattr(NS, "gluster", maps.NamedDict())
    NS.gluster.definitions = defs
    NS.gluster.config = cfgs

    t = threading.Thread(target=manager.main, kwargs={})
    t.start()
    t.join()

    assert NS.type == "sds"
    assert NS.publisher_id == "gluster_integration"
    assert NS.state_sync_thread is not None
    assert NS.message_handler_thread is not None

    with mock.patch.object(GlusterIntegrationManager, 'start') \
        as manager_start:
        manager_start.assert_called
    with mock.patch.object(Definition, 'save') as def_save:
        def_save.assert_called
    with mock.patch.object(Config, 'save') as conf_save:
        conf_save.assert_called
