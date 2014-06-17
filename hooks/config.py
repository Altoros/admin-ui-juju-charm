import os
from charmhelpers.core import hookenv
from charmhelpers.core import services
from charmhelpers.contrib.cloudfoundry import contexts

__all__ = ['ADMIN_UI_PACKAGES', 'CF_DIR', 'ADMIN_UI_DIR',
           'ADMIN_UI_CONFIG_PATH']

ADMIN_UI_PACKAGES = ['git', 'ruby1.9.3']

CF_DIR = '/var/lib/cloudfoundry'
ADMIN_UI_DIR = os.path.join(CF_DIR, 'cfadminui')
ADMIN_UI_CONFIG_PATH = os.path.join(ADMIN_UI_DIR, 'config', 'default.yml')


SERVICES = [
    {
        'service': 'cf-admin-ui',
        'required_data': [contexts.NatsRelation(),
                          contexts.CloudControllerRelation(),
                          hookenv.config()],
        'data_ready': [
            services.template(source='cf-admin-ui.conf',
                              target='/etc/init/cf-admin-ui.conf'),
            services.template(source='default.yml',
                              target=ADMIN_UI_CONFIG_PATH),
        ]
    }
]
