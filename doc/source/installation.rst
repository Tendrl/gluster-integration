===========
Environment
===========

1. Install Gluster current stable release (https://www.gluster.org/download/)
2. Install Etcd>=2.3.x && <3.x (https://github.com/coreos/etcd/releases/tag/v2.3.7)


============
Installation
============

Since there is no stable release yet, the only option is to install the project from the source.

Development version from the source
-----------------------------------

1. Install http://github.com/tendrl/bridge_common from the source code::

    $ git clone https://github.com/Tendrl/bridge_common.git
    $ cd bridge_common
    $ mkvirtualenv bridge_common
    $ pip install .

2. Create bridge_common logging config file::

    $ cp etc/samples/logging.yaml.timedrotation.sample /etc/tendrl/common_logging.yaml

Note that there are other sample config files for logging shipped with the product
and could be utilized for logging differently. For example there are config files
bundeled for syslog and journald logging as well. These could be used similarly as above.

3. Install gluster_bridge itself::
    $ git clone https://github.com/shtripat/gluster_bridge.git
    $ cd gluster_bridge
    $ workon gluster_bridge
    $ pip install .

Note that we use virtualenvwrapper_ here to activate ``gluster_bridge`` `python
virtual enviroment`_. This way, we install *gluster bridge* into the same virtual
enviroment which we have created during installation of *bridge common*.

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/
.. _`python virtual enviroment`: https://virtualenv.pypa.io/en/stable/

4. Create config file::

    $ cp etc/tendrl/tendrl.conf.sample /etc/tendrl/tendrl.conf
    $ cp etc/logging.yaml.timedrotation.sample /etc/tendrl/gluster_bridge_logging.yaml

5. Edit ``/etc/tendrl/tendrl.conf`` as below

    Set the value of ``log_cfg_path`` under section ``bridge_common``

    ``log_cfg_path = /etc/tendrl/common_logging.yaml``

    Set the value of ``log_cfg_path`` under section ``gluster_bridge``

    ``log_cfg_path = /etc/tendrl/gluster_bridge_logging.yaml``

6. Create log dir::

    $ mkdir /var/log/tendrl/common
    $ mkdir /var/log/tendrl/gluster_bridge

7. Run::
    $ tendrl-gluster-bridge
