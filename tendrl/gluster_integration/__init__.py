from tendrl.commons import TendrlNS


class GlusterIntegrationNS(TendrlNS):
    def __init__(self):
        self,
        ns_name = "gluster"
        ns_src = "tendrl.gluster_integration"
        super(GlusterIntegrationNS, self).__init__(ns_name, ns_src)
