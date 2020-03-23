import etcd
import json
import uuid


integration_id = "ab3b125e-4769-4071-a349-e82b380c11f4"
job_id = str(uuid.uuid4())

payload = {
    "integration_id": integration_id,
    "run": "tendrl.gluster.flows.CreateGlusterBrick",
    "parameters": {
        "Cluster.node_configuration": {
            "81720b6c-6732-49dd-ad32-15845f199c79": {
                "vdb": {
                    "brick_name": "brick_1",
                },
                "vdc": {
                    "brick_name": "brick_2",
                },
                "vdd": {
                    "brick_name": "brick_3",
                },
            },
            "ab003bbc-00cd-4b74-b236-f19c2c33b96b": {
                "vdb": {
                    "brick_name": "brick_1",
                },
                "vdc": {
                    "brick_name": "brick_2",
                },
                "vdd": {
                    "brick_name": "brick_3",
                },
            }
        },
        'GlusterBrick.disk_type': "raid10",
        'GlusterBrick.disk_count': "4",
        'GlusterBrick.stripe_size': "128",
    },
    "type": "sds",
    "tags": "provisioner/4a47db22-b286-44da-8240-c8256b28d256"
}

def run():
    client = etcd.Client(host="11.22.33.44", port=2379)
    client.write("/queue/%s/payload" % job_id, json.dumps(payload))
    client.write("/queue/%s/status" % job_id, "new")
    client.write("/queue/%s/job_id" % job_id, job_id)
    print(job_id)

if __name__ == "__main__":
    run()
