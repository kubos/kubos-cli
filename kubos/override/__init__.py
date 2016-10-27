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

import os

file_list = []
base_dir = os.path.dirname(__file__)
for name in os.listdir(base_dir):
    file_path = os.path.join(base_dir, name)
    if not name.startswith('__') and os.path.isfile(file_path): #avoid __init__.py(c) files and skip sub-driectories
        base_name, ext = os.path.splitext(name) #remove file extension
        if ext != '.pyc':
            file_list.append(base_name)

__all__ = file_list
