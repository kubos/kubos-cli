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

from pkg_resources import resource_filename
from yotta import link, link_target
import yotta

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

def get_module_name(path):
    if not os.path.isfile(path):
        return None
    string = open(path, 'r').read()
    data = json.loads(string)
    return data['name']

def is_marker(entity_name):
    #Determine if the directory name is at the root of a module or target
    marker_names = ['module.json',
                    'target.json']
    return True if entity_name in marker_names else False


'''
The following functions are used for recursively creating links too and from the global
cache (located at /usr/local/lib/yotta_*).

`kubos update` command will link all modules
to the global cache after downloading newer kubos source.

`kubos link --all` will link all of the modules and target in the global cache into a
project.
'''


def link_entities(src, dst):
    '''
    This function is used for recursively searching subdirectories for module and target
    roots ie. where a module.json or target.json file exists once a root is found, the 
    linking function is called.
    '''
    logging.disable(logging.WARNING) #suppress yotta warning for linking non-required modules and targets
    for subdir in os.listdir(src):
        #loop through the subdirectories of src
        cur_dir = os.path.join(src, subdir)
        if is_marker(subdir):
            #if we're pointing to a target.json or module.json - link the module and return
            #NOTE: This assumes there are not nested modules
            run_link(cur_dir, dst)
            return
        elif os.path.isdir(cur_dir):
            #if we're looking at a subdirectory recursively search for a module root
            link_entities(cur_dir, dst)


def run_link(src, dst):
    '''
    This is used for proxying to the yotta link and link_target commands that actually
    generate the links to or from the global cache.
    '''
    link_module = link if 'module' in src else link_target
    if dst:
        #we're linking to a project from the global cache so we need to link the module by name
        entity_name = get_module_name(src)
        path = dst
    else:
        #we're linking to the global cache, the default behavior of a None module/target name
        #is linking it to the global cache.
        entity_name = None
        path = os.path.dirname(src)
    start_dir = os.getcwd()
    os.chdir(path)
    link_args = argparse.Namespace(module_or_path=entity_name,
                                   target_or_path=entity_name,
                                   config=None,
                                   target=yotta.lib.detect.kubosDefaultTarget(),
                                   save_global=True,
                                   no_install=False)
    link_module.execCommand(link_args, '')
    os.chdir(start_dir)


def link_to_project(project):
    print 'Linking modules...'
    link_entities(GLOBAL_MODULE_PATH, project)
    print 'Linking targets...'
    link_entities(GLOBAL_TARGET_PATH, project)


def link_to_global_cache(path):
    link_entities(path, None)
