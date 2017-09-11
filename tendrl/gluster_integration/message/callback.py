# The callback function names below should match(in small case)
# the event_type field of gluster native events as documented
# at: https://gluster.readthedocs.io/en/latest/Administrator%20Guide/
# Events%20APIs/ .
# Whenever gluster-integration receives a gluster native event,
# event handler checks if there is a callback function defined for
# that event in this file, If it finds then that callback function
# will be invoked


class Callback(object):
    def peer_connect(self, event):
        pass

    def peer_disconnect(self, event):
        pass

    def volume_create(self, event):
        pass

    def volume_delete(self, event):
        pass
