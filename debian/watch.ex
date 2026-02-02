# Example watch control file for uscan
# Rename this file to "watch" and then you can run the "uscan" command
# to check for upstream updates and more.
# See uscan(1) for format

# Compulsory line, this is a version 4 file
version=4

# PGP signature mangle, so foo.tar.gz has foo.tar.gz.sig
#opts="pgpsigurlmangle=s%$%.sig%"

# HTTP site (basic)
#http://example.com/downloads.html \
#  files/mingw64-i686-tiff-([\d\.]+)\.tar\.gz debian uupdate

# Uncommment to examine a FTP server
#ftp://ftp.example.com/pub/mingw64-i686-tiff-(.*)\.tar\.gz debian uupdate

# SourceForge hosted projects
# http://sf.net/mingw64-i686-tiff/ mingw64-i686-tiff-(.*)\.tar\.gz debian uupdate

# GitHub hosted projects
#opts="filenamemangle=s%(?:.*?)?v?(\d[\d.]*)\.tar\.gz%<project>-$1.tar.gz%" \
#   https://github.com/<user>/mingw64-i686-tiff/tags \
#   (?:.*?/)?v?(\d[\d.]*)\.tar\.gz debian uupdate

# PyPI
# https://pypi.debian.net/mingw64-i686-tiff/mingw64-i686-tiff-(.+)\.(?:zip|tgz|tbz|txz|(?:tar\.(?:gz|bz2|xz)))

# Direct Git
# opts="mode=git" http://git.example.com/mingw64-i686-tiff.git \
#   refs/tags/v([\d\.]+) debian uupdate

# Uncomment to find new files on GooglePages
# http://example.googlepages.com/foo.html mingw64-i686-tiff-(.*)\.tar\.gz
