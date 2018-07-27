from tendrl.commons import objects


class GeoReplicationSessionStatus(object):
    UP = "up"
    PARTIAL = "partial"
    DOWN = "down"
    CREATED = "created"
    STOPPED = "stopped"
    PAUSED = "paused"


class GeoReplicationSession(objects.BaseObject):
    def __init__(
        self,
        vol_id,
        session_id=None,
        session_status=None,
        pairs=None,
        integration_id=None,
        *args,
        **kwargs
    ):
        super(GeoReplicationSession, self).__init__(*args, **kwargs)

        self.vol_id = vol_id
        self.session_id = session_id
        self.session_status = session_status
        self.integration_id = integration_id or \
            NS.tendrl_context.integration_id
        if pairs:
            self.pairs = pairs
        self.value = 'clusters/{0}/Volumes/{1}/GeoRepSessions/{2}'

    def render(self):
        self.value = self.value.format(
            self.integration_id or NS.tendrl_context.integration_id,
            self.vol_id,
            self.session_id
        )
        return super(GeoReplicationSession, self).render()
