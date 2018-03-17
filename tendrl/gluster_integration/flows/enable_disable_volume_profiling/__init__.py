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
                "cluster (%s)" % (
                    action,
                    NS.tendrl_context.integration_id
                )
            )

        volumes = NS.gluster.objects.Volume().load_all() or []
        failed_vols = []
        for volume in volumes:
            out, err, rc = cmd_utils.Command(
                "gluster volume profile %s %s" %
                (volume.name, VOL_PROFILE_ACTIONS[action])
            ).run()
            if err or rc != 0:
                logger.log(
                    "INFO",
                    NS.publisher_id,
                    {
                        "message": "%s profiling failed for volume: %s" %
                        (action, volume.name)
                    },
                    flow_id=self.parameters["flow_id"],
                    job_id=self.parameters["job_id"]
                )
                failed_vols.append(volume.name)
            else:
                if action == "enable":
                    volume.profiling_enabled = "yes"
                else:
                    volume.profiling_enabled = "no"
                volume.save()
        if len(failed_vols) > 0:
            raise FlowExecutionFailedError(
                "%s profiling failed for volumes %s" % (
                    action,
                    str(failed_vols)
                )
            )

        return True
