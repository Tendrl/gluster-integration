from mock import patch

from tendrl.commons.objects import BaseObject
from tendrl.commons.utils import event_utils
from tendrl.gluster_integration.message import process_events
from tendrl.gluster_integration.tests.test_init import init


@patch.object(BaseObject, "load_all")
@patch.object(BaseObject, "save")
def test_process_events(save, load_all):
    init()
    save.return_value = True
    obj = NS.gluster.objects.NativeEvents(
        'svc_reconfigure_failed|testingv1',
        alert_notify=True,
        current_value='svc_reconfigure_failed',
        message='Service reconfigure failed for service: test',
        severity='warning',
    )
    load_all.return_value = [obj]
    with patch.object(event_utils, "emit_event") as emit_event:
        process_events.process_events()
        emit_event.assert_called_with(
            'svc_reconfigure_failed',
            'svc_reconfigure_failed',
            'Service reconfigure failed for service: test',
            'svc_reconfigure_failed|testingv1',
            'WARNING',
            alert_notify=True,
            tags={}
        )
    obj = NS.gluster.objects.NativeEvents(
        'quorum|v1',
        current_value='quorum_gained',
        message='Quorum of volume: v1 is regained in cluster '
                '77deef29-b8e5-4dc5-8247-21e2a409a66a',
        severity='recovery',
        tags={'volume_name': 'v1',
              'entity_type': 'volume'
              }
    )
    load_all.return_value = [obj]
    with patch.object(event_utils, "emit_event") as emit_event:
        process_events.process_events()
        emit_event.assert_called_with(
            'quorum',
            'quorum_gained',
            'Quorum of volume: v1 is regained in cluster '
            '77deef29-b8e5-4dc5-8247-21e2a409a66a',
            'quorum|v1',
            'INFO',
            tags={'entity_type': 'volume', 'volume_name': 'v1'}
        )
