import json

import etcd
from tendrl.gluster_bridge.atoms.volume.create import Create


class CreateVolume(object):
    def __init__(self, api_job):
        super(CreateVolume, self).__init__()
        self.api_job = api_job
        self.atom = Create

    def start(self):
        attributes = json.loads(self.api_job['attributes'].decode('utf-8'))
        vol_name = attributes['volname']
        brickdetails = attributes['brickdetails']
        self.atom().start(vol_name, brickdetails)
        self.api_job['status'] = "finished"
        etcd.Client().write(self.api_job['request_id'],
                            json.dumps(self.api_job))
