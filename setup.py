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

setup(**setup_data)
