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



from kubos.utils.sdk import *
from yotta import link
from yotta.options import parser


def addOptions(parser):
    parser.add_argument('-a', '--all', action='store_true', default=False, help='Link modules to be used in other projects or modules.')


def execCommand(args, following_args):
    '''
    The point of defining the link command is to allow the CLI to link all of the global targets
    and modules into a project that was not created with the kubos-cli. Otherwise, when a project
    is cloned from Github (rather than created with the kubos-cli `init` command, each target and
    module would have to be linked in individually.

    If the -a or --all argument is not provided, this command proxies to the default yotta command
    implementation.
    '''
    args = vars(args)
    if args['all']:
        #TODO: Add some sort of verification to the cwd -> make sure we're actually in a project directory
        link_to_project(os.getcwd())
    else:
        link.execCommand(args, following_args)

