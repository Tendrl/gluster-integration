import etcd
import json
import uuid


integration_id = "89604c6b-2eff-4221-96b4-e41319240240"
job_id = str(uuid.uuid4())

payload = {
    "integration_id": integration_id,
    "run": "tendrl.gluster.flows.GenerateBrickMapping",
    "parameters": {
        "Cluster.node_configuration": {
            "67afa32d-883b-45f3-b331-bc96ecd010ba": None,
            "erafa32d-883b-45f3-b331-bc96ecd010ba": None,
            "uuafa32d-883b-45f3-b331-bc96ecd010ba": None,
            "daafa32d-883b-45f3-b331-bc96ecd010ba": None,
        },
        "Volume.brick_count": 3,
        "Volume.subvol_size": 2
    },
    "type": "sds",
    "tags": ["provisioner/89604c6b-2eff-4221-96b4-e41319240240"]
}

def run():
    client = etcd.Client(host="xx.xx.xx.xx", port=2379)
    client.write("/queue/%s/payload" % job_id, json.dumps(payload))
    client.write("/queue/%s/status" % job_id, "new")
    client.write("/queue/%s/job_id" % job_id, job_id)
    print job_id

if __name__ == "__main__":
    run()
