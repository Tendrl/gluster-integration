import time

from tendrl.commons import objects
from tendrl.commons.objects import AtomExecutionFailedError
from tendrl.commons.utils import cmd_utils


class StopProfiling(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(StopProfiling, self).__init__(*args, **kwargs)

    def run(self):
        vol_id = self.parameters['Volume.vol_id']
        volume = NS.gluster.objects.Volume(
            vol_id=vol_id
        ).load()

        command = "gluster volume profile %s stop" % volume.name
        cmd = cmd_utils.Command(command)
        out, err, rc = cmd.run()
        if rc != 0:
            raise AtomExecutionFailedError(
                "Error while disabling profiling "
                "for volume: %s in cluster: %s. Error: %s" % (
                    volume.name,
                    NS.tendrl_context.integration_id,
                    err
                )
            )
        loop_count = 0
        while True:
            if loop_count >= 24:
                raise AtomExecutionFailedError(
                    "Volume profiling not yet marked disabled "
                    "for volume: %s in cluster: %s. Timing out" % (
                        volume.name,
                        NS.tendrl_context.integration_id
                    )
                )
            out, err, rc = cmd_utils.Command(
                "gluster volume profile %s info" % volume.name
            ).run()
            if rc == 1:
                break
            else:
                time.sleep(5)
                loop_count += 1
        volume.profiling_enabled = "no"
        volume.save()
        return True
