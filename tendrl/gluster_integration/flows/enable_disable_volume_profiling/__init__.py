from tendrl.commons import flows
from tendrl.commons.flows.exceptions import FlowExecutionFailedError
from tendrl.commons.utils import cmd_utils
from tendrl.commons.utils import log_utils as logger


VOL_PROFILE_ACTIONS = {
    "enable": "start",
    "disable": "stop"
}


class EnableDisableVolumeProfiling(flows.BaseFlow):
    def __init__(self, *args, **kwargs):
        super(EnableDisableVolumeProfiling, self).__init__(
            *args,
            **kwargs
        )

    def run(self):
        action = self.parameters["Cluster.volume_profiling_flag"]
        if action not in VOL_PROFILE_ACTIONS.keys():
            raise FlowExecutionFailedError(
                "Invalid value of Cluster.volume_profiling_flag "
                "(%s) while enable/disable volume profiling for"
                "cluster (%s). Valid values are enable/disable" %
                (
                    action,
                    NS.tendrl_context.integration_id
                )
            )

        _cluster = NS.tendrl.objects.Cluster(
            integration_id=NS.tendrl_context.integration_id
        ).load()
        _lock_details = {
            'node_id': NS.node_context.node_id,
            'tags': NS.node_context.tags,
            'type': NS.type,
            'job_name': self.__class__.__name__,
            'job_id': self.job_id
        }
        _cluster.locked_by = _lock_details
        _cluster.status = "set_volume_profiling"
        _cluster.current_job = {
            'job_id': self.job_id,
            'job_name': self.__class__.__name__,
            'status': 'in_progress'
        }
        _cluster.save()

        volumes = NS.tendrl.objects.GlusterVolume().load_all() or []
        failed_vols = []
        for volume in volumes:
            out, err, rc = cmd_utils.Command(
                "gluster volume profile %s %s" %
                (volume.name, VOL_PROFILE_ACTIONS[action])
            ).run()
            if err != "" or rc != 0:
                logger.log(
                    "error",
                    NS.publisher_id,
                    {
                        "message": "%s profiling failed for volume: %s" %
                        (action, volume.name)
                    },
                    job_id=self.parameters["job_id"],
                    flow_id=self.parameters["flow_id"]
                )
                failed_vols.append(volume.name)
            else:
                if action == "enable":
                    volume.profiling_enabled = "yes"
                else:
                    volume.profiling_enabled = "no"
                volume.save()
        if len(failed_vols) > 0:
            logger.log(
                "error",
                NS.publisher_id,
                {
                    "message": "%s profiling failed for "
                    "volumes: %s" % (action, str(failed_vols))
                },
                job_id=self.parameters['job_id'],
                flow_id=self.parameters["flow_id"]
            )

        _cluster = NS.tendrl.objects.Cluster(
            integration_id=NS.tendrl_context.integration_id
        ).load()
        _cluster.status = ""
        _cluster.locked_by = {}
        _cluster.current_job = {
            'status': "finished",
            'job_name': self.__class__.__name__,
            'job_id': self.job_id
        }
        _cluster.save()
        return True
