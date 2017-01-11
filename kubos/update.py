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
import git
import json
import logging
import sys
import time
import os

from kubos.utils.git_common import *
from kubos.utils.sdk import *
from kubos.utils import status_spinner
from kubos import versions
from yotta.options import parser

def addOptions(parser):
    parser.add_argument('set_version', nargs='?', default=None, help='Specify a version of the kubos source to use.')


def execCommand(args, following_args):
    if not os.path.isdir(KUBOS_DIR):
        os.makedirs(KUBOS_DIR)
    os.chdir(KUBOS_DIR)
    print 'Checking for the most recent KubOS Source...'
    spinner = status_spinner.start_spinner()
    src_repo = clone_repo(KUBOS_SRC_DIR, KUBOS_SRC_URL)
    clone_example_repo(KUBOS_EXAMPLE_DIR, KUBOS_EXAMPLE_URL)
    status_spinner.stop_spinner(spinner)
    set_version = vars(args)['set_version']
    if set_version:
        check_provided_version(set_version, src_repo)


def clone_example_repo(repo_dir, repo_url):
    '''
    For the example repo (kubos-rt-example) we simply checkout
    the latest version, rather than making the user specify a 
    specific version of the example repo.
    '''
    repo = clone_repo(repo_dir, repo_url)
    tag_list = versions.get_tag_list(repo)
    latest_tag = versions.get_latest_tag(tag_list)
    checkout(latest_tag, repo)


def clone_repo(repo_dir, repo_url):
    try:
        if not os.path.isdir(repo_dir):
            repo = git.Repo.clone_from(repo_url, repo_dir)
            print 'Successfully cloned repo: %s' % repo_url
        else:
            repo = git.Repo(repo_dir)
            print 'Repo %s already exists' % repo_url
        fetch_tags(repo)
        #Link the modules/targets from the kubos repo to the default, Global location
        link_to_global_cache(KUBOS_SRC_DIR)
        return repo
    except git.exc.GitCommandError as e:
        print 'Error: there was an error accessing the remote git repository...'
        print >>sys.stderr, 'The specific error is: \n\n %s' % e




