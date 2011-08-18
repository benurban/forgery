# ForgeryDrawMode.py
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
	'ForgeryDrawMode',
)

import ForgeryDrawView, ForgeryMode, ForgeryPalette, ForgeryToolPalette
from tracer import traced

class ForgeryDrawMode(ForgeryMode.ForgeryMode):
	modeID = ID.DRAW_MODE
	tool = ID.SELECT_TOOL
	
	@property
	def tools(self):
		return self.paletteDelegate.tools
	@property
	def currentTool(self):
		return self.tools[self.tool]
	
	# Shared
	
	@traced
	def activate(self):
		super(ForgeryDrawMode, self).activate()
		self.currentTool.activate()
	
	@traced
	def deactivate(self):
		self.currentTool.deactivate()
		super(ForgeryDrawMode, self).deactivate()
	
	@traced
	def changeTool(self, toolID):
		if toolID != self.tool:
			self.currentTool.deactivate()
			self.tool = toolID
			self.currentTool.activate()
			ForgeryPalette.sharedPalette().updateSelection()
	
	@traced
	def validateUI(self, itemID):
		result = self.currentTool.validateUI(itemID)
		if result is None:
			result = super(ForgeryDrawMode, self).validateUI(itemID)
		return result
	
	@traced
	def getStatusText(self):
		return self.currentTool.getStatusText()
	
	@traced
	def cutSelection(self):
		return self.currentTool.cutSelection()
	
	@traced
	def copySelection(self):
		return self.currentTool.copySelection()
	
	@traced
	def paste(self):
		return self.currentTool.paste()
	
	@traced
	def deleteSelection(self):
		return self.currentTool.deleteSelection()
	
	@traced
	def duplicateSelection(self):
		return self.currentTool.duplicateSelection()
	
	@traced
	def selectAll(self):
		return self.currentTool.selectAll()
	
	@traced
	def selectNone(self):
		return self.currentTool.selectNone()
	
	@traced
	def mouseUp(self, modifiers):
		return self.currentTool.mouseUp(modifiers)
	
	@traced
	def mouseDown(self, modifiers):
		return self.currentTool.mouseDown(modifiers)
	
	@traced
	def mouseDragged(self, modifiers):
		return self.currentTool.mouseDragged(modifiers)
	
	@traced
	def optionDown(self):
		self.currentTool.optionDown()
	
	@traced
	def optionUp(self):
		self.currentTool.optionUp()
	
	@traced
	def commandDown(self):
		self.currentTool.commandDown()
	
	@traced
	def commandUp(self):
		self.currentTool.commandUp()
	
	@traced
	def shiftDown(self):
		self.currentTool.shiftDown()
	
	@traced
	def shiftUp(self):
		self.currentTool.shiftUp()
	
	if usePyObjC:
		
		@traced
		def awakeFromNib(self):
			self.paletteDelegate = ForgeryToolPalette.ForgeryToolPalette.alloc().initWithMode_(self)
		
	else:
		
		def __init__(self, *posArgs, **kwdArgs):
			super(ForgeryDrawMode, self).__init__(*posArgs, **kwdArgs)
			self.viewDelegate = ForgeryDrawView.ForgeryDrawView(self.document)
			self.paletteDelegate = ForgeryToolPalette.ForgeryToolPalette(self)

ForgeryMode.modes[ForgeryDrawMode.modeID] = ForgeryDrawMode
