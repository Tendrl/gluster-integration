from mock import patch

from tendrl.commons.utils.cmd_utils import Command
from tendrl.commons.utils.service import Service
from tendrl.commons.utils.service_status import ServiceStatus
from tendrl.gluster_integration.message.gluster_native_message_handler import \
    GlusterNativeMessageHandler


@patch.object(Service, "start")
@patch.object(ServiceStatus, "status")
@patch.object(Command, "run")
def test_gluster_native_message_handler(cmd, status, start):
    cmd.return_value = ("testing", None, 0)
    start.return_value = ("testing", True)
    status.return_value = True
    obj = GlusterNativeMessageHandler()
    obj._setup_gluster_native_message_reciever()
    cmd.return_value = ("testing", "error", 1)
    obj._setup_gluster_native_message_reciever()
    start.return_value = ("testing", False)
    obj._setup_gluster_native_message_reciever()
    obj._cleanup_gluster_native_message_reciever()
