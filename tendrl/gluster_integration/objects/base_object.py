import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseObject(object):
    def __init__(
            self,
            name=None,
            attrs=None,
            enabled=None,
            obj_list=None,
            obj_value=None,
            atoms=None,
            flows=None
    ):
        self.name = name

        self.attrs = attrs
        self.enabled = enabled

        # path to LIST of all instance of the object
        self.obj_list = obj_list

        # path to GET an instance of the object
        self.obj_value = obj_value

        self.atoms = atoms

        # List of flows under this object
        self.flows = flows

    def __new__(cls, *args, **kwargs):

        super_new = super(BaseObject, cls).__new__
        if super_new is object.__new__:
            instance = super_new(cls)
        else:
            instance = super_new(cls, *args, **kwargs)

        return instance


@six.add_metaclass(abc.ABCMeta)
class GlusterIntegrationObject(BaseObject):
    def __init__(
            self,
            name=None,
            attrs=None,
            enabled=None,
            obj_list=None,
            obj_value=None,
            atoms=None,
            flows=None
    ):
        obj_def = tendrl_ns.definitions.get_obj(
            tendrl_ns.to_str,
            self.__class__.__name__
        )
        self.name = name or obj_def.name

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

    def __new__(cls, *args, **kwargs):

        super_new = super(GlusterIntegrationObject, cls).__new__
        if super_new is object.__new__:
            instance = super_new(cls)
        else:
            instance = super_new(cls, *args, **kwargs)

        return instance
