#! /usr/bin/env python
import sys
from pony_client import BuildCommand, TestCommand, do, send, \
     TempDirectoryContext, SetupCommand, GitClone, check, parse_cmdline
import os
import tempfile
import shutil

options, args = parse_cmdline()

###

default_server_url = 'http://localhost:8080/xmlrpc'
repo_url = 'git://github.com/nzjrs/wasp.git'
tags = ['wasp']

###

def do_autobuild(commands, name):
    server_url = options.server_url or default_server_url
    if not options.force_build:
        if not check(name, server_url, tags=tags):
            print 'check build says no need to build; bye'
            sys.exit(0)

    context = TempDirectoryContext(options.cleanup_temp)
    results = do(name, commands, context=context)
    client_info, reslist = results

    if options.report:
        print 'result: %s; sending' % (client_info['success'],)
        send(server_url, results, tags=tags)
    else:
        print 'build result:'
        import pprint
        pprint.pprint(client_info)
        pprint.pprint(reslist)
        print '(NOT SENDING BUILD RESULT TO SERVER)'

if __name__ == "__main__":
    #onboard
    do_autobuild([
        GitClone(repo_url),
        BuildCommand(['make', 'clean', 'all'],
                  name='build', run_cwd='sw/onboard'),
        TestCommand(['./build-tests.sh'],
                 name='run onboard tests', run_cwd='sw/onboard')
        ],
        'wasp-onboard')

    #groundstation
    do_autobuild([
        GitClone(repo_url),
        TestCommand(['make', 'test'],
                  name='groundstation tests', run_cwd='sw/groundstation'),
        ],
        'wasp-groundstation')



