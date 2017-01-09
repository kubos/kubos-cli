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

import json
import logging
import os

from pkg_resources import resource_filename

KUBOS_RESOURCE_DIR = os.path.join(resource_filename(__name__, ''), '..')
SDK_MODULE_JSON = os.path.join(KUBOS_RESOURCE_DIR, 'module.json')
GLOBAL_TARGET_PATH  = os.path.join('/', 'usr', 'local', 'lib', 'yotta_targets')
GLOBAL_MODULE_PATH  = os.path.join('/', 'usr', 'local', 'lib', 'yotta_modules')

def get_sdk_attribute(attr):
    sdk_data = json.load(open(SDK_MODULE_JSON, 'r'))
    if attr in sdk_data:
        return sdk_data[attr]
    else:
        return None

def is_marker(entity_name):
    #Determine if the directory name is at the root of a module
    marker_names = ['module.json',
                    'target.json']
    return True if entity_name in marker_names else False

def link_entities(src, dst):
    logging.disable(logging.WARNING) #suppress yotta warning for linking non-required modules and targets
    for subdir in os.listdir(src):
        #Traverse all the subdirectories of src
        #if a subdirectory is a module or a target link it to dst (globally if dst is None)
        cur_dir = os.path.join(src, subdir)
        if os.path.isdir(cur_dir):
            link_entities(cur_dir, dst)
        elif is_marker(subdir):
            if dst:
                link_entity_globally(cur_dir)
            else:
                link_to_project(cur_dir)


def link_entity_globally(path): # links both targets and modules
    path = os.path.dirname(path)
    start_dir = os.getcwd()
    os.chdir(path)
    link_target_args = argparse.Namespace(module_or_path=None,
                                          target_or_path=None,
                                          config=None,
                                          target=detect.kubosDefaultTarget(),
                                          save_global=True,
                                          no_install=False)
    link_target.execCommand(link_target_args, '')
    os.chdir(start_dir)


def link_to_project(project):
    pass
    #TODO: Implement linking global modules and targets into a project

