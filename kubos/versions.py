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
from packaging import version
from yotta.options import parser

def addOptions(parser):
    pass


def execCommand(args, following_args):
    repo, origin = get_repo(KUBOS_SRC_DIR)
    tag_list = get_tag_list(repo)
    latest   = get_latest_tag(tag_list)
    print 'Availalbe versions are:'
    print_tag_list(tag_list)
    print 'The most recent release is: %s' % latest


def get_tag_list(repo):
    tags = repo.tags
    tag_list = []
    for tag in tags:
        tag_list.append(tag)
    return tag_list


def print_tag_list(tag_list):
    active_version = get_active_kubos_version()
    for tag in tag_list:
        if tag.name == active_version:
            sys.stdout.write('*')
        print tag.name


def get_latest_tag(tag_list):
    latest_tag = git.TagReference("", "", check_path=False) #Set to a dummy tag that will be less than any other valid tag
    for tag in tag_list:
        if version.parse(tag.name) > version.parse(latest_tag.name):
            latest_tag = tag
    return latest_tag

