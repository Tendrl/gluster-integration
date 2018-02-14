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

        return True
