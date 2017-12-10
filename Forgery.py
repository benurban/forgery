#!/usr/bin/env python2.5

# Forgery.py
# Forgery

# Copyright (c) 2007 by Ben Urban <benurban@users.sourceforge.net>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import __builtin__

# This overrides PyObjC detection in ForgeryCommon, so that the
# wxPython version can be used on a Mac.  Set it to True to enable
# the override, or False to disable it.
__builtin__.preferWX = False

from ForgeryCommon import *

if usePyObjC:
	
	from PyObjCTools import NibClassBuilder, AppHelper
	from Foundation import NSBundle
	
	info = NSBundle.mainBundle().infoDictionary()[u'PyObjCXcode']
	
	for nibFile in info[u'NIBFiles']:
		NibClassBuilder.extractClasses(nibFile)
	del nibFile
	
	for pythonModule in info[u'Modules']:
		__import__(pythonModule)
	del pythonModule
	
	del info

import ForgeryApplication, ForgeryCursor

def main():
	if usePyObjC:
		ForgeryCursor.initCursors()
		AppHelper.runEventLoop()
	else:
		app = ForgeryApplication.sharedApplication() # just to create the instance
		ForgeryCursor.initCursors() # wx needs the application to exist before it can create the cursors
		# infinite recursion occurs if the document creation is
		# done in OnInit()
		# (_sharedApplication is not set, but the document
		# tries to access the instance to put itself in the list)
		app.CreateDocument()
		app.MainLoop()

if __name__ == '__main__':
	main()
