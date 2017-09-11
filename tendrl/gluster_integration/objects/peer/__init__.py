from tendrl.commons import objects


class Peer(objects.BaseObject):
    def __init__(
        self,
        state=None,
        connected=None,
        hostname=None,
        peer_uuid=None,
        *args,
        **kwargs
    ):
        super(Peer, self).__init__(*args, **kwargs)

        self.state = state
        self.connected = connected
        self.hostname = hostname
        self.peer_uuid = peer_uuid
        self.value = 'clusters/{0}/Peers/{1}'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id,
                                       self.peer_uuid)
        return super(Peer, self).render()
