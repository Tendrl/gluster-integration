from tendrl.commons import objects


class ClientConnection(objects.BaseObject):
    def __init__(
        self,
        brick_name,
        hostname,
        fqdn,
        brick_dir,
        bytesread,
        byteswrite,
        opversion,
        *args,
        **kwargs
    ):
        super(ClientConnection, self).__init__(*args, **kwargs)

        self.brick_name = brick_name
        self.fqdn = fqdn
        self.brick_dir = brick_dir
        self.hostname = hostname
        self.bytesread = bytesread
        self.byteswrite = byteswrite
        self.opversion = opversion
        self.value = 'clusters/{0}/Bricks/all/{1}/{2}/ClientConnections/{3}'

    def render(self):
        self.value = self.value.format(
            NS.tendrl_context.integration_id,
            self.fqdn,
            self.brick_dir,
            self.hostname
        )
        return super(ClientConnection, self).render()
