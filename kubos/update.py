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
import sys
import time
import os

from yotta.options import parser

from kubos.utils import git_utils, \
                        sdk_utils, \
                        status_spinner
from kubos.utils.constants import *

def addOptions(parser):
    parser.add_argument('set_version', nargs='?', default=None, help='Specify a version of the kubos source to use.')


def execCommand(args, following_args):
    if not os.path.isdir(KUBOS_DIR):
        os.makedirs(KUBOS_DIR)
    os.chdir(KUBOS_DIR)
    logging.info('Checking for the most recent KubOS Source...')
    spinner = status_spinner.start_spinner()
    src_repo = git_utils.clone_repo(KUBOS_SRC_DIR, KUBOS_SRC_URL)
    git_utils.clone_example_repo(KUBOS_RT_EXAMPLE_DIR, KUBOS_RT_EXAMPLE_URL)
    git_utils.clone_example_repo(KUBOS_LINUX_EXAMPLE_DIR, KUBOS_LINUX_EXAMPLE_URL)
    status_spinner.stop_spinner(spinner)
    set_version = vars(args)['set_version']
    if set_version:
        git_utils.check_provided_version(set_version, src_repo)

