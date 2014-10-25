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
juju add-relation admin-ui cc
juju add-relation admin-ui:ccdb cc:ccdb
juju add-relation admin-ui uaa
juju add-relation admin-ui:uaadb uaa:uaadb
```




