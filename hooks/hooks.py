#!/usr/bin/python

import os
import sys

sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], 'lib'))

from charmhelpers.core import (
    hookenv,
    host
)

import charmhelpers.core.services
from charmhelpers.core.services import RelationContext

hooks = hookenv.Hooks()
log = hookenv.log

SERVICE = 'admin-ui'

manager = services.ServiceManager([
    {
        'service': 'admin-ui',
        # 'ports': [80, 443],
        'required_data': [, {'basepath': '/opt/logstash'}],
        'data_ready': [
            services.template(source='admin-ui.conf',
                              target='/etc/init',
                              owner='logstash', perms=0400),
            services.template(source='admin-ui.conf',
                              target='/etc/init',
                              owner='logstash', perms=0400),
        ],
    },
    {
        'service': 'spadesd',
        'data_ready': services.template(source='spadesd_run.j2',
                                        target='/etc/sv/spadesd/run',
                                        perms=0555),
        'start': runit_start,
        'stop': runit_stop,
    },
])


@hooks.hook('install')
def install():
    # manager.manage()
    


@hooks.hook('config-changed')
def config_changed():
    config = hookenv.config()

    for key in config:
        if config.changed(key):
            log("config['{}'] changed from {} to {}".format(
                key, config.previous(key), config[key]))

    config.save()
    start()


@hooks.hook('upgrade-charm')
def upgrade_charm():
    log('Upgrading admin-ui')


@hooks.hook('start')
def start():
    host.service_restart(SERVICE) or host.service_start(SERVICE)


@hooks.hook('stop')
def stop():
    host.service_stop(SERVICE)


if __name__ == "__main__":
    # execute a hook based on the name the program is called by
    # hooks.execute(sys.argv)
    manager.manage()
