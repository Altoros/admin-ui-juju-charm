#!/usr/bin/python
# vim: et ai ts=4 sw=4:
import os
import sys
import subprocess
sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], 'lib'))

from charmhelpers.core import ( hookenv, host, services )
from charmhelpers.fetch import ( giturl, apt_install, filter_installed_packages )
from cloudfoundry import contexts
import config

hooks = hookenv.Hooks()
log = hookenv.log
git = giturl.GitUrlFetchHandler()
manager = services.ServiceManager(config.SERVICE)


@hooks.hook('install')
def install():
    charm_config = hookenv.config()
    host.adduser('vcap')
    host.mkdir(config.CF_DIR, owner='vcap', group='vcap', perms=0775)
    apt_install(packages=filter_installed_packages(config.ADMIN_UI_PACKAGES), fatal=True)
    repo = git.clone(charm_config['repository'], config.ADMIN_UI_DIR, 'master')
    repo.reset('--hard', charm_config['commit'])
    chdir(os.path.join(config.working_directory, 'admin-ui'))
    subprocess.check_call(['bundle', 'install', '--standalone', 
                                                '--without', 'test', 'development'], cwd=config.ADMIN_UI_DIR)



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


@hooks.hook('stop')
def stop():
    log('Stop admin-ui.')
    manager.manage()


if __name__ == "__main__":
    hooks.execute(sys.argv)

