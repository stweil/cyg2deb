#!/usr/bin/python3

# http://ftp-stud.hs-esslingen.de/pub/Mirrors/sources.redhat.com/cygwin/x86_64/

# curl -O ftp://ftp.cygwin.com/pub/cygwin/x86/setup.ini
# curl -O ftp://ftp.cygwin.com/pub/cygwin/x86_64/setup.ini
# wget ftp://ftp.cygwin.com/pub/cygwin/x86_64/setup.ini
# wget ftp://ftp.cygwin.com/pub/cygwin/x86_64/setup.xz
# xz -d setup.xz
# mv setup setup.ini

#~ release: cygwin
#~ arch: x86_64
#~ setup-timestamp: 1475435599
#~ setup-version: 2.876

#~ sdesc: "Zlib for Win64 toolchain"
#~ ldesc: "This package does NOT contain cygwin binaries.  Instead, it
#~ contains msvcrt-linked binaries (aka 'mingw').  It is for use with the
#~ mingw64-x86_64-gcc cross compiler, and installs into the
#~ /usr/x86_64-w64-mingw32/sys-root/mingw/{lib,include} directories."
#~ category: Devel
#~ version: 1.2.8-4
#~ install: x86_64/release/mingw64-x86_64-zlib/mingw64-x86_64-zlib-1.2.8-4.tar.xz 105120 9e2689e86723680243da505487589f7557ddf49151411ac58eed176df15002992028eaa19cc0d4c8f6655c200b44fe8155a73a84022423dad6a79a1fc1b03a59
#~ source: x86_64/release/mingw64-x86_64-zlib/mingw64-x86_64-zlib-1.2.8-4-src.tar.xz 574400 909f1792eb9462aeaee997f233f9ce2c1c88b5db25219d37f8826f82068bf82a0800c9d070f0c3b4ea68d07ffde0fdeed59a1f80591c2a9d772d4b52533f9899
#~ [prev]
#~ version: 1.2.8-3
#~ install: x86_64/release/mingw64-x86_64-zlib/mingw64-x86_64-zlib-1.2.8-3.tar.xz 105132 76023e0876c81399e3d19a6a93e44d3dc53734eb0e75736ad32e30851450a4d31fd537cbfc504bf14e22944fc2fda2855d6db929e64585c80c2368c6f22d82e7
#~ source: x86_64/release/mingw64-x86_64-zlib/mingw64-x86_64-zlib-1.2.8-3-src.tar.xz 573192 20637095faf8e48989369457d9db260300c82d086fc2cfe0581430004bb48be65fc64fc5a50a3377ba201580eb9b8c47dacc1974d59a073773a4a786df355fe7

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

class Package:
    def __init__(self, name):
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

    def __str__(self):
        return self.name + ' ' + self.version + ' (' + self.sdesc + ')'

    def get(self):
        # TODO: check sha512sum.
        filename = self.name.lower().replace('_', '-') + '_' + self.version + '-1_all.deb'
        print("get package, ", filename)
        if not os.path.exists(filename):
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
            try:
                f = tarfile.open(filename)
                f.extractall(tmpdir)
                f.close()
                srcdir = tmpdir + '/usr/' + ARCH + '/sys-root/mingw/lib/pkgconfig'
                if os.path.exists(srcdir):
                    dstdir = tmpdir + '/usr/' + ARCH + '/lib/pkgconfig'
                    print(dstdir)
                    os.makedirs(dstdir)
                    for path, dirs,  files in os.walk(srcdir):
                        for filename in files:
                            srcfile = os.path.join('../../sys-root/mingw/lib/pkgconfig', filename)
                            dstfile = os.path.join(dstdir, filename)
                            os.symlink(srcfile, dstfile)
                filename = CACHEDIR + '/' + self.name + '.tar'
                f = tarfile.open(filename, 'w')
                try:
                    f.add(tmpdir, '')
                except:
                    print('no files')
                f.close()
                #~ print('/usr/bin/fakeroot', 'alien', 'alien', '--to-deb', '--keep-version', '--description=' + self.sdesc, '--version=' + self.version, '--target=all', filename)
                os.spawnlp(os.P_WAIT, '/usr/bin/fakeroot', 'fakeroot', '/usr/bin/alien', '--to-deb', '--keep-version', '--description=' + self.sdesc, '--version=' + self.version, '--target=all', filename)
                os.remove(filename)
            except:
                print('failed')

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
            package.printinfo()
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

    m = re.search('^@ (' + PATTERN + ')', line)
    if m:
        name = m.group(1)
        if name == 'mingw64-x86_64-zlib' or True:
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

    print(package, " ???")
    print(line)

f.close()
