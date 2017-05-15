from tendrl.commons import objects


class SyncObject(objects.BaseObject):
    def __init__(
        self,
        data=None,
        *args,
        **kwargs
    ):
        super(SyncObject, self).__init__(*args, **kwargs)

        self.data = data
        self.value = 'clusters/{0}/raw_map'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id)
        return super(SyncObject, self).render()
