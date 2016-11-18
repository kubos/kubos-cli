import os, sys, imp

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
sys.path.append(myPath + '/../kubos/utils/')

import kubos
from kubos import update
from git_common import *
import shutil


class TestUpdate(object):
    def setup_class(cls):
      if os.path.isdir(KUBOS_DIR):
        shutil.rmtree(KUBOS_DIR)


    def test_creates_kubos_dir(self):
	assert not (os.path.isdir(KUBOS_DIR))
	kubos.update.execCommand([], [])
	assert os.path.isdir(KUBOS_DIR)

