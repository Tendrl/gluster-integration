import json

import etcd
from gluster_bridge.atoms.volume.create import Create

class CreateVolume(object):
    def __init__(self, api_job):
        super(CreateVolume, self).__init__()
        self.api_job = api_job
        self.atom = Create

    def start(self):
        vol_name = self.api_job['attributes']['volname']
        brickdetails = self.api_job['attributes']['brickdetails']
        self.atom().start(vol_name, brickdetails)
        self.api_job['status'] = "finished"
        etcd.Client().write(self.api_job['request_id'], json.dumps(self.api_job))
