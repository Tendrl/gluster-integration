from tendrl.gluster_integration.objects import geo_replication_session
from tendrl.gluster_integration.tests.test_init import init


def test_geo_replication_session():
    init()
    obj = geo_replication_session.GeoReplicationSession(
        vol_id="58b1283f-fde6-4abf-8d57-b17bb22f0922",
        session_id="123",
        session_status="up",
        pair="testing"
    )
    obj.render()
    result = 'clusters/77deef29-b8e5-4dc5-8247-21e2a409a66a' + \
        '/Volumes/58b1283f-fde6-4abf-8d57-b17bb22f0922/' + \
        'GeoRepSessions/123'
    if obj.value != result:
        raise AssertionError(obj.value)
