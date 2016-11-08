from tendrl.gluster_bridge.persistence import servers


class Test_Peer(object):
    def test_peer(self):
        self.peer = servers.Peer()
        assert self.peer.render() == [
            {
                'name': 'cluster_id',
                'key': '/clusters/None/peers/None/cluster_id',
                'dir': False,
                'value': None
            },
            {
                'name': 'hostname',
                'key': '/clusters/None/peers/None/hostname',
                'dir': False,
                'value': None
            },
            {
                'name': 'peer_uuid',
                'key': '/clusters/None/peers/None/peer_uuid',
                'dir': False, 'value': None
            },
            {
                'name': 'state',
                'key': '/clusters/None/peers/None/state',
                'dir': False, 'value': None
            },
            {
                'name': 'updated',
                'key': '/clusters/None/peers/None/updated',
                'dir': False,
                'value': None
            }]


class Test_Volume(object):
    def test_volume(self):
        self.volume = servers.Volume()
        assert self.volume.render() == [
            {
                'dir': False,
                'name': 'brick_count',
                'key': '/clusters/None/volumes/None/brick_count',
                'value': None
            },
            {
                'dir': False,
                'name': 'cluster_id',
                'key': '/clusters/None/volumes/None/cluster_id',
                'value': None
            },
            {
                'dir': False,
                'name': 'name',
                'key': '/clusters/None/volumes/None/name',
                'value': None
            },
            {
                'dir': False,
                'name': 'status',
                'key': '/clusters/None/volumes/None/status',
                'value': None},
            {
                'dir': False,
                'name': 'vol_id',
                'key': '/clusters/None/volumes/None/vol_id',
                'value': None
            },
            {
                'dir': False,
                'name': 'vol_type',
                'key': '/clusters/None/volumes/None/vol_type',
                'value': None
            }]


class Test_Brick(object):
    def test_brick(self):
        self.brick = servers.Brick()
        self.brick.path = "/test/pytest"
        assert self.brick.render() == [
            {
                'name': 'cluster_id',
                'key': '/clusters/None/volumes/None/bricks/_test_pytest/'
                'cluster_id',
                'dir': False,
                'value': None
            },
            {
                'name': 'fs_type',
                'value': None,
                'dir': False,
                'key': '/clusters/None/volumes/None/bricks/_test_pytest/'
                'fs_type'
            },
            {
                'name': 'hostname',
                'value': None,
                'dir': False,
                'key': '/clusters/None/volumes/None/bricks/_test_pytest/'
                'hostname'
            },
            {
                'name': 'mount_opts',
                'value': None,
                'dir': False,
                'key': '/clusters/None/volumes/None/bricks/_test_pytest/'
                'mount_opts'
            },
            {
                'name': 'path',
                'value': '/test/pytest',
                'dir': False,
                'key': '/clusters/None/volumes/None/bricks/_test_pytest/'
                'path'
            },
            {
                'name': 'port',
                'value': None,
                'dir': False,
                'key': '/clusters/None/volumes/None/bricks/_test_pytest/'
                'port'
            },
            {
                'name': 'status',
                'value': None,
                'dir': False,
                'key': '/clusters/None/volumes/None/bricks/_test_pytest/'
                'status'
            },
            {
                'name': 'vol_id',
                'value': None,
                'dir': False,
                'key': '/clusters/None/volumes/None/bricks/_test_pytest/'
                'vol_id'
            }]
