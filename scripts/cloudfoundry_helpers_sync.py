#!/usr/bin/env python
# Copyright 2013 Canonical Ltd.

# Authors:
#   Adam Gandelman <adamg@ubuntu.com>

import logging
import optparse
import os
import subprocess
import shutil
import sys
import tempfile
import yaml

from fnmatch import fnmatch

CHARM_HELPERS_BRANCH = 'lp:cloudfoundry'


def parse_config(conf_file):
    if not os.path.isfile(conf_file):
        logging.error('Invalid config file: %s.' % conf_file)
        return False
    return yaml.load(open(conf_file).read())


def clone_helpers(work_dir, branch):
    dest = os.path.join(work_dir, )
    logging.info('Checking out %s to %s.' % (branch, dest))
    cmd = ['bzr', 'branch', branch, dest]
    subprocess.check_call(cmd)
    return dest


def _module_path(module):
    return os.path.join(*module.split('.'))


def _src_path(src, module):
    return os.path.join(src, 'charmhelpers', _module_path(module))


def _dest_path(dest, module):
    return os.path.join(dest, _module_path(module))


def _is_pyfile(path):
    return os.path.isfile(path + '.py')


def ensure_init(path):
    '''
    ensure directories leading up to path are importable, omitting
    parent directory, eg path='/hooks/helpers/foo'/:
        hooks/
        hooks/helpers/__init__.py
        hooks/helpers/foo/__init__.py
    '''
    for d, dirs, files in os.walk(os.path.join(*path.split('/')[:2])):
        _i = os.path.join(d, '__init__.py')
        if not os.path.exists(_i):
            logging.info('Adding missing __init__.py: %s' % _i)
            open(_i, 'wb').close()


def sync_pyfile(src, dest):
    src = src + '.py'
    src_dir = os.path.dirname(src)
    logging.info('Syncing pyfile: %s -> %s.' % (src, dest))
    if not os.path.exists(dest):
        os.makedirs(dest)
    shutil.copy(src, dest)
    if os.path.isfile(os.path.join(src_dir, '__init__.py')):
        shutil.copy(os.path.join(src_dir, '__init__.py'),
                    dest)
    ensure_init(dest)


def get_filter(opts=None):
    opts = opts or []
    if 'inc=*' in opts:
        # do not filter any files, include everything
        return None

    def _filter(dir, ls):
        incs = [opt.split('=').pop() for opt in opts if 'inc=' in opt]
        _filter = []
        for f in ls:
            _f = os.path.join(dir, f)

            if not os.path.isdir(_f) and not _f.endswith('.py') and incs:
                if True not in [fnmatch(_f, inc) for inc in incs]:
                    logging.debug('Not syncing %s, does not match include '
                                  'filters (%s)' % (_f, incs))
                    _filter.append(f)
                else:
                    logging.debug('Including file, which matches include '
                                  'filters (%s): %s' % (incs, _f))
            elif (os.path.isfile(_f) and not _f.endswith('.py')):
                logging.debug('Not syncing file: %s' % f)
                _filter.append(f)
            elif (os.path.isdir(_f) and not
                  os.path.isfile(os.path.join(_f, '__init__.py'))):
                logging.debug('Not syncing directory: %s' % f)
                _filter.append(f)
        return _filter
    return _filter


def sync_directory(src, dest, opts=None):
    if os.path.exists(dest):
        logging.debug('Removing existing directory: %s' % dest)
        shutil.rmtree(dest)
    logging.info('Syncing directory: %s -> %s.' % (src, dest))

    shutil.copytree(src, dest, ignore=get_filter(opts))
    ensure_init(dest)


def sync(src, dest, module, opts=None):
    if os.path.isdir(_src_path(src, module)):
        sync_directory(_src_path(src, module), _dest_path(dest, module), opts)
    elif _is_pyfile(_src_path(src, module)):
        sync_pyfile(_src_path(src, module),
                    os.path.dirname(_dest_path(dest, module)))
    else:
        logging.warn('Could not sync: %s. Neither a pyfile or directory, '
                     'does it even exist?' % module)


def parse_sync_options(options):
    if not options:
        return []
    return options.split(',')


def extract_options(inc, global_options=None):
    global_options = global_options or []
    if global_options and isinstance(global_options, basestring):
        global_options = [global_options]
    if '|' not in inc:
        return (inc, global_options)
    inc, opts = inc.split('|')
    return (inc, parse_sync_options(opts) + global_options)


def sync_helpers(include, src, dest, options=None):
    source_folder = options['source_folder'] if options['source_folder'] else 'cloudfoundry'

    if not os.path.isdir(dest):
        os.mkdir_p(dest)

    for inc in include:
        if isinstance(inc, str):
            inc, opts = extract_options(inc, global_options)
            sync(src, dest, inc, opts)
        elif isinstance(inc, dict):
            # could also do nested dicts here.
            for k, v in inc.iteritems():
                if isinstance(v, list):
                    for m in v:
                        inc, opts = extract_options(m, global_options)
                        sync(src, dest, '%s.%s' % (k, inc), opts)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-c', '--config', action='store', dest='config',
                      default=None, help='helper config file')
    (opts, args) = parser.parse_args()

    config_path = opts.config if opts.config else 'cloudfoundry-helpers.yaml'

    logging.info('Loading cloudfoundry helper from %s.' % config_path)
    config = parse_config(config_path)
    if not config:
        logging.error('Could not parse config from %s.' % opts.config)
        sys.exit(1)

    if 'destination' not in config:
        logging.error('No destination dir. specified as option or config.')
        sys.exit(1)

    tmpd = tempfile.mkdtemp()

    try:
        checkout = clone_helpers(tmpd, config['branch'])
        sync_helpers(config['include'], checkout, config['destination'],
                     options=sync_options)
    except Exception, e:
        logging.error("Could not sync: %s" % e)
        raise e
    finally:
        logging.debug('Cleaning up %s' % tmpd)
        shutil.rmtree(tmpd)
