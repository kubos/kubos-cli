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
import hashlib
import json
import os
import sys
import time

from appdirs import AppDirs
from kubos.utils.sdk import get_sdk_attribute
from pip.utils import get_installed_version


def load_config():
    return _config_class()

def load_sdk_version():
    return get_installed_version('kubos-sdk')

def load_sdk_edition():
    return get_sdk_attribute('edition')

class KubosSDKConfig(object):
    def __init__(self):
        self.appdirs = AppDirs('kubos')
        self.config_path = os.path.join(self.appdirs.user_config_dir, 'kubos-sdk.json')
        self.sdk_version = load_sdk_version()
        self.sdk_edition = load_sdk_edition()
        self.load_config()

    def load_config(self):
        self.config = {}
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)

    def save_config(self):
        if not os.path.isdir(self.appdirs.user_config_dir):
            os.makedirs(self.appdirs.user_config_dir)

        with open(self.config_path, 'w') as f:
            f.write(json.dumps(self.config))

_config_class = KubosSDKConfig
