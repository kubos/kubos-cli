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
import sys
import os
import json
import yotta.lib.globalconf as globalconf

from kubos.utils.sdk import *
from yotta import target
from yotta.options import parser


def addOptions(parser):
    parser.add_argument('set_target', nargs='?', default=None, help='set a new target board or display the current target')


def execCommand(args, following_args):
    args = vars(args)
    target = args['set_target'] #Confusingly the set_target key is the target the user wants to set, no the currently set target
    default_target = args['target'] #this is either the currently set target or the default stm32f4 discovery target
    if target != None:
        set_target(target)
    else:
        show_target(default_target)


def show_target(default_target):
    current_target = default_target
    if current_target:
        target_args = argparse.Namespace(plain=False,
                                         set_target=None,
                                         target=default_target)
        target.displayCurrentTarget(target_args)
    else:
        print 'No target currently set'
        set_target('') #prints the available target list


def set_target(new_target):
    available_target_list = get_target_list()
    print 'Setting Target: %s' % new_target.split('@')[0]

    if new_target in available_target_list:
        new_target_args = argparse.Namespace(target_or_path=new_target,
                                              config=None,
                                              target=new_target,
                                              set_target=new_target,
                                              save_global=False,
                                              no_install=False)
        target.execCommand(new_target_args, '')
        print '\nTarget Successfully Set to: %s' % new_target
    else:
        if new_target != '':
            print >>sys.stderr, 'Error: Requested target %s not available.' % new_target
        print 'Available targets are:\n'
        for _target in available_target_list:
            print >>sys.stderr, _target
        sys.exit(1)


def get_target_list():
    target_list = os.listdir(GLOBAL_TARGET_PATH)
    available_target_list = []

    for subdir in target_list:
        target_json = os.path.join(GLOBAL_TARGET_PATH, subdir, 'target.json')
        with open(target_json, 'r') as json_file:
            data = json.load(json_file)
            available_target_list.append(data['name'])
    return available_target_list
