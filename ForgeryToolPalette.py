# ForgeryToolPalette.py
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
	'ForgeryToolPalette',
)

import ForgeryPalette, ForgeryTool
from tracer import traced

class ForgeryToolPalette(ForgeryPalette.ForgeryPaletteDelegate):
	tools = None
	title = u"Tools"
	currentObject = property(
		fget = lambda self: self.mode.tool,
		fset = lambda self, value: self.mode.changeTool(value),
	)
	
	@traced
	def setupElements(self):
		if not self.tools:
			self.tools = {}
			for toolID, tool in ForgeryTool.tools.iteritems():
				self.tools[toolID] = tool(self.mode.document)
		self.elements = {}
		self.icons = {}
		for toolID, tool in self.tools.iteritems():
			self.elements[tool.position] = toolID
			self.icons[tool.position] = tool.icon
	
	#def deactivate(self, obj):
	#	self.mode.currentTool.deactivate()
	
	#def activate(self, obj):
	#	self.mode.currentTool.activate()
	
	def doubleClick(self, obj):
		self.mode.currentTool.doubleClick()
