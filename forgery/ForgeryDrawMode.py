# ForgeryDrawMode.py
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
	'ForgeryDrawMode',
)

import ForgeryDrawView, ForgeryMode, ForgeryPalette, ForgeryToolPalette

class ForgeryDrawMode(ForgeryMode.ForgeryMode):
	modeID = ID.DRAW_MODE
	tool = ID.SELECT_TOOL
	
	tools = property(fget = lambda self: self.paletteDelegate.tools)
	currentTool = property(fget = lambda self: self.tools[self.tool])
	
	# Shared
	
	def activate(self):
		super(ForgeryDrawMode, self).activate()
		self.currentTool.activate()
	
	def deactivate(self):
		self.currentTool.deactivate()
		super(ForgeryDrawMode, self).deactivate()
	
	def changeTool(self, toolID):
		if toolID != self.tool:
			self.currentTool.deactivate()
			self.tool = toolID
			self.currentTool.activate()
			ForgeryPalette.sharedPalette().updateSelection()
	
	def validateUI(self, itemID):
		result = self.currentTool.validateUI(itemID)
		if result is None:
			result = super(ForgeryDrawMode, self).validateUI(itemID)
		return result
	
	def getStatusText(self):
		return self.currentTool.getStatusText()
	
	def cutSelection(self):
		return self.currentTool.cutSelection()
	
	def copySelection(self):
		return self.currentTool.copySelection()
	
	def paste(self):
		return self.currentTool.paste()
	
	def deleteSelection(self):
		return self.currentTool.deleteSelection()
	
	def duplicateSelection(self):
		return self.currentTool.duplicateSelection()
	
	def selectAll(self):
		return self.currentTool.selectAll()
	
	def selectNone(self):
		return self.currentTool.selectNone()
	
	def mouseUp(self, modifiers):
		return self.currentTool.mouseUp(modifiers)
	
	def mouseDown(self, modifiers):
		return self.currentTool.mouseDown(modifiers)
	
	def mouseDragged(self, modifiers):
		return self.currentTool.mouseDragged(modifiers)
	
	def optionDown(self):
		self.currentTool.optionDown()
	
	def optionUp(self):
		self.currentTool.optionUp()
	
	def commandDown(self):
		self.currentTool.commandDown()
	
	def commandUp(self):
		self.currentTool.commandUp()
	
	def shiftDown(self):
		self.currentTool.shiftDown()
	
	def shiftUp(self):
		self.currentTool.shiftUp()
	
	# PyObjC
	
	def awakeFromNib(self):
		self.paletteDelegate = ForgeryToolPalette.ForgeryToolPalette.alloc().initWithMode_(self)
	
	# wxPython
	
	if not usePyObjC:
		
		def __init__(self, *posArgs, **kwdArgs):
			super(ForgeryDrawMode, self).__init__(*posArgs, **kwdArgs)
			self.viewDelegate = ForgeryDrawView.ForgeryDrawView(self.document)
			self.paletteDelegate = ForgeryToolPalette.ForgeryToolPalette(self)

ForgeryMode.modes[ForgeryDrawMode.modeID] = ForgeryDrawMode
