from tendrl.commons import objects
from tendrl.commons.objects import AtomExecutionFailedError
from tendrl.commons.utils import cmd_utils


class StartProfiling(objects.BaseAtom):
    def __init__(self, *args, **kwargs):
        super(StartProfiling, self).__init__(*args, **kwargs)

    def run(self):
        vol_id = self.parameters['Volume.vol_id']
        volume = NS.gluster.objects.Volume(
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

        return True
