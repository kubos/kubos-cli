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
from kubos import versions
from packaging import version
from yotta import link, link_target
from yotta.lib import detect
from yotta.options import parser

def addOptions(parser):
    parser.add_argument('set_version', nargs='?', default=None, help='Specify a version of the kubos source to use.')


def execCommand(args, following_args):
    if os.geteuid() != 0:
        #After changing the version the new target/modules are re-linked to /usr/local/lib.. which requires root to succeed
        print 'Woops, this command needs to be run as root. Please re-run `sudo kubos update`'
        sys.exit(1)
    if not os.path.isdir(KUBOS_DIR):
        os.makedirs(KUBOS_DIR)
    os.chdir(KUBOS_DIR)
    src_repo = clone_repo(KUBOS_SRC_DIR, KUBOS_SRC_URL)
    clone_example_repo(KUBOS_EXAMPLE_DIR, KUBOS_EXAMPLE_URL)
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
        fetch_new_tags(repo)
        return repo
    except git.exc.GitCommandError as e:
        print 'Error: there was an error accessing the remote git repository...'
        print 'The specific error is: \n\n %s' % e


def fetch_new_tags(repo):
    origin = repo.remotes.origin
    tag_list = []
    latest_tag = ""
    print 'Checking for newer releases...'
    origin.fetch(tags=True)
    relink_modules(KUBOS_SRC_DIR)


def relink_modules(path):
    logging.disable(logging.WARNING)
    for subdir in os.listdir(path):
        cur_dir = os.path.join(path, subdir)
        if os.path.isdir(cur_dir):
            relink_modules(cur_dir)
        elif subdir == 'module.json':
            link_module_globally(cur_dir)
        elif subdir == 'target.json':
            link_target_globally(cur_dir)


def link_target_globally(path):
    path = os.path.dirname(path)
    start_dir = os.getcwd()
    os.chdir(path)
    link_target_args = argparse.Namespace(target_or_path=None,
                                          config=None,
                                          target=detect.kubosDefaultTarget(),
                                          save_global=True,
                                          no_install=False)
    link_target.execCommand(link_target_args, '')
    os.chdir(start_dir)


def link_module_globally(path):
    start_dir = os.getcwd()
    path_dir_name = os.path.dirname(path)
    os.chdir(path_dir_name)
    link_args = argparse.Namespace(module_or_path=None,
                                   config=None,
                                   target=detect.kubosDefaultTarget())
    link.execCommand(link_args, None)
    os.chdir(start_dir)


def check_provided_version(requested_version, repo):
    #the repo paramenter allows this function to be used for the example project as well
    active_version = get_active_kubos_version()
    if requested_version == active_version:
        print 'The requested version: %s is already active. There\'s nothing to do..' % requested_version
        return
    #verify_action_with_user(requested_version, repo)
    set_active_version(requested_version, repo)
    if active_version:
        print 'Deactivating Kubos source version: %s' % active_version
    print '\nActivating Kubos source version %s' % requested_version


def set_active_version(set_tag, repo):
    origin = repo.remotes.origin
    tag_list = versions.get_tag_list(repo)
    found = False
    for tag in tag_list:
        if tag.name == set_tag:
            checkout(tag, repo)
            found = True
            break
    if not found:
        print >>sys.stderr, '\nThe requested version "%s" is not an avaialble version.' % set_tag
        print >>sys.stderr, 'Available versions are: '
        versions.print_tag_list(tag_list)
        sys.exit(1)


def checkout(tag, repo):
    try:
        repo.git.checkout(tag.name)
        if repo.git_dir == os.path.join(KUBOS_SRC_DIR, '.git'): #only set the version file for kubos source checkouts, not for example checkouts
            with open(KUBOS_VERSION_FILE, 'w') as version_file:
                version_file.write(tag.name)
    except:
        print 'There was an error checking out the tag "%s"' % tag.name
        print 'The error details are: \n\n%s' %  sys.exc_info()[0]

