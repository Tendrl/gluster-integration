===========
Environment
===========

1. Install Gluster current stable release (https://www.gluster.org/download/)
2. Install Etcd>=2.3.x && <3.x (https://github.com/coreos/etcd/releases/tag/v2.3.7)


============
Installation
============


1. Install http://github.com/tendrl/bridge_common
2. Install http://github.com/tendrl/gluster_bridge

    At the command line::

    $ python setup.py install
    $ cp etc/tendrl/tendrl.conf.sample /etc/tendrl/tendrl.conf

4. Edit /etc/tendrl/tendrl.conf as required
5. mkdir /var/log/tendrl
6. Run
    $ tendrl-gluster-bridge