from flask import Flask
from flask import request
import gevent
import gevent.event
import gevent.greenlet
from gevent.wsgi import WSGIServer

from tendrl.commons.utils import cmd_utils
from tendrl.commons.utils import log_utils as logger
from tendrl.commons.utils import service as svc
from tendrl.commons.utils import service_status as svc_stat
from tendrl.gluster_integration.message import callback as cb


app = Flask(__name__)


class GlusterNativeMessageHandler(gevent.greenlet.Greenlet):
    def __init__(self):
        super(GlusterNativeMessageHandler, self).__init__()
        self.path = "/listen"
        self.host = "0.0.0.0"
        self.port = 8697
        self.callback = cb.Callback()

        @app.route(self.path, methods=["POST"])
        def events_listener():
            gluster_event = request.json
            if gluster_event:
                callback_function_name = gluster_event["event"].lower()
                try:
                    function = getattr(self.callback, callback_function_name)
                except AttributeError:
                    # tendrl does not handle this perticular event hence ignore
                    pass
                event_handler = gevent.spawn(function, gluster_event)
                event_handler.join()

    def _setup_gluster_native_message_reciever(self):
        service = svc.Service("glustereventsd")
        message, success = service.start()
        gluster_eventsd = svc_stat.ServiceStatus("glustereventsd")
        if not gluster_eventsd.status():
            if not success:
                logger.log(
                    "error",
                    NS.publisher_id,
                    {
                        "message": "glustereventsd could"
                        " not be started: %s" % message
                    }
                )
                return False

        url = "http://{0}:{1}{2}".format(self.host, str(self.port), self.path)
        cmd = cmd_utils.Command('gluster-eventsapi webhook-add %s' % url)
        out, err, rc = cmd.run()
        if rc != 0:
            logger.log(
                "error",
                NS.publisher_id,
                {
                    "message": "could not add webhook"
                    " for glustereventsd. Error: %s" % err
                }
            )
        return True

    def _cleanup_gluster_native_message_reciever(self):
        url = "http://{0}:{1}{2}".format(self.host, str(self.port), self.path)
        cmd = cmd_utils.Command('gluster-eventsapi webhook-del %s' % url)
        out, err, rc = cmd.run()
        if rc != 0:
            logger.log(
                "error",
                NS.publisher_id,
                {
                    "message": "could not delete webhook from"
                    " glustereventsd. Error: %s" % err
                }
            )
        return True

    def stop(self):
        if not self._cleanup_gluster_native_message_reciever():
            logger.log(
                "error",
                NS.publisher_id,
                {"message": "gluster native message reciever cleanup failed"}
            )

    def _run(self):
        if not self._setup_gluster_native_message_reciever():
            logger.log(
                "error",
                NS.publisher_id,
                {"message": "gluster native message reciever setup failed"}
            )
            return
        event_receiver = WSGIServer((self.host, self.port), app)
        event_receiver.serve_forever()
