from tendrl.gluster_integration.objects.peer import Peer


def test_peer():
    obj = Peer(
        state="['Peer', 'Cluster', 'in']",
        connected="Connected",
        hostname="dhcp12-123.lab.abc.com",
        peer_uuid="53dfa0fa-edb2-4966-80b9-86ca981c7fcb"
    )
    out = [
        {'dir': False,
         'value': False,
         'name': 'deleted',
         'key': '/clusters/77deef29-b8e5-4dc5-8247-21e2a'
                '409a66a/Peers/53dfa0fa-edb2-4966-80b9-8'
                '6ca981c7fcb/deleted'
         },
        {'dir': False,
         'value': '',
         'name': 'deleted_at',
         'key': '/clusters/77deef29-b8e5-4dc5-8247-21e2a'
                '409a66a/Peers/53dfa0fa-edb2-4966-80b9-8'
                '6ca981c7fcb/deleted_at'
         },
        {'dir': False,
         'value': "['Peer', 'Cluster', 'in']",
         'name': 'state',
         'key': '/clusters/77deef29-b8e5-4dc5-8247-21e2a'
                '409a66a/Peers/53dfa0fa-edb2-4966-80b9-8'
                '6ca981c7fcb/state'
         },
        {'dir': False,
         'value': 'Connected',
         'name': 'connected',
         'key': '/clusters/77deef29-b8e5-4dc5-8247-21e2a'
         '409a66a/Peers/53dfa0fa-edb2-4966-80b9-86ca981c'
         '7fcb/connected'
         },
        {'dir': False,
         'value': '53dfa0fa-edb2-4966-80b9-86ca981c7fcb',
         'name': 'peer_uuid',
         'key': '/clusters/77deef29-b8e5-4dc5-8247-21e2a4'
                '09a66a/Peers/53dfa0fa-edb2-4966-80b9-86ca'
                '981c7fcb/peer_uuid'
         },
        {'dir': False,
         'value': 'dhcp12-123.lab.abc.com',
         'name': 'hostname',
         'key': '/clusters/77deef29-b8e5-4dc5-8247-21e2a40'
                '9a66a/Peers/53dfa0fa-edb2-4966-80b9-86ca9'
                '81c7fcb/hostname'
         }
    ]
    for result in obj.render():
        if result not in out:
            raise AssertionError
