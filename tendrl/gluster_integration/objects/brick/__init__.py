from tendrl.commons import objects


class Brick(objects.BaseObject):
    def __init__(
        self,
        vol_id=None,
        sequence_number=None,
        path=None,
        hostname=None,
        port=None,
        status=None,
        filesystem_type=None,
        mount_opts=None,
        utilization=None,
        *args,
        **kwargs
    ):
        super(Brick, self).__init__(*args, **kwargs)

        self.vol_id = vol_id
        self.sequence_number = sequence_number
        self.path = path
        self.hostname = hostname
        self.port = port
        self.status = status
        self.filesystem_type = filesystem_type
        self.mount_opts = mount_opts
        self.utilization = utilization
        self.value = 'clusters/{0}/Volumes/{1}/Bricks/{2}'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id,
                                       self.vol_id,
                                       self.path.replace("/", "_")
        )
        return super(Brick, self).render()
