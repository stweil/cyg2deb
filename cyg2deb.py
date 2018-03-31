#!/usr/bin/python3

import glob
import http.client
import os
import re
import shutil
import sys
import tarfile

#~ PROXYSERVER = 'ftp.cygwin.com'
#~ PROXYPATH = '/pub/cygwin/'

PROXYSERVER = 'ftp-stud.hs-esslingen.de'
PROXYPATH = '/pub/Mirrors/sources.redhat.com/cygwin/'

HOSTARCH = 'x86_64'

if len(sys.argv) > 1:
    ARCH = sys.argv[1]
else:
    ARCH = 'x86_64'

if len(sys.argv) > 2:
    PATTERN = sys.argv[2]
else:
    PATTERN = 'mingw64-' + ARCH + '-.*'

CACHEDIR = 'cache' + '/' + HOSTARCH

# Cygwin package handling.
class Package:
    def __init__(self, name):
        # Initialise data for the package.
        # Sets name and resets all other values.
        self.name = name
        self.sdesc = ''
        self.ldesc = ''
        self.category = ''
        self.requires = ''
        self.version = ''
        self.install = ''
        self.install_size = 0
        self.install_sha512sum = ''
        self.source = ''
        self.source_size = 0
        self.source_sha512sum = ''
        self.message = ''
        self.arch = 'undefined'

    def __str__(self):
        # String which describes the package.
        return self.name + ' ' + self.version + ' (' + self.sdesc + ')'

    def get(self):
        # Get package file if it is missing in the local cache.
        # TODO: check sha512sum.
        name = self.name.lower().replace('_', '-')
        version = self.version.replace('_', '-')
        filename = name + '_' + version + '-1_' + self.arch + '.deb'
        if package.arch != 'all':
            print("skip package,", filename, '(wrong architecture)')
        elif package.category == '_obsolete':
            print("skip package,", filename, '(obsolete)')
        elif os.path.exists(filename):
            print("skip package,", filename, '(cached)')
        else:
            # Package file missing in cache, so get it.
            package.printinfo()
            print("")
            print("make package,", filename)
            print("")
            filename = CACHEDIR + '/' + self.install
            if not os.path.exists(filename):
                os.makedirs(os.path.dirname(filename), 0o777, True)
                c = http.client.HTTPSConnection(PROXYSERVER)
                c.request('GET', PROXYPATH + self.install)
                r = c.getresponse()
                #~ print(r.status, r.reason)
                f = open(filename, 'wb')
                f.write(r.read())
                f.close
                c.close()
            tmpdir = CACHEDIR + '/tmp'
            if os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)
            #~ try:
            if 1:
                f = tarfile.open(filename)
                f.extractall(tmpdir)
                f.close()
                archdir = '/usr/' + ARCH + '-w64-mingw32'
                srcdir = tmpdir + archdir + '/sys-root/mingw/lib/pkgconfig'
                if os.path.exists(srcdir):
                    # Package uses pkg-config.
                    # Make the *.pc file(s) available at the right location.
                    dstdir = tmpdir + archdir + '/lib/pkgconfig'
                    os.makedirs(dstdir)
                    for path, dirs, files in os.walk(srcdir):
                        for filename in files:
                            srcfile = os.path.join('../../sys-root/mingw/lib/pkgconfig', filename)
                            dstfile = os.path.join(dstdir, filename)
                            os.symlink(srcfile, dstfile)
                else:
                    # Package does not use pkg-config.
                    # Make the *.h and *.a file(s) available at the right location.
                    dstdir = tmpdir + archdir + '/include'
                    os.makedirs(dstdir)
                    srcdir = tmpdir + archdir + '/sys-root/mingw/include'
                    for path, dirs, files in os.walk(srcdir):
                        for filename in files:
                            srcfile = os.path.join('../sys-root/mingw/include', filename)
                            dstfile = os.path.join(dstdir, filename)
                            os.symlink(srcfile, dstfile)
                    dstdir = tmpdir + archdir + '/lib'
                    os.makedirs(dstdir)
                    srcdir = tmpdir + archdir + '/sys-root/mingw/lib'
                    for path, dirs, files in os.walk(srcdir):
                        for filename in files:
                            srcfile = os.path.join('../sys-root/mingw/lib', filename)
                            dstfile = os.path.join(dstdir, filename)
                            os.symlink(srcfile, dstfile)
                filename = CACHEDIR + '/' + self.name + '.tar'
                f = tarfile.open(filename, 'w')
                for dir in glob.glob(tmpdir + '/*'):
                    f.add(dir, arcname = os.path.basename(dir))
                f.close()
                #~ print('/usr/bin/fakeroot', '/usr/bin/alien', '--to-deb', '--keep-version', '--description="' + self.sdesc + '"', '--version=' + version, '--target=all', filename)
                os.spawnlp(os.P_WAIT, '/usr/bin/fakeroot', 'fakeroot', '/usr/bin/alien', '--to-deb', '--keep-version', '--description=' + self.sdesc, '--version=' + version, '--target=all', filename)
                os.remove(filename)
            #~ except:
                #~ print('failed')

    def printinfo(self):
        # Print some information for package.
        #~ self.ldesc = ''
        #~ self.install_sha512sum = ''
        #~ self.source = ''
        #~ self.source_size = 0
        #~ self.source_sha512sum = ''
        #~ self.message = ''
        print("Name:        " + self.name)
        print("Version:     " + self.version)
        print("Category:    " + self.category)
        print("Requires:    " + self.requires)
        print("Description: " + self.sdesc)
        print("Install:     " + self.install + " (" + self.install_size + ")")


