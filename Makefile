CHARM_DIR := $(shell pwd)
TEST_TIMEOUT := 900

test: lint 

lint:
	@echo "Lint check (flake8)"
	@flake8 --exclude=hooks/charmhelpers hooks 
clean:
	find . -name '*.pyc' -delete
	find . -name '*.bak' -delete
run: uh lint deploy
vlog:
	view ~/.juju/local/log/unit-admin-ui-0.log
log:
	tail -f ~/.juju/local/log/unit-admin-ui-0.log
destroy:
	juju destroy-service admin-ui
deploy:

ifdef m
	juju deploy --to $(m) --repository=../../. local:trusty/cf-admin-ui admin-ui --show-log
else
	juju deploy --repository=../../. local:trusty/cf-admin-ui admin-ui --show-log
endif
uh:
	../../../helpers/update_helpers.py
upgrade:
	juju upgrade-charm --repository=../../. admin-ui --show-log
