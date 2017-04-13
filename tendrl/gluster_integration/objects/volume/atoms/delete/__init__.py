import etcd
import subprocess

from tendrl.commons.event import Event
from tendrl.commons.message import Message
from tendrl.commons import objects
from tendrl.gluster_integration.objects.volume import Volume


class Delete(objects.BaseAtom):
    obj = Volume
    def __init__(self, *args, **kwargs):
        super(Delete, self).__init__(*args, **kwargs)

    def run(self):
        vol_id = self.parameters['Volume.vol_id']
        if NS.gdeploy_plugin.stop_volume(
                self.parameters.get('Volume.volname')
        ):
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Stopped the volume %s before delete" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
        else:
            Event(
                Message(
                    priority="error",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Could not stop volume %s before delete" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False
        args = {}
        if self.parameters.get('Volume.volname') is not None:
            args.update({
                "format_bricks": self.parameters.get('Volume.format_bricks')
            })

        if NS.gdeploy_plugin.delete_volume(
                self.parameters.get('Volume.volname'),
                **args
        ):
            Event(
                Message(
                    priority="info",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Deleted the volume %s" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
        else:
            Event(
                Message(
                    priority="error",
                    publisher=NS.publisher_id,
                    payload={
                        "message": "Failed to delete volume %s" %
                        self.parameters['Volume.volname']
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=NS.tendrl_context.integration_id,
                )
            )
            return False

        while True:
            try:
                NS.etcd_orm.client.delete(
                    "clusters/%s/Volumes/%s" % (
                        NS.tendrl_context.integration_id,
                        self.parameters['Volume.vol_id']
                    ),
                    recursive=True
                )
            except (etcd.EtcdKeyNotFound, KeyError):
                Event(
                    Message(
                        priority="info",
                        publisher=NS.publisher_id,
                        payload={
                            "message": "Deleted the volume %s" %
                            self.parameters['Volume.volname']
                        },
                        job_id=self.parameters["job_id"],
                        flow_id=self.parameters["flow_id"],
                        cluster_id=NS.tendrl_context.integration_id,
                    )
                )
                return True
