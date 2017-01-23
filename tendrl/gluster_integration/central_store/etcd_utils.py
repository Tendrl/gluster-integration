from tendrl.commons.etcdobj import fields


def to_etcdobj(cls_etcd, obj):
    for attr, value in vars(obj).iteritems():
        setattr(cls_etcd, attr, to_etcd_field(attr, value))
    return cls_etcd


def to_etcd_field(name, value):
    type_to_etcd_fields_map = {
        dict: fields.DictField,
        str: fields.StrField,
        int: fields.IntField
    }
    return type_to_etcd_fields_map[type(value)](name)
