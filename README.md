Overview
========

This charm provides the Cloud Foundry [Administration Web UI](https://github.com/cloudfoundry-incubator/admin-ui/blob/master/README.md).

The Administration Web UI provides metrics and operations data for Cloud Foundry NG. It gathers data from the varz providers for the various Cloud Foundry components as well as from the Cloud Controller and UAA REST APIs.

In order to execute, the Administration UI needs to be able to access the following resources:
- NATS
- Cloud Controller DB
- UAA 
- UAA DB

You can find charms to install them here: cf-nats charm, cf-cloud-controller charm


Usage
=====
Obviously used in a bundle with other CF components deployed with juju charms.
To deploy the DEA service:
```bash
# create folder structure
mkdir trusty
git clone https://github.com/Altoros/admin-ui-juju-charm.git trusty/admin-ui
# deploy admin-ui charm
juju deploy --repository . local:trusty/admin-ui admin-ui
juju add-relation admin-ui nats
juju add-relation admin-ui:cc cc:cc
juju add-relation admin-ui:ccdb cc:ccdb
juju add-relation admin-ui:uaa uaa:uaa
juju add-relation admin-ui:uaadb uaa:uaadb
juju add-relation admin-ui cloudfoundry
```

Set uaa access properties:
```
gem install cf-uaac --no-ri --no-rdoc

DOMAIN=10.244.0.34.xip.io
ADMIN_SECRET=

uaac target http://uaa.$DOMAIN
uaac token client get admin -s $ADMIN_SECRET

# Add 'scim.write' if not already there and re-get token
uaac client update admin --authorities "`uaac client get admin | \
    awk '/:/{e=0}/authorities:/{e=1;if(e==1){$1="";print}}'` scim.write"
uaac token client get admin -s $ADMIN_SECRET

# Create a new group and add the 'admin' user to it
uaac group add admin_ui.admin
uaac member add admin_ui.admin admin

# Create the new UAA admin_ui_client
uaac client add admin_ui_client \
 --authorities cloud_controller.admin,cloud_controller.read,cloud_controller.write,openid,scim.read \
 --authorized_grant_types authorization_code,client_credentials,refresh_token \
 --autoapprove true \
 --scope admin_ui.admin,admin_ui.user,openid \
 -s admin_ui_secret
```
