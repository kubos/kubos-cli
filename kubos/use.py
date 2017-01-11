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

import git
import sys

from kubos.utils.sdk import *
from kubos.utils.git_common import *
from kubos import versions
from yotta import target
from yotta.options import parser


def addOptions(parser):
    parser.add_argument('set_version', nargs=1, help='Set a specific version of the KubOS modules to build your projects against.')

def execCommand(args, following_args):
    args = vars(args)
    version = args['set_version'][0]
    kubos_repo, origin = get_repo(KUBOS_SRC_DIR)
    check_provided_version(version, kubos_repo)

def check_provided_version(requested_version, repo):
    #the repo paramenter allows this function to be used for the example project as well
    active_version = get_active_kubos_version()
    if requested_version == active_version:
        logging.info('The requested version: %s is already active. There\'s nothing to do..' % requested_version)
        return
    set_active_kubos_version(requested_version, repo)
    if active_version:
        logging.info('Deactivating Kubos source version: %s' % active_version)
    logging.info('\nActivating Kubos source version %s' % requested_version)


def set_active_kubos_version(set_tag, repo):
    origin = repo.remotes.origin
    tag_list = versions.get_tag_list(repo)
    found = False
    for tag in tag_list:
        if tag.name == set_tag:
            checkout_and_update_version_file(tag, repo)
            found = True
            break
    if not found:
        logging.error('The requested version "%s" is not an avaialble version.' % set_tag)
        logging.info('Available versions are: ')
        versions.print_tag_list(tag_list)
        sys.exit(1)

