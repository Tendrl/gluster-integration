from tendrl.commons import objects


class SyncObject(objects.BaseObject):
    def __init__(self, data=None, node_id=None,
                 integration_id=None, *args, **kwargs):
        super(SyncObject, self).__init__(*args, **kwargs)

        self.data = data
        self._node_id = node_id
        self._integration_id = integration_id
        self.value = 'clusters/{0}/nodes/{1}/raw_map'

    def render(self):
        self.value = self.value.format(
            self._integration_id or NS.tendrl_context.integration_id,
            self._node_id or NS.node_context.node_id
        )
        return super(SyncObject, self).render()
