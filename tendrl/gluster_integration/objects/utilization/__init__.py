from tendrl.commons import objects


class Utilization(objects.BaseObject):
    def __init__(self, raw_capacity=None, usable_capacity=None,
                 used_capacity=None, pcnt_used=None, *args, **kwargs):
        super(Utilization, self).__init__(*args, **kwargs)

        self.raw_capacity = raw_capacity
        self.usable_capacity = usable_capacity
        self.used_capacity = used_capacity
        self.pcnt_used = pcnt_used
        self.value = 'clusters/{0}/Utilization'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id)
        return super(Utilization, self).render()
