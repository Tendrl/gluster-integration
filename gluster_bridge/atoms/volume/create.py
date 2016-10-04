import subprocess


class Create(object):
    def start(self, name, bricks):
        subprocess.call(['gluster', 'volume', 'create',
                         name, ' '.join(bricks), ' force'])
        subprocess.call(['gluster', 'volume', 'start', name])

