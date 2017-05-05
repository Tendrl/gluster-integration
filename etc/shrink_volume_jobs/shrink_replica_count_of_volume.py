import etcd
import json
import uuid


integration_id = "ab3b125e-4769-4071-a349-e82b380c11f4"
job_id = str(uuid.uuid4())

payload = {
    "integration_id": integration_id,
    "run": "tendrl.gluster.objects.Volume.flows.ShrinkVolume",
    "parameters": {
        "Volume.volname": 'Vol3',
        "Volume.vol_id": "ad8ca449-61ad-43d4-9e48-17acf4c7286e",
        "Volume.bricks": [
            [
                {"<hostname>":"/glusterfs/brick31/b31"}
            ],
            [
                {"<hostname>":"/glusterfs/brick33/b33"}
            ],
        ],
        "Volume.replica_count": 2,
        "Volume.force": True,
        "Volume.action": "start",
    },
    "type": "sds",
    "tags": "provisioner/ab3b125e-4769-4071-a349-e82b380c11f4"
}

def run():
    client = etcd.Client(host="12.34.45.67", port=2379)
    client.write("/queue/%s/payload" % job_id, json.dumps(payload))
    client.write("/queue/%s/status" % job_id, "new")
    client.write("/queue/%s/job_id" % job_id, job_id)
    print job_id

if __name__ == "__main__":
    run()