#~ alien --to-deb --generate --keep-version --description "Zlib for Win64 toolchain" --version 1.2.8-4 --target=all

os.makedirs(CACHEDIR, 0o777, True)

setup_ini = CACHEDIR + '/setup.ini'

if not os.path.exists(setup_ini):
    # Did not find setup.ini in local cache, so get it from server.
    conn = http.client.HTTPSConnection(PROXYSERVER)
    conn.request('GET', PROXYPATH + HOSTARCH + '/setup.ini')
    response = conn.getresponse()
    # 200 OK
    #~ print(response.status, response.reason)
    data = response.read()
    conn.close()
    f = open(setup_ini, "wb")
    f.write(data)
    f.close()

f = open(setup_ini)

do_ldesc = False
do_message = False
do_skip = False

package = False

for line in f:
    line = line.strip()
    #~ print(line)
    #~ continue

    if do_ldesc:
        package.ldesc += ' '
        m = re.search('(.*)"', line)
        if m:
            package.ldesc += m.group(1)
            do_ldesc = False
        else:
            package.ldesc += line
        continue

    if do_message:
        package.message += ' '
        m = re.search('(.*)"', line)
        if m:
            package.message += m.group(1)
            do_message = False
        else:
            package.message += line
        continue

    if not line:
        if package:
            package.get()
        do_ldesc = False
        do_message = False
        do_skip = False
        package = False
        continue

    if do_skip:
        continue

    if re.search('^\[prev\]$', line) or re.search('^\[test\]$', line):
        # Skip information for previous or test package versions.
        do_skip = True
        continue

    m = re.search('^@ (' + PATTERN + ')$', line)
    if m:
        name = m.group(1)
        package = Package(name)
        continue
    elif not package:
        continue

    m = re.search('^sdesc: "(.*)"', line)
    if m:
        package.sdesc = m.group(1)
        continue

    m = re.search('^ldesc: "(.*)', line)
    if m:
        package.ldesc = m.group(1)
        m = re.search('^ldesc: "(.*)"', line)
        if m:
            package.ldesc = m.group(1)
        else:
            do_ldesc = True
        continue

    m = re.search('^category: (.*)', line)
    if m:
        package.category = m.group(1)
        continue

    m = re.search('^requires: (.*)', line)
    if m:
        package.requires = m.group(1)
        continue

    m = re.search('^version: (.*)', line)
    if m:
        package.version = m.group(1)
        continue

    m = re.search('^install: (.*) (.*) (.*)', line)
    if m:
        package.install = m.group(1)
        package.install_size = m.group(2)
        package.install_sha512sum = m.group(3)
        m = re.search('^([^/]*)', package.install)
        if m:
            package.arch = m.group(1)
            if package.arch == 'noarch':
                package.arch = 'all'
        continue

    m = re.search('^source: (.*) (.*) (.*)', line)
    if m:
        package.source = m.group(1)
        package.source_size = m.group(2)
        package.source_sha512sum = m.group(3)
        continue

    m = re.search('^message: (.*) "(.*)', line)
    if m:
        package.message = m.group(2)
        m = re.search('^message: (.*) "(.*)"', line)
        if m:
            package.message = m.group(2)
        else:
            do_message = True
        continue

    #~ print(package, " ???")
    #~ print(line)

f.close()
