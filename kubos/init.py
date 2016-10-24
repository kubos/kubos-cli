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

from kubos.utils.git_common import KUBOS_EXAMPLE_DIR
from yotta import link, link_target
from yotta.lib import folders
from yotta.lib.detect import systemDefaultTarget

def addOptions(parser):
    parser.add_argument('proj_name', nargs=1, help='specify the project name')


def execCommand(args, following_args):
    proj_name = vars(args)['proj_name'][0] #vars returns a dict of args. proj_name is a list since nargs=1
    print 'Initializing project: %s ...' % proj_name
    proj_name_dir = os.path.join(os.getcwd(), proj_name)

    if os.path.isdir(proj_name_dir):
        print >>sys.stderr, 'The project directory %s already exists. Not overwritting the current directory' % proj_name_dir
        sys.exit(1)

    shutil.copytree(KUBOS_EXAMPLE_DIR, proj_name_dir, ignore=shutil.ignore_patterns('.git'))
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
    link_kubos_modules()
    link_kubos_targets()


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


'''
logging.WARNING messages are disabled because we currently link all of
the kubos source to each project. Modules that aren't needed print
warning messages when they are linked.
'''
def link_kubos_modules():
    logging.disable(logging.WARNING)
    global_module_path = folders.globalInstallDirectory()
    default_target = systemDefaultTarget()
    for subdir in os.listdir(global_module_path):
        module_json = os.path.join(global_module_path, subdir, 'module.json')
        with open(module_json, 'r') as json_file:
            data = json.load(json_file)
            module_name = data['name']
        link_args = argparse.Namespace(module_or_path=module_name,
                                       config=None,
                                       target=default_target)
        link.execCommand(link_args, None)


def link_kubos_targets():
    logging.disable(logging.WARNING)
    target_list = get_target_list()
    for linked_target in target_list:
        link_target_args = argparse.Namespace(target_or_path=linked_target,
                                              config=None,
                                              target=linked_target,
                                              set_target=linked_target,
                                              save_global=False,
                                              no_install=False)
        link_target.execCommand(link_target_args, '')
