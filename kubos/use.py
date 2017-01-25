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

from yotta.options import parser

from kubos.utils import git_utils, sdk_utils
from kubos.utils.constants import  KUBOS_SRC_DIR

def addOptions(parser):
    parser.add_argument('set_version', nargs=1, help='Set a specific version of the KubOS modules to build your projects against.')


def execCommand(args, following_args):
    args = vars(args)
    version = args['set_version'][0]
    kubos_repo = git_utils.get_repo(KUBOS_SRC_DIR)
    git_utils.check_provided_version(version, kubos_repo)
    sdk_utils.purge_global_cache()
    sdk_utils.link_to_global_cache(KUBOS_SRC_DIR)
