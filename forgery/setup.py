#!/usr/bin/env python2.5
#
# ------------------------------------------------
#
#   CHANGE ABOVE OR EDIT THE "Shell Script Files"
#   PHASE TO START THE THIS SCRIPT WITH ANOTHER
#   PYTHON INTERPRETER.
#
# ------------------------------------------------
# 

"""
Distutils script for building Forgery.

Development:
	xcodebuild -buildstyle Development

Deployment:
	xcodebuild -buildstyle Deployment

These will place the executable in
the "build" dir by default.

Alternatively, you can use py2app directly.
    
Development:
	python setup.py py2app --alias
    
Deployment:
	python setup.py py2app
    
These will place the executable in
the "dist" dir by default.

"""

from distutils.core import setup
import py2app
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from PyObjCTools import XcodeSupport

xcode = XcodeSupport.xcodeFromEnvironment(
	'Forgery.xcodeproj',
	os.environ,
)

sys.argv = xcode.py2app_argv(sys.argv)
if sys.argv[1] == 'py2app':
	sys.argv.insert(2, '--plist=Info.plist')
setup_options = xcode.py2app_setup_options('app')

#
# mangle any distutils options you need here
# in the setup_options dict
#

setup_options['name'] = 'Forgery'
setup_options['version'] = setup_options['app'][0]['plist']['CFBundleShortVersionString']
setup_options['description'] = 'Forgery is the first cross-platform Aleph One map editor'
setup_options['author'] = 'Ben Urban'
setup_options['author_email'] = 'benurban@users.sourceforge.net'
setup_options['url'] = 'http://forgery.sourceforge.net/'
setup_options['license'] = 'GPL-2'
setup_options['classifiers'] = [
	'Development Status :: 3 - Alpha',
	'Environment :: MacOS X',
	'Environment :: Win32 (MS Windows)',
	'Environment :: X11 Applications',
	'Intended Audience :: End Users/Desktop',
	'License :; OSI Approved :: GNU General Public License (GPL)',
	'Natural Language :: English',
	'Operating System :: MacOS :: MacOS X',
	'Operating System :: Microsoft :: Windows',
	'Operating System :: OS Independent',
	'Operating System :: POSIX',
	'Programming Language :: Python',
	'Topic :: Games/Entertainment :: First Person Shooters',
]

setup(**setup_options)
