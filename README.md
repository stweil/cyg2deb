# cyg2deb – convert Cygwin packages to Debian packages

## What is the purpose of this software?
This software is used to convert [Cygwin](https://cygwin.com/) packages to [Debian](https://www.debian.org/) packages.

## Why is this useful?
Most Cygwin packages are only useful on Windows, but the Cygwin package list also includes lots of packages for cross compilation.
Those packages can also be used on Debian GNU Linux to run cross compilations there.

The focus is on cross compilations with [Mingw-w64](https://mingw-w64.org/) on Debian GNU Linux.
Both Cygwin and Debian include Mingw-w64 cross compilers which allow building 32 bit and 64 bit Windows applications,
but Debian only has a small number of libraries for that purpose. Ignore that libraries and use the libraries from Cygwin!

## Where is it used?
It is used to build Windows installers for [QEMU](https://www.qemu.org/) and [Tesseract](https://github.com/tesseract-ocr/tesseract/).

## How to use it?
Here is a typical use case running under Debian (a UTF-8 environment is required):

    $ python3 cyg2deb.py
    Name:        mingw64-x86_64-a52dec
    Version:     0.7.4-2
    Category:    Devel
    Requires:
    Description: ATSC A/52 (AC-3) decoder library for Win64 toolchain
    Install:     noarch/release/mingw64-x86_64-a52dec/mingw64-x86_64-a52dec-0.7.4-2.tar.xz (47832)

    make package, mingw64-x86-64-a52dec_0.7.4-2-1_all.deb

    mingw64-x86-64-a52dec_0.7.4-2-1_all.deb generated
    Name:        mingw64-x86_64-aalib
    Version:     1.4rc5-2
    Category:    Devel
    Requires:    bash mingw64-x86_64-ncurses
    Description: ASCII art library for Win64 toolchain
    Install:     noarch/release/mingw64-x86_64-aalib/mingw64-x86_64-aalib-1.4rc5-2.tar.xz (66348)

    make package, mingw64-x86-64-aalib_1.4rc5-2-1_all.deb

    mingw64-x86-64-aalib_1.4rc5-2-1_all.deb generated
    Name:        mingw64-x86_64-adwaita-icon-theme
    Version:     3.26.1-1
    Category:    Devel
    Requires:    mingw64-x86_64-hicolor-icon-theme mingw64-x86_64-pkg-config
    Description: GNOME desktop icon theme for Win64 toolchain
    Install:     noarch/release/mingw64-x86_64-adwaita-icon-theme/mingw64-x86_64-adwaita-icon-theme-3.26.1-1.tar.xz (13172464)

    make package, mingw64-x86-64-adwaita-icon-theme_3.26.1-1-1_all.deb

    mingw64-x86-64-adwaita-icon-theme_3.26.1-1-1_all.deb generated
    [...]

That use case first gets the complete Cygwin package list `setup.ini`.
Then it looks for all packages named mingw64-x86_64-*, downloads them,
unpacks them and repacks them into Debian packages for 64 bit cross compilation.
Deprecated packages are skipped automatically.
Packages which are not useful for cross compilation because they only work on
Windows are skipped, too.

To get packages for 32 bit cross compilation (mingw64-i686-*),
just run `python3 cyg2deb.py i686`.
