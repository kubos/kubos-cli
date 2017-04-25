#!/usr/bin/python

import json
import kubos
import logging
import mock
import os
import sys
import unittest

from sets import Set
from kubos.test.utils import KubosTestCase
from kubos.utils.constants import GLOBAL_TARGET_PATH
from kubos.utils.sdk_utils import get_target_lists

class CLIIntegrationTest(KubosTestCase):

    def setUp(self):
        super(CLIIntegrationTest, self).setUp()
        self.proj_name = 'project-test'
        self.proj_dir = os.path.join(self.base_dir, self.proj_name)
        self.target_list = None #Defined at test runtime
        self.first_arg = sys.argv[0]
        sys.argv = [self.first_arg] #clear any excess command line arguhements
        logging.error = mock.MagicMock()


        #The tests are run in alphabetical order by default (hence the 1,2,3,etc..)
        #TODO: Get a better way of running the test in order while still being readable
    def test_1_update_source_check_versions(self):
        #testing displaying versions, various methods for chaning versions and updating the kubos source
        self.run_command('version')
        self.run_command('update')
        self.run_command('update', '--latest')
        self.run_command('version')
        self.run_command('versions')
        self.run_command('use', '--branch', 'master')
        self.run_command('version')
        self.run_command('versions')
        os.chdir(self.base_dir)


    def test_2_rt_example(self):
        #test setting and verifying that our targets can all be set
        #Projects are not built because this is only testing the CLI's ability to
        #set/show and verify targets
        self.run_command('init', self.proj_name)
        os.chdir(self.proj_dir)
        self.run_command('target')
        rt_list, linux_list = get_target_lists()
        for target in rt_list:
            self.run_command('target', target)
            self.run_command('target') #print the target
            self.run_command('list')
        os.chdir(self.base_dir)


    def test_3_linux_example(self):
        #Same test as the rt-example test but for the linux targets/project
        self.run_command('init', '-l', self.proj_name)
        os.chdir(self.proj_dir)
        self.run_command('target')
        rt_list, linux_list = get_target_lists()
        for target in linux_list:
            self.run_command('target', target)
            self.run_command('target')
            self.run_command('list')
        os.chdir(self.base_dir)


    def run_command(self, subcommand_name, *args):
        arg_list = [subcommand_name] + list(args)
        #store the current command line arguments so we can restore them later
        starting_args = sys.argv
        #set up new command line args
        sys.argv = sys.argv + arg_list
        print '\nRunning command %s %s' % (subcommand_name, ' '.join(args))

        #run the command
        return_code = kubos.main()
        self.assertEqual(return_code, 0)
        logging.error.assert_not_called() #secondary safeguard for detecting runtime errors

        #reset the command line arguments that we added during this command run
        sys.argv = starting_args


    def tearDown(self):
        super(CLIIntegrationTest, self).tearDown()


if __name__ == '__main__':
    unittest.main()
