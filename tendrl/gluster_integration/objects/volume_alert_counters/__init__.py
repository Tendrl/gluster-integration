from tendrl.commons import objects


class VolumeAlertCounters(objects.BaseObject):
    def __init__(
        self,
        alert_count=0,
        integration_id=None,
        volume_id=None,
        *args,
        **kwargs
    ):
        super(VolumeAlertCounters, self).__init__(*args, **kwargs)
        self.alert_count = alert_count
        self.integration_id = integration_id
        self.volume_id = volume_id
        self.value = '/clusters/{0}/Volumes/{1}/alert_counters'

    def render(self):
        self.value = self.value.format(
            (self.integration_id or NS.tendrl_context.integration_id),
            self.volume_id
        )
        return super(VolumeAlertCounters, self).render()
