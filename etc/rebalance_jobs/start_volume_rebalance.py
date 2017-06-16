import etcd
import json
import uuid


integration_id = "d3c644f1-0f94-43e1-946f-e40c4694d703"
job_id = str(uuid.uuid4())

payload = {
    "integration_id": integration_id,
    "run": "gluster.objects.Volume.flows.StartVolumeRebalance",
    "parameters": {
        "Volume.volname": 'GlusterVolume',
        "Volume.force": True, # optional
        "Volume.fix_layout": True, # optional
        "Volume.vol_id": '5c4839ab-1997-47a1-8fe8-fa3684c28f16',
    },
    "type": "sds",
    "tags": ["provisioner/d3c644f1-0f94-43e1-946f-e40c4694d703"]
}

def run():
    client = etcd.Client(host="xx.xx.xx.xx", port=2379)
    client.write("/queue/%s/payload" % job_id, json.dumps(payload))
    client.write("/queue/%s/status" % job_id, "new")
    client.write("/queue/%s/job_id" % job_id, job_id)
    print job_id

if __name__ == "__main__":
    run()
