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
from kubos import version as kubos_version
from options import parser
from packaging import version
from yotta import link, link_target
from yotta.lib import detect

def addOptions(parser):
    pass


def execCommand(args, following_args):
    if os.geteuid() != 0:
        #After changing the version the new target/modules are re-linked to /usr/local/lib.. which requires root to succeed
        print 'Woops, this command needs to be run as root. Please re-run `sudo kubos update`'
        sys.exit(1)
    if not os.path.isdir(KUBOS_DIR):
        os.makedirs(KUBOS_DIR)
    os.chdir(KUBOS_DIR)
    try:
        if not os.path.isdir(KUBOS_SRC_DIR):
            repo = git.Repo.clone_from(KUBOS_SRC_URL, KUBOS_SRC_DIR)
            print 'Successfully Pulled Kubos Source Repo'
        else:
            repo = git.Repo(KUBOS_SRC_DIR)
            print 'Kubos Source Repo already exists'
        origin = repo.remotes.origin
        tag_list = []
        latest_tag = ""
        print 'Checking for newer KubOS source releases...'
        origin.fetch(tags=True)
        setattr(args, 'set_version', None)
        kubos_version.execCommand(args, following_args)
    except git.exc.GitCommandError as e:
        print 'Error: there was an error accessing the remote git repository...'
        print 'The specific error is: \n\n %s' % e
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
    with open(path, 'r') as json_file:
        data = json.load(json_file)
        module_name = data['name']
    link_args = argparse.Namespace(module_or_path=path_dir_name,
                                   config=None,
                                   target=detect.kubosDefaultTarget())
    link.execCommand(link_args, None)
    os.chdir(start_dir)

