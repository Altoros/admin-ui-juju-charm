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
    apt_install(packages=filter_installed_packages(config.ADMIN_UI_PACKAGES), fatal=True)
    host.adduser('vcap')
    host.mkdir(config.CF_DIR, owner='vcap', group='vcap', perms=0775)
    repo = git.clone(charm_config['repository'], config.ADMIN_UI_DIR, charm_config['branch'])
    if bool(charm_config['commit']):
        repo.head.reference = charm_config['commit']
        repo.head.reset(index=True, working_tree=True)
    subprocess.check_call(['bundle', 'install', '--standalone', 
                                                '--without', 'test', 'development'], cwd=config.ADMIN_UI_DIR)


@hooks.hook('upgrade-charm')
def upgrade_charm():
    log('Upgrading admin-ui.')


if __name__ == "__main__":
    if hookenv.hook_name() == 'install':
        hooks.execute(sys.argv)
    else:
        manager.manage()

