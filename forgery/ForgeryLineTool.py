# ForgeryLineTool.py
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
	'ForgeryLineTool',
)

import ForgeryCursor, ForgeryElements, ForgeryPoint, ForgeryTool

from OpenGL.GL import *

from tracer import traced

class ForgeryLineTool(ForgeryTool.ForgeryTool):
	iconFileName = 'Line.png'
	cursor = ForgeryCursor.cross
	toolID = ID.LINE_TOOL
	position = (0, 1)
	
	vertex0 = None
	vertex0IsNew = True
	vertex1 = None
	vertex1IsNew = True
	line = None
	modifiers = (False, False, False) # command, option, shift
	
	def __init__(self, *posArgs, **kwdArgs):
		super(ForgeryLineTool, self).__init__(*posArgs, **kwdArgs)
		self.vertex0 = None
		self.vertex0IsNew = True
		self.vertex1 = None
		self.vertex1IsNew = True
		self.line = None
		self.modifiers = (False, False, False) # command, option, shift
	
	@traced
	def activate(self):
		super(ForgeryLineTool, self).activate()
		self.addDrawHook(self.drawLine)
		self.refresh()
	
	@traced
	def deactivate(self):
		self.removeDrawHook(self.drawLine)
		super(ForgeryLineTool, self).deactivate()
		self.refresh()
	
	@traced
	def mouseDown(self, modifiers):
		self.modifiers = modifiers
		pos = self.mouse1.convertTo('object')
		if self.snapToGrid:
			gridSpacing = self.realGridSpacing
			pos = ForgeryPoint.ForgeryPoint(
				pos.coordinates,
				pos.view,
				roundToNearest(pos.x, gridSpacing),
				roundToNearest(pos.y, gridSpacing),
			)
		radius = self.vertexSelectionRadius * self.zoomFactor
		radius2 = radius * radius
		for v in self.data.vertices.values():
			if (pos - (v.x, v.y)).r2 <= radius2:
				self.vertex0 = v
				self.vertex0IsNew = False
				break
		else:
			self.vertex0 = ForgeryElements.ForgeryVertex(
				elementID = ForgeryElements.uniqueID('vertex %03d', self.data.vertices.iterkeys()),
				x = pos.x, y = pos.y,
			)
			self.vertex0IsNew = True
		self.refresh()
	
	def mouseDragged(self, modifiers):
		pos = self.mouse1.convertTo('object')
		if self.snapToGrid:
			gridSpacing = self.realGridSpacing
			pos = ForgeryPoint.ForgeryPoint(
				pos.coordinates,
				pos.view,
				roundToNearest(pos.x, gridSpacing),
				roundToNearest(pos.y, gridSpacing),
			)
		radius = self.vertexSelectionRadius * self.zoomFactor
		radius2 = radius * radius
		for v in self.data.vertices.values():
			if (pos - (v.x, v.y)).r2 < radius2:
				self.vertex1 = v
				self.vertex1IsNew = False
				break
		else:
			self.vertex1 = ForgeryElements.ForgeryVertex(
				elementID = ForgeryElements.uniqueID('vertex %03d', self.data.vertices.keys() + [self.vertex0.elementID]),
				x = pos.x, y = pos.y,
			)
			self.vertex1IsNew = True
		self.line = ForgeryElements.ForgeryLine(
			elementID = ForgeryElements.uniqueID('line %03d', self.data.lines.iterkeys()),
			vertex0 = self.vertex0,
			vertex1 = self.vertex1,
		)
		self.refresh()
	
	@traced
	def mouseUp(self, modifiers):
		if self.line:
			self.openUndoGroup(u"Draw Line '%s'" % (self.line.elementID, ))
		elif self.vertex0IsNew and self.vertex0:
			self.openUndoGroup(u"Draw Vertex '%s'" % (self.vertex0.elementID, ))
		elif self.vertex1IsNew and self.vertex1: # I don't think this can happen.
			self.openUndoGroup(u"Draw Vertex '%s'" % (self.vertex1.elementID, ))
		else:
			self.openUndoGroup() # to offset closeUndoGroup(), below
		if self.vertex0IsNew and self.vertex0:
			self.data.addElement(self.vertex0)
		if self.vertex1IsNew and self.vertex1:
			self.data.addElement(self.vertex1)
		if self.line:
			self.data.addElement(self.line)
		self.closeUndoGroup()
		self.line = None
		self.vertex1 = None
		self.vertex1IsNew = True
		self.vertex0 = None
		self.vertex0IsNew = True
		self.refresh()
	
	@traced
	def drawLine(self):
		if self.line:
			glColor3f(0.0, 0.0, 0.0)
			glBegin(GL_LINES)
			self.line.drawSelf()
			glEnd()
		
		glColor3f(1.0, 0.0, 0.0)
		glPointSize(2.0)
		glBegin(GL_POINTS)
		if self.vertex0 and self.vertex0IsNew:
			self.vertex0.drawSelf()
		if self.vertex1 and self.vertex1IsNew:
			self.vertex1.drawSelf()
		glEnd()
		glPointSize(1.0)

ForgeryTool.tools[ForgeryLineTool.toolID] = ForgeryLineTool
