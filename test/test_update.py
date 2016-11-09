import os, sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../kubos/utils/')

from git_common import *
from kubos import update

def test_creates_kubos_dir():
    result = update.execCommand([], [])
    assert os.path.isdir(KUBOS_DIR)
