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
import json
import sys
import time
import os

from kubos.utils.git_common import *
from kubos import version as kubos_version
from options import parser
from packaging import version

def addOptions(parser):
    pass


def execCommand(args, following_args):
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
