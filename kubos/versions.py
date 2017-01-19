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
from kubos.utils.git_utils import *
from packaging import version
from yotta.options import parser

def addOptions(parser):
    pass


def execCommand(args, following_args):
    if not os.path.isdir(KUBOS_SRC_DIR):
        logging.info('No versions are locally available. Please run `kubos update` to pull all of the available source versions.')
        sys.exit(1)
    repo, origin = get_repo(KUBOS_SRC_DIR)
    tag_list = get_tag_list(repo)
    latest   = get_latest_tag(tag_list)
    logging.info('Available versions are:')
    print_tag_list(tag_list)
    logging.info('The most recent release is: %s' % latest)

