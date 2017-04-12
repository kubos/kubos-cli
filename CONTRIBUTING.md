Contributing to KubOS
---

Before a pull request is merged, you must [sign our Contributor's License Agreement](https://www.clahub.com/agreements/openkosmosorg/KubOS)

## Instructions:
  1. Fork and clone the repo
  2. Create a virtualenv for this project
  3. Install dependent packages with pip install -e .
  4. Install test dependent packages with pip install -r requirements-test.txt
  5. Run tests
  6. Submitting code

### Fork and clone the repo

Start by clicking the Fork button on our Github repo. Then, open a command line and type
the following.

```
cd ~/Projects
git clone git@github.com:{YOUR_USERNAME}/kubos-cli.git
```

### Creating a virtual environment

Kubos uses Vagrant to create environments that also has the added benifit of a virtual dev environment. We will be using Vagrant in place of installing a Python Virtual Environment.

#### Set up KubOS Sdk
Follow these instructions for setting up [Vagrant for Kubos](http://docs.kubos.co/0.2.2/md_docs_sdk-installing.html)

#### Linking your volume
To develop locally on your machine and have the changes take affect, link your cloned kubos-cli folder to Vagrant.

Open your Vagrant file from the previous step and change the following line:
```
config.vm.synced_folder "../data", "/vagrant_data"
```
To this
```
config.vm.synced_folder "~/Projects/kubos-cli, "/home/vagrant/kubos-cli"
```
Afterwards, if you have already ran Vagrant, you will need to reload for the changes to take affect.
```
vagrant reload
```

### Installing Dependent Packages
Next, log into your Vagrant environment and install Kubos CLI for development
```
vagrant up
vagrant ssh
```
It is also recommended to use the latest version of pip. You can upgrade it with:
```
pip install -U pip
```

Then install the dependent libraries
```
cd /home/vagrant/kubos-cli
pip install -e .
```
`pip install -e .` means install the kubos-cli package in editable mode (or developer mode). This allows you to edit code directly in ~/Projects/kubos-cli without reinstalling the package.

To run tests, requirements are placed in a separate file named requirements.txt. To install them, do:
```
cd /home/vagrant/kubos-cli
pip install -r requirements.txt
```
### Run Tests

```
cd /home/vagrant/kubos-cli
// Integration
python ./kubos/test/integration/integration_test.py

// Unit
python setup.py test
```

*Note* After making changes to your code, run both unit and integration tests to ensure no
side affects have occurred.

### Submitting code

```
git checkout -b new-fix
git push --set-upstream origin new-fix
```

Then head to (kubos-cli)[https://github.com/kubostech/kubos-cli] and create a PR.
