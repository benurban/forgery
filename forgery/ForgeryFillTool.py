# ForgeryFillTool.py
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
	'ForgeryFillTool',
)

import ForgeryCursor, ForgeryTool

class ForgeryFillTool(ForgeryTool.ForgeryTool):
	iconFileName = 'Bucket.png'
	cursor = ForgeryCursor.bucket
	toolID = ID.FILL_TOOL
	position = (1, 1)
	
	def mouseDown(self, modifiers):
		polygon = self.data.fillPolygon(self.mouse1.convertTo('object'))
		self.openUndoGroup(u"Fill Polygon '%s'" % (polygon.elementID, ))
		self.data.addElement(polygon)
		self.closeUndoGroup()
		self.refresh()
	
	def mouseDragged(self, modifiers):
		pass
	
	def mouseUp(self, modifiers):
		pass

ForgeryTool.tools[ForgeryFillTool.toolID] = ForgeryFillTool
