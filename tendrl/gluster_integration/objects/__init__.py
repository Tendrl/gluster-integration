from tendrl.commons import atoms
from tendrl.commons import objects


class GlusterIntegrationBaseObject(objects.BaseObject):
    def __init__(
            self,
            attrs=None,
            enabled=None,
            obj_list=None,
            obj_value=None,
            atoms=None,
            flows=None
    ):
        super(GlusterIntegrationBaseObject, self).__init__(
            attrs=None,
            enabled=None,
            obj_list=None,
            obj_value=None,
            atoms=None,
            flows=None
        )

        obj_def = tendrl_ns.definitions.get_obj_definition(
            tendrl_ns.to_str,
            self.__class__.__name__
        )
        # list of attr tuple of (attr_name, type)
        # eg: {'status': {'type': 'Boolean'}, 'fqdn': {'type': 'String'},
        # 'cmd_str': {'type': 'String'}}
        self.attrs = attrs or obj_def.attrs
        self.enabled = enabled or obj_def.enabled

        # path to LIST of all instance of the object
        self.obj_list = obj_list or obj_def.obj_list

        # path to GET an instance of the object
        self.obj_value = obj_value or obj_def.obj_value

        # eg: {'cmd': {'help': 'Executes a command', 'inputs': {'mandatory':
        # ['Node.cmd_str']}, 'run': 'tendrl.node_agent.atoms.node.cmd.Cmd',
        # 'name': 'Execute CMD on Node', 'type': 'Create', 'enabled': True,
        # 'uuid': 'dc8fff3a-34d9-4786-9282-55eff6abb6c3'},
        # 'check_node_up': {'inputs': {'mandatory': ['Node.fqdn']},
        # 'run': 'tendrl.node_agent.atoms.node.check_node_up',
        # 'help': 'Checks if a node is up', 'outputs': ['Node.status'],
        # 'enabled': True, 'name': 'check whether the node is up',
        # 'type': 'Create', 'uuid': 'eda0b13a-7362-48d5-b5ca-4b6d6533a5ab'}}
        self.atoms = atoms or obj_def.atoms

        # List of flows under this object
        self.flows = flows or obj_def.flows


class GlusterIntegrationBaseAtom(atoms.BaseAtom):
    obj = GlusterIntegrationBaseObject
    def __init__(self, *args, **kwargs):
        super(GlusterIntegrationBaseAtom, self).__init__(*args, **kwargs)
