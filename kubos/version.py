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
    repo, origin = get_repo(KUBOS_SRC_DIR)
    check_provided_version(requested_version, repo)


def check_provided_version(requested_version, repo):
    #the repo paramenter allows this function to be used for the example project as well
    if not requested_version:
        print 'No version requested - Defaulting to the most recent release'
        requested_version = get_latest_tag(get_tag_list(repo))
    active_version = get_active_version()
    if requested_version == active_version:
        print 'The requested version: %s is already active. There\'s nothing to do..' % requested_version
        return
    verify_action_with_user(requested_version, repo)
    set_active_version(requested_version, repo)
    if active_version:
        print 'Deactivating version: %s' % active_version
    print '\nActivating version %s' % requested_version


def verify_action_with_user(requested_version, repo):
    if 'example' in repo.git_dir: #Skip user input for the example repo - Check out the lastest tag of kubos-rt-example
        return
    yes = set(['yes','ye', 'y'])
    print '\nThis will checkout version %s of the Kubos Source... continue? [y/n]' % requested_version
    response = raw_input().lower()
    if response not in yes:
        print 'Didn\'t receive a yes response from the user.. Aborting.'
        sys.exit(1)


def set_active_version(set_tag, repo):
    origin = repo.remotes.origin
    tag_list = get_tag_list(repo)
    found = False
    for tag in tag_list:
        if tag.name == set_tag:
            checkout(tag, repo)
            found = True
            break
    if not found:
        print >>sys.stderr, '\nThe requested version "%s" is not an avaialble version.' % set_tag
        print >>sys.stderr, 'Available versions are: '
        print_tag_list(tag_list)
        sys.exit(1)


def checkout(tag, repo):
    try:
        repo.git.checkout(tag.name)
        if repo.git_dir == os.path.join(KUBOS_SRC_DIR, '.git'):
            with open(KUBOS_VERSION_FILE, 'w') as version_file:
                version_file.write(tag.name)
    except:
        print 'There was an error checking out the tag "%s"' % tag.name
        print 'The error details are: \n\n%s' %  sys.exc_info()[0]

