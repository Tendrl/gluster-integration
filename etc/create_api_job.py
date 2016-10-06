import json
import uuid

import etcd

job_id1 = str(uuid.uuid4())

job = {
    "cluster_id": "49fa2adde8a6e98591f0f5cb4bc5f44d",
    "sds_type": "gluster",
    "flow": "CreateVolume",
    "object_type": "volume",
    "status": 'new',
    "message": 'Creating cluster',
    "attributes": {
        "volname": 'Volume1',
        "brickdetails": ["mntpath"]
    },
    "errors": {}

}


client = etcd.Client()
client.write("/api_job_queue/job_%s" % job_id1, json.dumps(job))
