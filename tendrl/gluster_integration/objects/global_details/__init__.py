from tendrl.commons import objects


class GlobalDetails(objects.BaseObject):
    def __init__(self, status=None, connection_count=None,
                 connection_active=None, volume_up_degraded=None,
                 *args, **kwargs):
        super(GlobalDetails, self).__init__(*args, **kwargs)

        self.status = status
        self.connection_count = connection_count
        self.connection_active = connection_active
        self.volume_up_degraded = volume_up_degraded
        self.value = 'clusters/{0}/GlobalDetails'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id)
        return super(GlobalDetails, self).render()
