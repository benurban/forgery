# ForgeryViewDelegate.py
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

from OpenGL.GL import *
from OpenGL.GLU import *

import ForgeryElements

if usePyObjC:
	from Foundation import *

__all__ = (
	'ForgeryViewDelegate',
)

from tracer import traced

class ForgeryViewDelegate(NSObject if usePyObjC else object):
	if usePyObjC:
		document = objc.IBOutlet()
	else:
		document = None
	
	@property
	def data(self):
		return self.document.data
	@property
	def view(self):
		return self.document.view
	@property
	def currentMode(self):
		return self.document.currentMode
	@property
	def preferences(self):
		return self.document.preferences
	@property
	def anchorPointColor(self):
		return self.preferences.anchorPointColor
	@property
	def backgroundColor(self):
		return self.preferences.backgroundColor
	@property
	def externalLineColor(self):
		return self.preferences.externalLineColor
	@property
	def gridColor(self):
		return self.preferences.gridColor
	@property
	def gridSpacing(self):
		return self.preferences.gridSpacing
	@property
	def internalLineColor(self):
		return self.preferences.internalLineColor
	@property
	def invalidLineColor(self):
		return self.preferences.invalidLineColor
	@property
	def vertexColor(self):
		return self.preferences.vertexColor
	
	@property
	def center(self):
		return self.view.center
	@property
	def clipMax(self):
		return self.view.clipMax
	@property
	def clipMin(self):
		return self.view.clipMin
	@property
	def player(self):
		return self.view.player
	@property
	def scrollMax(self):
		return self.view.scrollMax
	@property
	def scrollMin(self):
		return self.view.scrollMin
	@property
	def scrollPos(self):
		return self.view.scrollPos
	@property
	def scrollSize(self):
		return self.view.scrollSize
	@property
	def sizeInPixels(self):
		return self.view.sizeInPixels
	@property
	def zoomFactor(self):
		return self.view.zoomFactor
	
	@property
	def realGridSpacing(self):
		result = float(WU) / float(self.gridSpacing)
		if self.zoomFactor > 16.0:
			result *= self.zoomFactor / 16.0
		return result
	
	if not usePyObjC:
		def __init__(self, document):
			super(ForgeryViewDelegate, self).__init__()
			self.document = document
	
	@traced
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
		
		gridSpacing = self.realGridSpacing
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
		glLineWidth(1.0)
		glBegin(GL_LINES)
		invalidLines = []
		for l in self.data.lines.itervalues():
			if not l.isValid(self.data):
				invalidLines.append(l)
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
		glEnd()
		glLineWidth(3.0)
		glBegin(GL_LINES)
		glColor4f(*self.invalidLineColor)
		for l in invalidLines:
			l.drawSelf()
		glEnd()
		glLineWidth(1.0)
	
	def drawVertices(self):
		glPointSize(2.0)
		glBegin(GL_POINTS)
		for v in self.data.vertices.values():
			glColor3f(*self.vertexColor)
			v.drawSelf()
		glEnd()
		glPointSize(1.0)
