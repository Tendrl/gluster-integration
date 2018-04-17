from tendrl.commons import objects


class GeoReplicationPair(objects.BaseObject):
    def __init__(
        self,
        vol_id,
        session_id,
        pair=None,
        master_node=None,
        master_volume=None,
        master_brick=None,
        slave_user=None,
        slave=None,
        slave_node=None,
        status=None,
        crawl_status=None,
        last_synced=None,
        entry=None,
        data=None,
        meta=None,
        failures=None,
        checkpoint_time=None,
        checkpoint_completed=None,
        checkpoint_completion_time=None,
        *args,
        **kwargs
    ):
        super(GeoReplicationPair, self).__init__(*args, **kwargs)

        self.vol_id = vol_id
        self.session_id = session_id
        self.pair = pair
        self.master_node = master_node
        self.master_volume = master_node
        self.master_brick = master_brick
        self.slave_user = slave_user
        self.slave = slave
        self.slave_node = slave_node
        self.status = status
        self.crawl_status = crawl_status
        self.last_synced = last_synced
        self.entry = entry
        self.data = data
        self.meta = meta
        self.failures = failures
        self.checkpoint_time = checkpoint_time
        self.checkpoint_completed = checkpoint_completed
        self.checkpoint_completion_time = checkpoint_completion_time
        self.value = 'clusters/{0}/Volumes/{1}/GeoRepSessions/{2}/pairs/{3}'

    def render(self):
        self.value = self.value.format(
            NS.tendrl_context.integration_id,
            self.vol_id,
            self.session_id,
            self.pair
        )
        return super(GeoReplicationPair, self).render()
