import logging

from tendrl.commons import objects

LOG = logging.getLogger(__name__)


class GlusterBrick(objects.BaseObject):
    def __init__(
        self,
        name,
        disk,
        brick_path,
        mount_path,
        node_id,
        lv=None,
        vg=None,
        pool=None,
        pv=None,
        disk_type=None,
        disk_count=None,
        stripe_size=None,
        *args,
        **kwargs
    ):
        super(GlusterBrick, self).__init__(*args, **kwargs)

        self.disk = disk
        self.name = name
        self.node_id = node_id
        self.brick_path = brick_path
        self.mount_path = mount_path
        self.disk_type = disk_type
        self.disk_count = disk_count
        self.lv = lv
        self.vg = vg
        self.pool = pool
        self.pv = pv
        self.stripe_size = stripe_size
        self.value = 'clusters/{0}/nodes/{1}/GlusterBricks/{2}'

    def render(self):
        self.value = self.value.format(NS.tendrl_context.integration_id,
                                       self.node_id,
                                       self.name.replace("/", "_")
        )
        return super(GlusterBrick, self).render()
