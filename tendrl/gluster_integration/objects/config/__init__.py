from tendrl.commons import config as cmn_config


from tendrl.commons import objects


class Config(objects.BaseObject):
    internal = True

    def __init__(self, config=None, *args, **kwargs):
        self._defs = {}
        super(Config, self).__init__(*args, **kwargs)

        self.data = config or cmn_config.load_config(
            'gluster-integration',
            "/etc/tendrl/gluster-integration/gluster-integration.conf.yaml"
        )
        self.value = '_NS/gluster/config'
