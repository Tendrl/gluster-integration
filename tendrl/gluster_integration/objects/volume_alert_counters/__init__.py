from tendrl.commons import objects


class VolumeAlertCounters(objects.BaseObject):
    def __init__(
        self,
        warn_count=0,
        integration_id='',
        volume_id='',
        *args,
        **kwargs
    ):
        super(VolumeAlertCounters, self).__init__(*args, **kwargs)
        self.warning_count = warn_count
        self.integration_id = integration_id
        self.volume_id = volume_id
        self.value = '/clusters/{0}/Volumes/{1}/alert_counters'

    def render(self):
        self.value = self.value.format(
            self.integration_id, self.volume_id)
        return super(VolumeAlertCounters, self).render()
