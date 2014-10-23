Overview
========

This charm provides the Cloud Foundry [Administration Web UI](https://github.com/cloudfoundry-incubator/admin-ui/blob/master/README.md).

The Administration Web UI provides metrics and operations data for Cloud Foundry NG. It gathers data from the varz providers for the various Cloud Foundry components as well as from the Cloud Controller and UAA REST APIs.

In order to execute, the Administration UI needs to be able to access the following resources:
- NATS
- Cloud Controller REST API

You can find charms to install them here: cf-nats charm, cf-cloud-controller charm


Usage
=====
Obviously used in a bundle with other CF components.
To deploy the DEA service:
```
git clone ...
juju deploy --repository ../cf-admin-ui admin-ui
juju add-relation admin-ui nats
juju add-relation admin-ui cc
<!-- juju add-relation admin-ui uaa -->
```





