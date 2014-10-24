#!/usr/bin/python

import os
import sys

sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], 'lib'))

from charmhelpers.core import ( hookenv, host )
import charmhelpers.fetch.giturl

import charmhelpers.core.services
import cloudfoundry.contexts

from charmhelpers.core.services import RelationContext

hooks = hookenv.Hooks()
log = hookenv.log

SERVICE = 'admin-ui'

manager = services.ServiceManager([
    {
        'service': 'admin-ui',
        'ports': [8070],
        'required_data': [
            contexts.NatsRelation,
            contexts.CloudFoundryCredentials, 
            # contexts.RouterRelation, 
            contexts.UAARelation,
            contexts.UAADBRelation,
            contexts.CloudControllerDBRelation
        ],
        'data_ready': [
            services.template(source='admin-ui.conf',
                              target='/etc/init',
                              owner='logstash', perms=0400),
            services.template(source='default.yml',
                              target='/etc/init',
                              owner='logstash', perms=0400),
        ],
        'start': upstart_start('admin-ui'),
        'stop': upstart_stop('admin-ui')
    }
])


@hooks.hook('install')
def install():
    manager.manage()


@hooks.hook('config-changed')
def config_changed():
    log('Config changed hook is called.')
    manager.manage()


@hooks.hook('upgrade-charm')
def upgrade_charm():
    log('Upgrading admin-ui.')
    manager.manage()


@hooks.hook('start')
def start():
    log('Start admin-ui.')
    manager.manage()
    # host.service_restart(SERVICE) or host.service_start(SERVICE)


@hooks.hook('stop')
def stop():
    log('Stop admin-ui.')
    manager.manage()
    # host.service_stop(SERVICE)


if __name__ == "__main__":
    # execute a hook based on the name the program is called by
    hooks.execute(sys.argv)

