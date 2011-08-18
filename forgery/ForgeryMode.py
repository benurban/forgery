# ForgeryMode.py
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

from ForgeryCommon import *

__all__ = (
	'ForgeryMode',
	'modes',
)

import ForgeryPalette

if usePyObjC:
	from Foundation import *

from tracer import traced

class ForgeryMode(NSObject if usePyObjC else object):
	modeID = None
	if usePyObjC:
		document = objc.IBOutlet()
		paletteDelegate = None #objc.IBOutlet() # for some reason it crashes upon quitting when I make it an objc.ivar
		statusBar = objc.IBOutlet()
		view = objc.IBOutlet()
		viewDelegate = objc.IBOutlet()
	else:
		document = None
		paletteDelegate = None
		@property
		def view(self):
			return self.document.view
		viewDelegate = None
	
	@property
	def app(self):
		return self.document.app
	@property
	def palette(self):
		return self.app.palette
	@property
	def inspector(self):
		return self.app.inspector
	@property
	def preferences(self):
		return self.document.preferences
	@property
	def snapToGrid(self):
		return self.preferences.snapToGrid
	@property
	def gridSpacing(self):
		return self.preferences.gridSpacing
	@property
	def mouse0(self):
		return self.view.mouse0
	@property
	def mouse1(self):
		return self.view.mouse1
	@property
	def data(self):
		return self.document.data
	
	# Shared
	
	@traced
	def refresh(self):
		return self.view.refresh()
	
	@traced
	def openUndoGroup(self, name = None):
		return self.document.openUndoGroup(name)
	
	@traced
	def closeUndoGroup(self, name = None):
		return self.document.closeUndoGroup(name)
	
	@traced
	def activate(self):
		self.palette.delegate = self.paletteDelegate
		self.palette.update()
		self.inspector.update()
		self.refresh()
	
	@traced
	def deactivate(self):
		self.refresh()
	
	@traced
	def documentActivated(self):
		self.palette.delegate = self.paletteDelegate
		self.palette.update()
	
	@traced
	def documentDeactivated(self):
		pass
	
	@traced
	def documentClosed(self):
		pass
	
	@traced
	def texturesUpdated(self):
		pass
	
	@traced
	def validateUI(self, itemID):
		if ID.MODES_START <= itemID <= ID.MODES_END:
			if itemID in modes:
				return True
			else:
				return False
		else:
			return None
	
	@traced
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
	
	@traced
	def getStatusText(self):
		return u""
	
	@traced
	def cutSelection(self):
		pass
	
	@traced
	def copySelection(self):
		pass
	
	@traced
	def paste(self):
		pass
	
	@traced
	def deleteSelection(self):
		pass
	
	@traced
	def duplicateSelection(self):
		pass
	
	@traced
	def selectAll(self):
		pass
	
	@traced
	def selectNone(self):
		pass
	
	@traced
	def mouseUp(self, modifiers):
		print u"mouseUp at (%s, %s)" % tuple(self.mouse1)
	
	@traced
	def mouseDown(self, modifiers):
		print u"mouseDown at (%s, %s)" % tuple(self.mouse1)
	
	def mouseDragged(self, modifiers):
		print u"mouseDragged from (%s, %s) to (%s, %s)" % (tuple(self.mouse0) + tuple(self.mouse1))
	
	@traced
	def optionDown(self):
		pass
	
	@traced
	def optionUp(self):
		pass
	
	@traced
	def commandDown(self):
		pass
	
	@traced
	def commandUp(self):
		pass
	
	@traced
	def shiftDown(self):
		pass
	
	@traced
	def shiftUp(self):
		pass
	
	# wxPython
	
	if usePyObjC:
		
		@traced
		def init(self):
			self = super(ForgeryMode, self).init()
			if self and not self.paletteDelegate:
				self.paletteDelegate = ForgeryPalette.ForgeryPaletteDelegate.alloc().initWithMode_(self)
			return self
		
	else:
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
