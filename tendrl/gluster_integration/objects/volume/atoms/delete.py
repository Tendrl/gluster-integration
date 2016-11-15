import subprocess


class Delete(object):
    def run(self, parameters):
        subprocess.call(
            [
                'gluster',
                'volume',
                'stop',
                parameters.get('volname'),
                '--mode=script'
            ]
        )
        subprocess.call(
            [
                'gluster',
                'volume',
                'delete',
                parameters.get('volname'),
                '--mode=script'
            ]
        )
        return True
