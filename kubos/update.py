# Kubos SDK
# Copyright (C) 2016 Kubos Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import logging
import sys
import subprocess
import time
import os

from yotta.options import parser

from kubos.utils import git_utils, \
                        sdk_utils, \
                        status_spinner
from kubos.utils.constants import *

KUBOS_CLI_REPO_URL = 'git+https://github.com/kubostech/kubos-cli'
INSTALL_COMMAND    = ['sudo', 'pip', 'install', '--upgrade', KUBOS_CLI_REPO_URL]

def addOptions(parser):
    parser.add_argument('set_version', nargs='?', default=None, help='Specify a version of the kubos source to use.')
    parser.add_argument('-l', '--latest', action='store_true', default=False, help='Default to the most recent release of Kubos modules')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--source',  dest='component', action='store_const', const='s', default=False, help='Update only the source Kubos modules')
    group.add_argument('-c', '--cli',     dest='component', action='store_const', const='c', default=False, help='Update the Kubos CLI.')
    group.add_argument('-a', '--all',     dest='component', action='store_const', const='a', default=False, help='Update both the Kubos source modules and the Kubos CLI')
    #The default behavior is to only update the source modules.
    parser.set_defaults(component='s')


def execCommand(args, following_args):
    if args.component == 'a' or args.component == 's':
        update_source_modules(args)
    # TODO: I don't think this a check can ever be reached
    if args.component == 'a' or args.component == 'c':
        update_cli()


def update_cli():
    logging.info('Updating the Kubos CLI...')
    return_code = subprocess.check_call(INSTALL_COMMAND)
    if return_code == 0:
        logging.info('Succesfully updated the Kubos CLI module')
    else:
        #The subprocess stdout/stderr is printed to the console. Any errors that occurr will be visible there.
        logging.error('There was an issue updating the Kubos CLI module. See the above log for the error details.')


def update_source_modules(args):
    if not os.path.isdir(KUBOS_DIR):
        os.makedirs(KUBOS_DIR)
    os.chdir(KUBOS_DIR)
    logging.info('Checking for the most recent KubOS Source...')
    spinner = status_spinner.start_spinner()
    src_repo = git_utils.clone_repo(KUBOS_SRC_DIR, KUBOS_SRC_URL)
    git_utils.clone_example_repo(KUBOS_RT_EXAMPLE_DIR, KUBOS_RT_EXAMPLE_URL)
    git_utils.clone_example_repo(KUBOS_LINUX_EXAMPLE_DIR, KUBOS_LINUX_EXAMPLE_URL)
    status_spinner.stop_spinner(spinner)
    set_version = args.set_version
    if set_version:
        logging.info('Setting provided release: %s' % set_version)
        git_utils.check_provided_version(set_version, src_repo)
    if args.latest:
        latest_tag = git_utils.get_latest_tag(git_utils.get_tag_list(src_repo))
        logging.info('Setting latest release: %s' % latest_tag)
        git_utils.check_provided_version(latest_tag, src_repo)
