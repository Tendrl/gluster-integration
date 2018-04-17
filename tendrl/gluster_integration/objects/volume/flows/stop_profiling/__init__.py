from tendrl.commons import flows
from tendrl.commons.flows.exceptions import FlowExecutionFailedError
from tendrl.commons.objects import AtomExecutionFailedError


class StopProfiling(flows.BaseFlow):
    def __init__(self, *args, **kwargs):
        super(StopProfiling, self).__init__(*args, **kwargs)

    def run(self):
        volume = NS.tendrl.objects.GlusterVolume(
            vol_id=self.parameters['Volume.vol_id']
        ).load()
        if 'job_id' in volume.locked_by \
            and 'status' in volume.current_job \
            and volume.current_job['status'] in ['in_progress']:
            raise FlowExecutionFailedError(
                "Another job in progress for volume."
                " Please wait till the job finishes "
                "(job_id: %s) (volume: %s) (integration_id: %s) " %
                (
                    volume.current_job['job_id'],
                    volume.name,
                    NS.tendrl_context.integration_id
                )
            )
        _lock_details = {
            'node_id': NS.node_context.node_id,
            'fqdn': NS.node_context.fqdn,
            'tags': NS.node_context.tags,
            'type': NS.type,
            'job_name': self.__class__.__name__,
            'job_id': self.job_id
        }
        volume.locked_by = _lock_details
        volume.current_job = {
            'job_id': self.job_id,
            'job_name': self.__class__.__name__,
            'status': "in_progress"
        }
        volume.save()

        try:
            super(StopProfiling, self).run()
        except (FlowExecutionFailedError,
                AtomExecutionFailedError,
                Exception) as ex:
            volume = NS.tendrl.objects.GlusterVolume(
                vol_id=self.parameters['Volume.vol_id']
            ).load()
            volume.current_job = {
                'job_id': self.job_id,
                'job_name': self.__class__.__name__,
                'status': "failed"
            }
            volume.locked_by = {}
            volume.save(update=False)
            raise ex

        volume = NS.tendrl.objects.GlusterVolume(
            vol_id=self.parameters['Volume.vol_id']
        ).load()
        volume.current_job = {
            'job_id': self.job_id,
            'job_name': self.__class__.__name__,
            'status': "finished"
        }
        volume.locked_by = {}
        volume.save(update=False)
        return True
