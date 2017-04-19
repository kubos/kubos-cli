#! /usr/bin/python

import json
import os
import sys
import subprocess

module_json = 'module.json'
version_key = 'version'

def main():
    '''
    This script updates versions, builds and deploys new versions of the kubos-cli.

    How to use this script:

    To explicitly set the version of the new release, update the version to what you
    want in the module.json file and commit and push those changes to master. Once
    the tests pass this script will tag the repo at that new version number (that you set
    in module.json), build and upload the module to pypi.

    If you don't care about the version number, just merge your changes to master
    of the Kubos-cli repo. Once the tests pass, this will bump the build # of the version,
    tag and upload the module to pypi.
    '''
    latest_tag = get_latest_tag()
    module_version = get_module_version()
    commit = True
    if latest_tag == module_version:
        version = bump_and_write_version(module_version)
    else:
        version = module_version
        commit = False

    if commit:
        commit_and_push(version)

    tag_and_push(version)
    build_and_upload()


def get_latest_tag():
    tag_str = subprocess.check_output(['git', 'tag', '--sort=-creatordate'])
    tag_list = tag_str.split('\n')
    latest = tag_list[0]
    print 'The lastest tag is: %s' % latest
    return latest


def get_module_version():
    with open(module_json, 'r') as module_file:
        data = json.loads(module_file.read())
    version = data[version_key]
    print 'The module.json version is: %s' % version
    return version


def bump_and_write_version(version):
    version_fields = version.split('.')

    if len(version_fields) == 4:  #Add a patch number
        version_fields[3] = str(int(version_fields[3]) + 1) #bump the version number by 1 and store it as a string
        version = '.'.join(version_fields)
    elif len(version_fields) == 3:# bump the version number
        version = version + '.1'

    with open(module_json, 'r') as module_file:
        data = json.loads(module_file.read())

    data[version_key] = version

    with open(module_json, 'w') as module_file:
        module_file.write(json.dumps(data,
                                     sort_keys=True,
                                     indent=4,
                                     separators=(',', ': '))
                                     )
    return version


def check_and_commit_module_version(latest_tag):
    '''
    If the module.json version number has been bumped but not tagged, this won't
    increment the version but will tag and release it.

    If the module.json version number matches the latest tag, this will bump the
    version number and continue.
    '''

    data[version_key] = version
    return version


def commit_and_push(version_number):
    run_cmd('git', 'add', 'module.json')
    print 'Committing the version update...'
    run_cmd('git', 'commit', '-m', '"Bump version to %s. ci skip"' % version_number) #we want ci to skip to prevent an infinite release cycle.

    print 'Pushing the commit to origin...'
    run_cmd('git', 'push', 'origin', 'master') #push the commit


def tag_and_push(version_number):
    print 'Tagging the latest release: %s...' % version_number
    run_cmd('git', 'tag', version_number)

    print 'Pushing the tag to origin...'
    run_cmd('git', 'push', 'origin', version_number) #push the tag


def build_and_upload():
    print 'Building the wheel...'
    run_cmd('python', 'setup.py', 'bdist_wheel', '--universal')

    print 'Uploading the wheel...'
    run_cmd('twine', 'upload', 'dist/*', '--username', os.environ['PYPI_USERNAME'], '--password', os.environ['PYPI_PASSWORD'])


def run_cmd(*args, **kwargs):
    try:
        return subprocess.check_output(args, **kwargs)
    except subprocess.CalledProcessError, e:
        print >>sys.stderr, 'Error executing command, giving up.\nError Message: %s' % e
        sys.exit(1)


if __name__ == '__main__':
    main()

