import json
import os

from tendrl.commons.utils import log_utils as logger
from tendrl.commons.utils.time_utils import now as tendrl_now


def emit_event(resource, curr_value, msg, instance, severity):
    alert = {}
    alert['source'] = NS.publisher_id
    alert['classification'] = 'cluster'
    alert['pid'] = os.getpid()
    alert['time_stamp'] = tendrl_now().isoformat()
    alert['alert_type'] = 'STATUS'
    alert['severity'] = severity
    alert['resource'] = resource
    alert['current_value'] = curr_value
    alert['tags'] = dict(
        plugin_instance=instance,
        message=msg,
        integration_id=NS.tendrl_context.integration_id,
        cluster_name=NS.tendrl_context.cluster_name,
        sds_name=NS.tendrl_context.sds_name,
        fqdn=NS.node_context.fqdn
    )
    alert['node_id'] = NS.node_context.node_id
    if not NS.node_context.node_id:
        return
    payload = {'message': json.dumps(alert)}
    payload['alert_condition_state'] = severity
    payload['alert_condition_status'] = resource
    if severity == "INFO":
        payload['alert_condition_unset'] = True
    else:
        payload['alert_condition_unset'] = False
    logger.log(
        "notice",
        "alerting",
        payload
    )
