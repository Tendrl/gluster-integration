import json
import os
import socket

from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons.utils.time_utils import now as tendrl_now


def emit_event(self, resource, curr_value, msg, instance):
    alert = {}
    alert['source'] = NS.publisher_id
    alert['pid'] = os.getpid()
    alert['time_stamp'] = tendrl_now().isoformat()
    alert['alert_type'] = 'status'
    severity = "INFO"
    if curr_value.lower() == "stopped":
        severity = "CRITICAL"
    alert['severity'] = severity
    alert['resource'] = resource
    alert['current_value'] = curr_value
    alert['tags'] = dict(
        plugin_instance=instance,
        message=msg,
        cluster_id=NS.tendrl_context.integration_id,
        cluster_name=NS.tendrl_context.cluster_name,
        sds_name=NS.tendrl_context.sds_name,
        fqdn=socket.getfqdn()
    )
    alert['node_id'] = NS.node_context.node_id
    if not NS.node_context.node_id:
        return
    Event(
        Message(
            "notice",
            "alerting",
            {'message': json.dumps(alert)}
        )
    )
