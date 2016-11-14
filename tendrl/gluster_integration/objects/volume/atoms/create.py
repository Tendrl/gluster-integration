import subprocess


class Create(object):
    def run(self, parameters):
        cmd = ['gluster', 'volume', 'create', parameters.get('volname')]
        if parameters.get('stripe_count') is not None:
            cmd.append('stripe')
            cmd.append(str(parameters.get('stripe_count')))
        elif parameters.get('replica_count') is not None:
            cmd.append('replica')
            cmd.append(str(parameters.get('replica_count')))
            if parameters.get('arbiter_count') is not None:
                cmd.append('arbiter')
                cmd.append(str(parameters.get('arbiter_count')))
        elif parameters.get('disperse_count') is not None:
            cmd.append('disperse')
            cmd.append(str(parameters.get('disperse_count')))
        elif parameters.get('redundancy_count') is not None:
            cmd.append('redundancy')
            cmd.append(str(parameters.get('redundancy_count')))
        elif parameters.get('disperse_data_count') is not None:
            cmd.append('disperse-data')
            cmd.append(str(parameters.get('disperse_data_count')))
        if parameters.get('transport'):
            cmd.append('transport')
            cmd.append(','.join(parameters.get('transport')))
        cmd.extend(parameters.get('brickdetails'))
        cmd.append('force')
        cmd.append('--mode=script')
        subprocess.call(cmd)
        subprocess.call(
            [
                'gluster',
                'volume',
                'start',
                parameters.get('volname'),
                '--mode=script'
            ]
        )
        return True
