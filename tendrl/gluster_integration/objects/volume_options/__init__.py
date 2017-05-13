from tendrl.commons import objects


class VolumeOptions(objects.BaseObject):
    def __init__(
        self,
        vol_id=None,
        options=None,
    ):
        super(VolumeOptions, self).__init__()

        self.vol_id = vol_id
        self.options = options
        self.value = 'clusters/{0}/Volumes/{1}'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id,
                                       self.vol_id
        )
        return super(VolumeOptions, self).render()
