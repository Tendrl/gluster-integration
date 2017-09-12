from tendrl.commons import objects


class NativeEvents(objects.BaseObject):
    def __init__(
        self,
        context=None,
        processed=None,
        recovery_processed=None,
        message=None,
        severity=None,
        alert_notify=None,
        current_value=None,
        *args,
        **kwargs
    ):
        super(NativeEvents, self).__init__(*args, **kwargs)

        self.context = context
        self.processed = processed
        self.recovery_processed = recovery_processed
        self.message = message
        self.severity = severity
        self.alert_notify = alert_notify
        self.current_value = current_value
        self.value = 'clusters/{0}/native_events/{1}'

    def render(self):
        context = self.context.replace(
            " ", "").replace("/", "_").replace("\\", "-")
        self.value = self.value.format(
            NS.tendrl_context.integration_id,
            context
        )
        return super(NativeEvents, self).render()
