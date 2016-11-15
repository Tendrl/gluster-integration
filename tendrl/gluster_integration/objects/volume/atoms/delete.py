import subprocess


class Delete(object):
    def run(self, parameters):
        subprocess.call(
            [
                'gluster',
                'volume',
                'stop',
                parameters.get('Volume.volname'),
                '--mode=script'
            ]
        )
        subprocess.call(
            [
                'gluster',
                'volume',
                'delete',
                parameters.get('Volume.volname'),
                '--mode=script'
            ]
        )
        return True
