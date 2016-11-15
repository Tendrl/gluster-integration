import subprocess


class Stop(object):
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
        return True
