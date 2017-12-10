#!/usr/bin/env python2.6

# ForgeryTextureView.py
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
	'ForgeryTextureView',
)

import ForgeryElements, ForgeryViewDelegate

from OpenGL.GL import *
from OpenGL.GLU import *

from tracer import traced

class ForgeryTextureView(ForgeryViewDelegate.ForgeryViewDelegate):
	textures = None
	
	@property
	def which(self):
		return self.currentMode.which
	
	# Shared
	
	@traced
	def texturesUpdated(self):
		self.textures = {}
		self.view.refresh()
	
	def draw(self):
		super(ForgeryTextureView, self).draw()
		
		self.loadTextures()
		
		self.drawGrid()
		self.drawData()
	
	@traced
	def loadTextures(self):
		keys = self.data.textures.keys()
		if set(self.textures.keys()) != set(keys):
			glDeleteTextures(self.textures.values())
			ids = glGenTextures(len(keys))
			try:
				self.textures = dict(zip(keys, ids))
			except TypeError:
				self.textures = {keys[0]: ids}
			for key, texID in self.textures.iteritems():
				texture = self.data.textures[key]
				w, h = texture.size
				image = texture.toRGBA()
				
				glBindTexture(GL_TEXTURE_2D, texID)
				
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
		if self.data:
			for p in self.data.polygons.values():
				texID = self.textures.get(getattr(p, self.which).texture.elementID, 0)
				glBindTexture(GL_TEXTURE_2D, texID)
				glBegin(GL_POLYGON)
				p.drawSelf(textured = self.which)
				glEnd()
			glBindTexture(GL_TEXTURE_2D, 0)
			self.drawLines()
			self.drawVertices()
	
	if usePyObjC:
		
		@traced
		def init(self):
			self = super(ForgeryTextureView, self).init()
			if self:
				self.textures = {}
			return self
		
	else:
		
		def __init__(self, document):
			super(ForgeryTextureView, self).__init__(document)
			self.textures = {}

if __name__ == '__main__':
	import Forgery
	Forgery.main()
