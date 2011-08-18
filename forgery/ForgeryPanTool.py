# ForgeryPanTool.py
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
	'ForgeryPanTool',
)

import ForgeryCursor, ForgeryTool

from tracer import traced

class ForgeryPanTool(ForgeryTool.ForgeryTool):
	iconFileName = 'Hand.png'
	cursor = ForgeryCursor.openHand
	altCursor = ForgeryCursor.closedHand
	toolID = ID.PAN_TOOL
	position = (2, 0)
	
	@traced
	def mouseDown(self, modifiers):
		self.setCursor(self.altCursor)
	
	def mouseDragged(self, modifiers):
		self.view.pan(self.mouse1.convertTo('object') - self.mouse0.convertTo('object'))
	
	@traced
	def mouseUp(self, modifiers):
		self.setCursor(self.cursor)

ForgeryTool.tools[ForgeryPanTool.toolID] = ForgeryPanTool
