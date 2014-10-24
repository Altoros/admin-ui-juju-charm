import os
sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], 'lib'))

from charmhelpers.core import ( hookenv, host, services )
from cloudfoundry import contexts

__all__ = ['ADMIN_UI_PACKAGES', 'CF_DIR', 'ADMIN_UI_DIR',
           'ADMIN_UI_CONFIG_PATH', 'SERVICE']

ADMIN_UI_PACKAGES = ['git', 'ruby1.9.3', 'bundler',
                     'libmysqlclient-dev', 'libsqlite3-dev', 'libpq-dev']

CF_DIR = '/var/lib/cloudfoundry'
ADMIN_UI_DIR = os.path.join(CF_DIR, 'admin-ui')
ADMIN_UI_CONFIG_PATH = os.path.join(ADMIN_UI_DIR, 'config', 'default.yml')

upstart_template_context = {'working_directory': ADMIN_UI_DIR, 'config_path': ADMIN_UI_CONFIG_PATH, 
                            'user': 'vcap', 'group', 'vcap'}

SERVICE = [
    {
        'service': 'admin-ui',
        'required_data': [contexts.NatsRelation(),
                          contexts.CloudControllerRelation,
                          contexts.CloudControllerDBRelation,
                          contexts.UAARelation,
                          contexts.UAADBRelation,
                          hookenv.config(),
                          upstart_template_context],
        'data_ready': [
            services.template(source='admin-ui.conf',
                              target='/etc/init/admin-ui.conf'),
            services.template(source='default.yml',
                              target=ADMIN_UI_CONFIG_PATH),
        ]
    }
]
