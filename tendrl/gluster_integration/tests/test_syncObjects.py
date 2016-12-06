from tendrl.gluster_integration.persistence.sync_objects import SyncObject


class TestSyncObject(object):

    def test_SyncObject(self):
        self.sync_object = SyncObject()
        self.sync_object.cluster_id = "145b9021-d47c-4094-957b-7545e8232ab7"
        assert self.sync_object.render() == [
            {
                'value': '145b9021-d47c-4094-957b-7545e8232ab7',
                'name': 'cluster_id',
                'key': '/clusters/145b9021-d47c-4094-957b-7545e8232ab7/'
                       'raw_map/cluster_id',
                'dir': False
            },
            {
                'value': None,
                'name': 'data',
                'key': '/clusters/145b9021-d47c-4094-957b-7545e8232ab7/'
                       'raw_map/data',
                'dir': False
            },
            {
                'value': None,
                'name': 'updated',
                'key': '/clusters/145b9021-d47c-4094-957b-7545e8232ab7/'
                       'raw_map/updated',
                       'dir': False
            }]
