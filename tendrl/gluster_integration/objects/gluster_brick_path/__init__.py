from tendrl.commons import objects


class GlusterBrickDir(objects.BaseObject):
    def __init__(
        self,
        default_brick_dir=None,
        *args,
        **kwargs
    ):
        super(GlusterBrickDir, self).__init__(*args, **kwargs)

        self.default_brick_dir = default_brick_dir if default_brick_dir else \
                                  NS.config.data.get(
                                      'gluster_bricks_dir', "/tendrl_gluster_bricks"
                                  )
        self.value = 'clusters/{0}/GlusterBrickDir'

    def render(self):
        self.value = self.value.format(
            NS.tendrl_context.integration_id,
        )
        return super(GlusterBrickDir, self).render()
