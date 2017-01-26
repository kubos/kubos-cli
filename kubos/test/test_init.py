# Kubos CLI
# Copyright (C) 2017 Kubos Corporation
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
# limitations under the License.import argparse

import argparse
import kubos
import os
import tempfile
import unittest

from kubos import init
from kubos.test import utils

class KubosInitTest(utils.KubosTestCase):

    def setUp(self):
        super(KubosInitTest, self).setUp()
        self.proj_name = 'test-project'
        self.args = argparse.Namespace()
        self.args.proj_name = [self.proj_name] # argparse returns proj_name as an array
        self.args.linux = False

    def test_creates_proj_dir(self):
        self.proj_dir = os.path.join(self.base_dir, self.proj_name)
        main_src_file = os.path.join(self.proj_dir, 'source', 'main.c')
        kubos.init.execCommand(self.args, None)
        self.assertTrue(os.path.isdir(self.proj_dir))
        self.assertTrue(os.path.isfile(main_src_file))


    def test_overwrite_existing(self):
        self.proj_name = 'test-project'
        self.proj_dir = os.path.join(self.base_dir, self.proj_name)
        with self.assertRaises(SystemExit):
            kubos.init.execCommand(self.args, None)
            #we cd into the project directory to change the module.json file in execCommand
            os.chdir(self.base_dir)
            kubos.init.execCommand(self.args, None)


    def tearDown(self):
        super(KubosInitTest, self).tearDown()

if __name__ == '__main__':
    unittest.main()
