#!/usr/bin/env python

# Forgery.py
# Forgery

# Copyright (c) 2007-2011 by Ben Urban <benurban@users.sourceforge.net>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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
	
	#import modules required by application
	import objc
	import Foundation
	import AppKit
	
	from PyObjCTools import AppHelper
	
	# import modules containing classes required to start application and load MainMenu.nib
	import ForgeryApplication, ForgeryDocument, ForgeryInspector, ForgeryPalette, ForgeryPreferences, ForgeryProgressWindow

import ForgeryApplication, ForgeryCursor

def main():
	#app = ForgeryApplication.sharedApplication() # create the instance
	ForgeryCursor.initCursors() # initialize the cursors
	# (wx) the application must exist before it can create the cursors
	if usePyObjC:
		# pass control to AppKit
		AppHelper.runEventLoop()
	else:
		# infinite recursion occurs if the document creation is done in OnInit()
		# (_sharedApplication is not set, but the document
		# tries to access the instance to put itself in the list)
		app.CreateDocument()
		app.MainLoop()

if __name__ == '__main__':
	main()
