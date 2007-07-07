# ForgeryMode.py
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

from ForgeryCommon import *

__all__ = (
	'ForgeryMode',
	'modes',
)

import ForgeryPalette

if usePyObjC:
	
	from PyObjCTools import NibClassBuilder
	
	Superclass = NibClassBuilder.AutoBaseClass
	
else:
	
	Superclass = object

class ForgeryMode(Superclass):
	modeID = None
	if not usePyObjC:
		document = None
		viewDelegate = None
	paletteDelegate = None # for some reason it crashes upon quitting when i make it an objc.ivar
	
	if usePyObjC:
		palette = property(fget = lambda self: ForgeryPalette.sharedPalette())
	else:
		app = property(fget = lambda self: self.document and self.document.app)
		palette = property(fget = lambda self: self.app and self.app.palette)
	preferences = property(fget = lambda self: self.document and self.document.preferences)
	snapToGrid = property(fget = lambda self: self.preferences and self.preferences.snapToGrid)
	gridSpacing = property(fget = lambda self: self.preferences and self.preferences.gridSpacing)
	if not usePyObjC:
		view = property(fget = lambda self: self.document and self.document.view)
	mouse0 = property(fget = lambda self: self.view.mouse0)
	mouse1 = property(fget = lambda self: self.view.mouse1)
	data = property(fget = lambda self: self.document.data)
	
	# Shared
	
	def refresh(self):
		return self.view.refresh()
	
	def openUndoGroup(self, name = None):
		return self.document.openUndoGroup(name)
	
	def closeUndoGroup(self, name = None):
		return self.document.closeUndoGroup(name)
	
	def activate(self):
		self.palette.delegate = self.paletteDelegate
		self.palette.update()
		self.refresh()
	
	def deactivate(self):
		self.refresh()
	
	def documentActivated(self):
		self.palette.delegate = self.paletteDelegate
		self.palette.update()
	
	def documentDeactivated(self):
		pass
	
	def documentClosed(self):
		pass
	
	def texturesUpdated(self):
		pass
	
	def validateUI(self, itemID):
		if ID.MODES_START <= itemID <= ID.MODES_END:
			if itemID in modes:
				return True
			else:
				return False
		else:
			return None
	
	def updateMenuItem(self, itemID, check, setText):
		if ID.MODES_START <= itemID <= ID.MODES_END:
			if itemID == self.modeID:
				check(True)
			else:
				check(False)
			if itemID in modes:
				return True
			else:
				return False
		else:
			return None
	
	def getStatusText(self):
		return ""
	
	def cutSelection(self):
		pass
	
	def copySelection(self):
		pass
	
	def paste(self):
		pass
	
	def deleteSelection(self):
		pass
	
	def duplicateSelection(self):
		pass
	
	def selectAll(self):
		pass
	
	def selectNone(self):
		pass
	
	def mouseUp(self, modifiers):
		print "mouseUp at (%s, %s)" % tuple(self.mouse1)
	
	def mouseDown(self, modifiers):
		print "mouseDown at (%s, %s)" % tuple(self.mouse1)
	
	def mouseDragged(self, modifiers):
		print "mouseDragged from (%s, %s) to (%s, %s)" % (tuple(self.mouse0) + tuple(self.mouse1))
	
	def optionDown(self):
		pass
	
	def optionUp(self):
		pass
	
	def commandDown(self):
		pass
	
	def commandUp(self):
		pass
	
	def shiftDown(self):
		pass
	
	def shiftUp(self):
		pass
	
	# wxPython
	
	if not usePyObjC:
		def __init__(self, document):
			super(ForgeryMode, self).__init__()
			self.document = document

[ # palette
[65535, 0, 0],
[54894, 0, 0],
[44254, 0, 0],
[33613, 0, 0],
[22973, 0, 0],
[12332, 0, 0],
[0, 0, 65535],
[0, 0, 54109],
[0, 0, 42683],
[0, 0, 31257],
[0, 0, 19831],
[0, 0, 8405],
[0, 65535, 0],
[0, 54535, 0],
[0, 43535, 0],
[0, 32535, 0],
[0, 21535, 0],
[0, 10535, 0],
[55535, 55535, 55535],
[50892, 50892, 50892],
[46428, 46428, 46428],
[41875, 41875, 41875],
[37321, 37321, 37321],
[32768, 32768, 32768],
[28214, 28214, 28214],
[23661, 23661, 23661],
[19107, 19107, 19107],
[14554, 14554, 14554],
[10000, 10000, 10000],
]

modes = {}

import ForgeryDrawMode
import ForgeryTextureMode
