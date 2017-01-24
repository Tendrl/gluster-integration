from tendrl.commons import flows


class GlusterIntegrationBaseFlow(flows.BaseFlow):
    def __init__(self, *args, **kwargs):
        super(GlusterIntegrationBaseFlow, self).__init__(*args, **kwargs)
