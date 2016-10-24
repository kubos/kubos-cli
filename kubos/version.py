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
from kubos.versions import get_tag_list, print_tag_list, get_latest_tag
from packaging import version
from yotta.options import parser

def addOptions(parser):
    parser.add_argument('set_version', nargs='?', help='specify the desired KubOS Source version to set')


def execCommand(args, following_args):
    requested_version = vars(args)['set_version']
    if not requested_version:
        print 'No version requested - Defaulting to the most recent release'
        requested_version = get_latest_tag(get_tag_list())
    active_version = get_active_version()
    if requested_version == active_version:
        print 'The requested version: %s is already active. There\'s nothing to do..' % requested_version
        return
    set_active_version(requested_version)
    if active_version:
        print 'Changing from version: %s' % active_version
    print 'Activating version %s' % requested_version


def set_active_version(set_tag):
    repo, origin = get_kubos_repo()
    tag_list = get_tag_list()
    found = False
    for tag in tag_list:
        if tag.name == set_tag:
            checkout(tag)
            found = True
            break
    if not found:
        print >>sys.stderr, 'The requested version "%s" is not an avaialble version.' % set_tag
        print >>sys.stderr, 'Available versions are: '
        print_tag_list(tag_list)
        sys.exit(1)


def checkout(tag):
    repo, origin = get_kubos_repo()
    try:
        repo.git.checkout(tag.name)
        with open(KUBOS_VERSION_FILE, 'w') as version_file:
            version_file.write(tag.name)
    except:
        print 'There was an error checking out the tag "%s"' % tag.name
        print 'The error details are: \n\n%s' %  sys.exc_info()[0]

