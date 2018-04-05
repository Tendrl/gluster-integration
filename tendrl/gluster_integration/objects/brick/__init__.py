from tendrl.commons import objects
from tendrl.commons.utils import etcd_utils


class Brick(objects.BaseObject):
    def __init__(
        self,
        fqdn,
        brick_dir=None,
        name=None,
        devices=None,
        partitions=None,
        brick_path=None,
        mount_path=None,
        node_id=None,
        vol_id=None,
        vol_name=None,
        sequence_number=None,
        hostname=None,
        port=None,
        status=None,
        filesystem_type=None,
        mount_opts=None,
        utilization=None,
        used=None,
        lv=None,
        vg=None,
        pool=None,
        pv=None,
        size=None,
        disk_type=None,
        disk_count=None,
        stripe_size=None,
        client_count=None,
        is_arbiter=None,
        deleted=False,
        deleted_at=None,
        *args,
        **kwargs
    ):
        super(Brick, self).__init__(*args, **kwargs)

        self.devices = devices
        self.partitions = partitions
        self.name = name
        self.node_id = node_id
        self.fqdn = fqdn
        self.brick_dir = brick_dir
        self.brick_path = brick_path
        self.mount_path = mount_path
        self.disk_type = disk_type
        self.disk_count = disk_count
        self.lv = lv
        self.vg = vg
        self.pool = pool
        self.pv = pv
        self.stripe_size = stripe_size
        self.vol_id = vol_id
        self.vol_name = vol_name
        self.sequence_number = sequence_number
        self.hostname = hostname
        self.port = port
        self.size = size
        self.status = status
        self.filesystem_type = filesystem_type
        self.mount_opts = mount_opts
        self.utilization = utilization
        self.used = used
        self.client_count = client_count
        self.is_arbiter = is_arbiter
        self.deleted = deleted
        self.deleted_at = deleted_at
        self.value = 'clusters/{0}/Bricks/all/{1}/{2}'

    def save(self, update=True, ttl=None):
        if not self.hash_compare_with_central_store():
            _volume = NS.gluster.objects.Volume(vol_id=self.vol_id)
            _volume.invalidate_hash()

        super(Brick, self).save(update)
        status = self.value + "/status"
        if ttl:
            etcd_utils.refresh(status, ttl)

        return

    def render(self):
        self.value = self.value.format(
            NS.tendrl_context.integration_id,
            self.fqdn,
            self.brick_dir
        )
        return super(Brick, self).render()

    def on_change(self, attr, prev_value, current_value):
        return
