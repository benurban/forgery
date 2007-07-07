# ForgeryZoomTool.py
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
	'ForgeryZoomTool',
)

import ForgeryCursor, ForgeryTool

class ForgeryZoomTool(ForgeryTool.ForgeryTool):
	iconFileName = 'Lens.png'
	cursor = ForgeryCursor.zoomIn
	altCursor = ForgeryCursor.zoomOut
	toolID = ID.ZOOM_TOOL
	position = (2, 1)
	
	zoomRatio = 2
	
	def mouseDown(self, modifiers):
		self.view.pan(self.mouse1.convertTo('object') - self.center)
		if modifiers == (False, True, False): # option key is down
			self.view.zoom(1.0 / self.zoomRatio)
		else:
			self.view.zoom(self.zoomRatio)
	
	def mouseDragged(self, modifiers):
		pass
	
	def mouseUp(self, modifiers):
		pass
	
	def optionDown(self):
		self.setCursor(self.altCursor)
	
	def optionUp(self):
		self.setCursor(self.cursor)

ForgeryTool.tools[ForgeryZoomTool.toolID] = ForgeryZoomTool
