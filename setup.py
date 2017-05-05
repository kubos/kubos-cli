# Kubos CLI
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
import os
import shutil
import distutils.cmd
from setuptools import setup, find_packages

module_data = json.load(open("module.json", "r"))
setup_data = json.load(open("setup.json", "r"))

for ascii_key in ("name", "version"):
    module_data[ascii_key] = module_data[ascii_key].encode("ascii")

for key in module_data:
    setup_data[key] = module_data[key]

setup_data["packages"] = find_packages()
setup_data["package_data"] = {
                                 "kubos": ["completion/*"]
                             }

setup(**setup_data)
