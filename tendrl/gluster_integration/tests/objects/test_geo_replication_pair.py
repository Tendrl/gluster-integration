from tendrl.gluster_integration.objects.geo_replication_pair import \
    GeoReplicationPair
from tendrl.gluster_integration.tests.test_init import init


def test_geo_replication_pair():
    init()
    obj = GeoReplicationPair(
        vol_id="58b1283f-fde6-4abf-8d57-b17bb22f0922",
        session_id="123",
        pair="testing"
    )
    obj.render()
    result = 'clusters/77deef29-b8e5-4dc5-8247-21e2a409a66a' + \
        '/Volumes/58b1283f-fde6-4abf-8d57-b17bb22f0922/' + \
        'GeoRepSessions/123/pairs/testing'
    if obj.value != result:
        raise AssertionError(obj.value)
