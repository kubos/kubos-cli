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
import os

#Includes all of the sdk path variables
from kubos.utils.git_common import *
from kubos.versions import get_tag_list, print_tag_list
from packaging import version
from pip.utils import get_installed_version
from yotta.options import parser

def addOptions(parser):
    pass


def execCommand(args, following_args):
    kubos_version = get_active_kubos_version()
    print 'Kubos-CLI version    : %s' % get_installed_version('kubos-cli')
    print 'Kubos Source version : %s' % kubos_version
    if not kubos_version:
        repo, origin = get_repo(KUBOS_SRC_DIR)
        version_list = get_tag_list(repo)
        print '\nThere\'s not an active Kubos source version..'
        print 'The available versions are:'
        print_tag_list(version_list)
        print 'Please run kubos update <version> (with one of the above versions)' + \
              'to checkout a version of the source before working with a project.'

