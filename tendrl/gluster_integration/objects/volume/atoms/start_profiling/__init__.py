import time

from tendrl.commons import objects
from tendrl.commons.objects import AtomExecutionFailedError
from tendrl.commons.utils import cmd_utils


class StartProfiling(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(StartProfiling, self).__init__(*args, **kwargs)

    def run(self):
        vol_id = self.parameters['Volume.vol_id']
        volume = NS.tendrl.objects.GlusterVolume(
            vol_id=vol_id
        ).load()

        command = "gluster volume profile %s start" % volume.name
        cmd = cmd_utils.Command(command)
        out, err, rc = cmd.run()
        if rc != 0:
            raise AtomExecutionFailedError(
                "Error while enabling profiling "
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
                    "Could not enable profiling for volume: %s"
                    "under cluster: %s, Timed out" % (
                        volume.name,
                        NS.tendrl_context.integration_id
                    )
                )
            out, err, rc = cmd_utils.Command(
                "gluster volume profile %s info" % volume.name
            ).run()
            if rc == 0:
                break
            else:
                time.sleep(5)
                loop_count += 1

        volume.profiling_enabled = "yes"
        volume.save()
        return True
