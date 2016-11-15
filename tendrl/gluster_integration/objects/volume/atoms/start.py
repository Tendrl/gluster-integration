import subprocess


class Start(object):
    def run(self, parameters):
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
