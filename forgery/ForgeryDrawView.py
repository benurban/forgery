#!/usr/bin/env python2.5

# ForgeryDrawView.py
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
	'ForgeryDrawView',
)

import ForgeryElements, ForgeryViewDelegate

from OpenGL.GL import *
from OpenGL.GLU import *

if usePyObjC:
	
	from PyObjCTools import NibClassBuilder
	
	Superclass = NibClassBuilder.AutoBaseClass
	
else:
	
	Superclass = ForgeryViewDelegate.ForgeryViewDelegate

class ForgeryDrawView(Superclass):
	drawHooks = None
	concaveTexture = None
	
	platformEdgeColor = property(fget = lambda self: self.preferences and self.preferences.platformEdgeColor)
	polygonColor = property(fget = lambda self: self.preferences and self.preferences.polygonColor)
	
	# Shared
	
	def draw(self):
		super(ForgeryDrawView, self).draw()
		
		for hook in self.drawHooks:
			hook()

	def addDrawHook(self, hook):
		self.drawHooks.append(hook)
	
	def removeDrawHook(self, hook):
		try:
			del self.drawHooks[self.drawHooks.index(hook)]
		except ValueError:
			print "Can't find draw hook %r" % (hook, )
	
	def loadTexture(self):
		if not self.concaveTexture:
			texture = ForgeryElements.ForgeryTexture('')
			w, h = texture.size
			image = texture.toRGBA()
			
			self.concaveTexture = glGenTextures(1)
			
			glBindTexture(GL_TEXTURE_2D, self.concaveTexture)
			
			glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
			glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
			glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
			
			glEnable(GL_TEXTURE_2D)
			
			glBindTexture(GL_TEXTURE_2D, 0)
	
	def drawData(self):
		self.loadTexture()
		
		if self.data:
			for p in self.data.polygons.values():
				if p.isConvex():
					glColor3f(*self.polygonColor)
					glBegin(GL_POLYGON)
					p.drawSelf()
					glEnd()
				else:
					glBindTexture(GL_TEXTURE_2D, self.concaveTexture)
					glBegin(GL_POLYGON)
					p.drawSelf(textured = True)
					glEnd()
					glBindTexture(GL_TEXTURE_2D, 0)
			self.drawLines()
			self.drawVertices()
		
	def drawPlayerPos(self):
		size = 3.5 * self.zoomFactor
		player = self.player.convertTo('object')
		
		glColor3f(0.0, 0.0, 0.0)
		glBegin(GL_LINES)
		glVertex2f(*tuple(player + (-size, -size)))
		glVertex2f(*tuple(player + (size, size)))
		glVertex2f(*tuple(player + (-size, size)))
		glVertex2f(*tuple(player + (size, -size)))
		glEnd()
	
	# PyObjC
	
	def init(self):
		self = super(ForgeryDrawView, self).init()
		self.drawHooks = []
		self.addDrawHook(self.drawData)
		self.addDrawHook(self.drawPlayerPos)
		return self
	
	# wxPython
	
	if not usePyObjC:
		
		def __init__(self, document):
			super(ForgeryDrawView, self).__init__(document)
			
			self.drawHooks = []
			self.addDrawHook(self.drawData)
			self.addDrawHook(self.drawPlayerPos)

if __name__ == '__main__':
	import Forgery
	Forgery.main()
