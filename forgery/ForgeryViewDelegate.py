# ForgeryViewDelegate.py
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

from OpenGL.GL import *
from OpenGL.GLU import *

import ForgeryElements

__all__ = (
	'ForgeryViewDelegate',
)

if usePyObjC:
	
	from PyObjCTools import NibClassBuilder
	
	Superclass = NibClassBuilder.AutoBaseClass
	
else:
	
	Superclass = object

class ForgeryViewDelegate(Superclass):
	if not usePyObjC:
		document = None
	
	data = property(fget = lambda self: self.document and self.document.data)
	view = property(fget = lambda self: self.document and self.document.view)
	currentMode = property(fget = lambda self: self.document and self.document.currentMode)
	preferences = property(fget = lambda self: self.document and self.document.preferences)
	anchorPointColor = property(fget = lambda self: self.preferences and self.preferences.anchorPointColor)
	backgroundColor = property(fget = lambda self: self.preferences and self.preferences.backgroundColor)
	externalLineColor = property(fget = lambda self: self.preferences and self.preferences.externalLineColor)
	gridColor = property(fget = lambda self: self.preferences and self.preferences.gridColor)
	gridSpacing = property(fget = lambda self: self.preferences and self.preferences.gridSpacing)
	internalLineColor = property(fget = lambda self: self.preferences and self.preferences.internalLineColor)
	vertexColor = property(fget = lambda self: self.preferences and self.preferences.vertexColor)
	
	center = property(fget = lambda self: self.view.center)
	clipMax = property(fget = lambda self: self.view.clipMax)
	clipMin = property(fget = lambda self: self.view.clipMin)
	player = property(fget = lambda self: self.view.player)
	scrollMax = property(fget = lambda self: self.view.scrollMax)
	scrollMin = property(fget = lambda self: self.view.scrollMin)
	scrollPos = property(fget = lambda self: self.view.scrollPos)
	scrollSize = property(fget = lambda self: self.view.scrollSize)
	sizeInPixels = property(fget = lambda self: self.view.sizeInPixels)
	zoomFactor = property(fget = lambda self: self.view.zoomFactor)
	
	if not usePyObjC:
		def __init__(self, document):
			super(ForgeryViewDelegate, self).__init__()
			self.document = document
	
	def texturesUpdated(self):
		pass
	
	#def pixelToUnit(self, *posArgs, **kwdArgs):
	#	result = ForgeryPoint.ForgeryPoint(*posArgs, **kwdArgs)
	#	if not usePyObjC:
	#		result.y = (self.view.sizeInPixels.y - 1) - result.y
	#	result -= self.view.sizeInPixels / 2.0
	#	result *= self.zoomFactor
	#	result.coordinates = 'object'
	#	return result + self.center
	
	def draw(self):
		if usePyObjC:
			#xmin, ymin = self.scrollMin.asObject
			#xmax, ymax = self.scrollMax.asObject
			xmin, ymin = self.clipMin.asObject
			xmax, ymax = self.clipMax.asObject
			#xmin, ymin = self.center - (self.sizeInPixels.asView - (1, 1)) * self.zoomFactor / 2.0
			#xmax, ymax = self.center + (self.sizeInPixels.asView - (1, 1)) * self.zoomFactor / 2.0
		else:
			xmin, ymax = self.clipMin.asObject
			xmax, ymin = self.clipMax.asObject
			#width, height = self.sizeInPixels.asView
			#xmin, ymin = self.pixelToUnit('clip', self.view, 0, height - 1)
			#xmax, ymax = self.pixelToUnit('clip', self.view, width - 1, 0)
		
		glClearColor(self.backgroundColor[0], self.backgroundColor[1], self.backgroundColor[2], 1.0)
		glClearDepth(1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
		glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
		glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
		
		glMatrixMode(GL_PROJECTION)
		gluOrtho2D(xmin, xmax, ymin, ymax)
		glMatrixMode(GL_MODELVIEW)
		
		self.drawGrid()

	def drawGrid(self):
		if usePyObjC:
			xmin, ymin = self.scrollMin.asObject
			xmax, ymax = self.scrollMax.asObject
		else:
			xmin, ymax = self.scrollMin.asObject
			xmax, ymin = self.scrollMax.asObject
		
		gridSpacing = float(WU) / float(self.gridSpacing)
		gridMinorXmin = roundDown(xmin, gridSpacing) - gridSpacing
		gridMinorXmax = roundUp(xmax, gridSpacing) + gridSpacing
		gridMinorYmin = roundDown(ymin, gridSpacing) - gridSpacing
		gridMinorYmax = roundUp(ymax, gridSpacing) + gridSpacing
		
		gridMajorXmin = roundDown(xmin, WU) - WU
		gridMajorXmax = roundUp(xmax, WU) + WU
		gridMajorYmin = roundDown(ymin, WU) - WU
		gridMajorYmax = roundUp(ymax, WU) + WU
		
		# grid minor
		glColor3f(*self.gridColor)
		glBegin(GL_LINES)
		x = gridMinorXmin
		while x <= gridMinorXmax:
			glVertex2f(x, gridMinorYmin)
			glVertex2f(x, gridMinorYmax)
			x += gridSpacing
		y = gridMinorYmin
		while y <= gridMinorYmax:
			glVertex2f(gridMinorXmin, y)
			glVertex2f(gridMinorXmax, y)
			y += gridSpacing
		glEnd()
		
		# grid major
		r = 1.0 * self.zoomFactor
		
		glColor3f(*self.anchorPointColor)
		glBegin(GL_LINES)
		y = gridMajorYmin
		while y <= gridMajorYmax:
			x = gridMajorXmin
			while x <= gridMajorXmax:
				glVertex2f(x - r, y)
				glVertex2f(x + r, y)
				glVertex2f(x, y - r)
				glVertex2f(x, y + r)
				x += WU
			y += WU
		glEnd()
	
	def drawLines(self):
		glBegin(GL_LINES)
		for l in self.data.lines.values():
			if l.side0:
				glColor3f(*self.internalLineColor)
			else:
				glColor3f(*self.externalLineColor)
			glVertex2f(l.x0, l.y0)
			if l.side1:
				glColor3f(*self.internalLineColor)
			else:
				glColor3f(*self.externalLineColor)
			glVertex2f(l.x1, l.y1)
			#l.drawSelf()
		glEnd()
	
	def drawVertices(self):
		glPointSize(2.0)
		glBegin(GL_POINTS)
		for v in self.data.vertices.values():
			glColor3f(*self.vertexColor)
			v.drawSelf()
		glEnd()
		glPointSize(1.0)
