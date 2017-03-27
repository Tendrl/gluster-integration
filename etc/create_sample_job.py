import etcd
from tendrl.commons.objects.job import Job
import json
import uuid


integration_id = "f123b6b7-515f-4b45-bc26-abf8700f0608"
job_id = str(uuid.uuid4())

payload = {
    "integration_id": integration_id,
    "run": "tendrl.gluster.flows.CreateVolume",
    "parameters": {
        "Volume.volname": 'Volume2',
        "Volume.bricks": [
            [
                {"12.34.45.56":"/mnt/sample5/sampleBrick1"},
                {"12.34.45.56":"/mnt/sample4/sampleBrick1"}
            ]
        ],
        "Volume.replica_count": "2",
        "Volume.force": True,
    },
    "type": "node",
    "node_ids": ["e7162cf9-199c-4bbb-b4eb-219cf5cb1ed2"]
}

def run():
    client = etcd.Client(host="10.70.43.135", port=2379)
    client.write("/queue/%s/payload" % job_id, json.dumps(payload))
    client.write("/queue/%s/status" % job_id, "new")
    client.write("/queue/%s/job_id" % job_id, job_id)
    print job_id

if __name__ == "__main__":
    run()
