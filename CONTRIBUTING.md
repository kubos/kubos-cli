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
$ cd ~/Projects
$ git clone git@github.com:{YOUR_USERNAME}/kubos-cli.git
```

### Creating a virtual environment

We recommend creating a virtual environment to keep all your dependencies separate from your OS. Start by installing [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).

Then run

```
pyenv install 3.6.0
```

Then create a virtualenv

```
pyenv virtualenv 3.6.0 kubos-cli
```

Then activate the environment

```
pyenv activate kubos-cli
```

To exit the venv run

```
pyenv deactivate
```

### Installing Dependent Packages
The dependent packages should be installed on a virtualenv, so make sure you activate your virtualenv:

```
pyenv activate kubos-cli
```

It is also recommended to use the latest version of pip. You can upgrade it with:

```
pip install -U pip
```

Then install the dependent libraries

```
$ cd ~/Projects/kubos-cli
$ pip install -e .
```

pip install -e . means install the kubos-cli package in editable mode (or developer mode). This allows you to edit code directly in ~/Projects/kubos-cli without reinstalling the package.

### Run Tests

```
python ./kubos/test/integration/integration_test.py
```

### Submitting code

```
git checkout -b new-fix
git push --set-upstream origin new-fix
```

Then head to (kubos-cli)[https://github.com/kubostech/kubos-cli] and create a PR.
