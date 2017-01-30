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
import logging
import packaging.version
import re
import os
import sys

from kubos.utils import sdk_utils
from kubos.utils.constants import *

def get_repo(path):
    repo = git.Repo(path)
    return repo


def get_tag_list(repo):
    tags = repo.tags
    tag_list = []
    for tag in tags:
        tag_list.append(tag)
    return tag_list


def print_tag_list(tag_list):
    active_version = get_active_kubos_version()
    for tag in tag_list:
        tag_name = tag.name #tag.name is immutable...
        if tag.name == active_version:
            tag_name = tag.name + ' *'
        logging.info(tag_name)


def get_latest_tag(tag_list):
    latest_tag = git.TagReference("", "", check_path=False) #Set to a dummy tag that will be less than any other valid tag
    for tag in tag_list:
        if packaging.version.parse(tag.name) > packaging.version.parse(latest_tag.name):
            latest_tag = tag
    return latest_tag


def fetch_tags(repo):
    origin = repo.remotes.origin
    logging.info('Checking for newer releases...') #Tags mark new KubOS releases
    origin.fetch()


def checkout_and_update_version(ref, repo):
    tag_expr = re.compile('v+\d\.+\d\.+\d\.*') #Tags follow the vX.X.X convention
    is_tag = tag_expr.match(ref)
    logging.info("Checking out '%s'" % ref)
    if not is_tag:
        logging.warning('Kubos branches are not guaranteed to be stable. Proceed with caution.')
    try:
        repo.git.checkout(ref)
        if repo.git_dir == os.path.join(KUBOS_SRC_DIR, '.git'): #only set the version file for kubos source checkouts, not for example checkouts
            update_version_file(ref)
    except:
        logging.error('There was an error checking out branch "%s"' % ref)
        logging.debug('The error details are: %s' %  sys.exc_info()[0])


def update_version_file(version):
    with open(KUBOS_VERSION_FILE, 'w') as version_file:
        version_file.write(version)


def clone_example_repo(repo_dir, repo_url):
    '''
    For the example repos (kubos-rt-example, kubos-linux-example) we 
    simply checkout the latest version, rather than making the user 
    specify a specific version of the example repo.
    '''
    repo = clone_repo(repo_dir, repo_url)
    tag_list   = get_tag_list(repo)
    latest_tag = get_latest_tag(tag_list)
    checkout_and_update_version(latest_tag.name, repo)


def clone_repo(repo_dir, repo_url):
    try:
        if not os.path.isdir(repo_dir):
            repo = git.Repo.clone_from(repo_url, repo_dir)
            logging.info('Successfully cloned repo: %s' % repo_url)
        else:
            repo = git.Repo(repo_dir)
            logging.info('Repo %s already exists' % repo_url)
        fetch_tags(repo)
        #Link the modules/targets from the kubos repo to the default, Global location
        sdk_utils.link_to_global_cache(KUBOS_SRC_DIR)
        return repo
    except git.exc.GitCommandError as e:
        logging.error('Error: there was an error accessing the remote git repository...')
        logging.debug('The specific error is: \n\n %s' % e)


def get_active_kubos_version():
    if os.path.isfile(KUBOS_VERSION_FILE):
        return open(KUBOS_VERSION_FILE).read()
    else:
        return None


def set_active_kubos_version(set_tag, repo):
    origin = repo.remotes.origin
    tag_list = get_tag_list(repo)
    found = False
    for tag in tag_list:
        if tag.name == set_tag:
            checkout_and_update_version(tag.name, repo)
            found = True
            break
    if not found:
        logging.error('The requested version "%s" is not an available version.' % set_tag)
        logging.info('Available versions are: ')
        print_tag_list(tag_list)
        sys.exit(1)


def check_provided_version(requested_version, repo):
    #the repo paramenter allows this function to be used for the example project as well
    active_version = get_active_kubos_version()
    if requested_version == active_version:
        logging.info('The requested version: %s is already active. There\'s nothing to do..' % requested_version)
        return
    set_active_kubos_version(requested_version, repo)
    if active_version:
        logging.info('Deactivating Kubos source version: %s' % active_version)
    logging.info('Activating Kubos source version %s' % requested_version)

