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
import os
import shutil
import sys

from yotta import link, link_target
from yotta.lib import folders
from yotta.lib.detect import systemDefaultTarget

from kubos.utils.constants import KUBOS_RT_EXAMPLE_DIR, KUBOS_LINUX_EXAMPLE_DIR, KUBOS_SRC_DIR
from kubos.utils import sdk_utils

def addOptions(parser):
    parser.add_argument('proj_name', nargs=1, help='specify the project name')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--linux', action='store_true', help='Initialize Kubos SDK project for KubOS Linux')
    group.add_argument('-r', '--rt', action='store_true', default=True, help='Initialize Kubos SDK project for KubOS RT')

def execCommand(args, following_args):
    proj_name = vars(args)['proj_name'][0] #vars returns a dict of args. proj_name is a list since nargs=1
    logging.info('Initializing project: %s ...' % proj_name)
    proj_name_dir = os.path.join(os.getcwd(), proj_name)

    if os.path.isdir(proj_name_dir):
        logging.warning('The project directory %s already exists. Not overwritting the current directory' % proj_name_dir)
        sys.exit(1)

    #Copy in the correct example directory based on the desired OS
    example_dir = KUBOS_LINUX_EXAMPLE_DIR if args.linux else KUBOS_RT_EXAMPLE_DIR
    shutil.copytree(example_dir, proj_name_dir, ignore=shutil.ignore_patterns('.git'))

    #change project name in module.json
    module_json = os.path.join(proj_name_dir, 'module.json')
    with open(module_json, 'r') as init_module_json:
        module_data = json.load(init_module_json)
    module_data['name'] = proj_name
    module_data['repository']['url'] = 'git://<repository_url>' #These fields print warnings if they're
    module_data['homepage'] = 'https://<homepage>'              #left empty
    with open(module_json, 'w') as final_module_json:
        str_module_data = json.dumps(module_data,
                                     indent=4,
                                     separators=(',', ':'))
        final_module_json.write(str_module_data)
    os.chdir(proj_name_dir)
    sdk_utils.link_global_cache_to_project(proj_name_dir)

def get_target_list():
    '''
    This is a helper function for getting a list of all the globally linked
    targets.
    '''
    global_target_path = folders.globalTargetInstallDirectory()
    target_list = os.listdir(global_target_path)
    available_target_list = []

    for subdir in target_list:
        target_json = os.path.join(global_target_path, subdir, 'target.json')
        with open(target_json, 'r') as json_file:
            data = json.load(json_file)
            available_target_list.append(data['name'])
    return available_target_list


