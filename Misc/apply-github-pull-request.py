#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Helper script to apply pull requests from github.com to local hg working copy.

Example:

cd jython-hg-workdir
apply-github-pull-request.py 4

'''

import argparse
import getpass
import requests
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--github-repo', default='jythontools/jython')
parser.add_argument('--github-user', default=getpass.getuser())
parser.add_argument('--github-password')
parser.add_argument('--dry-run', action='store_true', help='Dry-run mode: only show what would be done')
parser.add_argument('pull_request_id', help='Pull request ID on github.com')

args = parser.parse_args()

password = args.github_password

if not password:
    password = getpass.getpass('{}@github.com'.format(args.github_user))

from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth(args.github_user, password)
r = requests.get('https://api.github.com/repos/{}/pulls/{}'.format(args.github_repo, args.pull_request_id), auth=auth)
if r.status_code != 200:
    print r.json()
    sys.exit(1)
data = r.json()
print 'Pull Request {} by {}:'.format(data['number'], data['user']['login'])
print data['title']
print data['body']
print '-' * 40

r = requests.get('https://github.com/{}/pull/{}.diff'.format(args.github_repo, args.pull_request_id))

patch_contents = r.text

print patch_contents

with tempfile.NamedTemporaryFile(suffix='-github-patch-{}'.format(args.pull_request_id)) as fd:
    fd.write(patch_contents)
    fd.flush()
    cmd = [
        'patch',
        '-p1',
        '--batch',
        '-i',
        fd.name,
    ]
    if args.dry_run:
        cmd.append('--dry-run')
    p = subprocess.Popen(cmd)
    p.communicate()

