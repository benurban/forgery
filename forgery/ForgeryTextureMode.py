# ForgeryTextureMode.py
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
	'ForgeryTextureMode',
	'ForgeryCeilingTextureMode',
	'ForgeryFloorTextureMode',
)

import ForgeryMode, ForgeryPalette, ForgeryTexturePalette, ForgeryTextureView

class ForgeryTextureMode(ForgeryMode.ForgeryMode):
	modeID = None
	texture = ''
	which = None
	
	textures = property(fget = lambda self: self.data and self.data.textures)
	currentTexture = property(fget = lambda self: self.textures and self.textures[self.texture])
	
	# Shared
	
	def texturesUpdated(self):
		ForgeryPalette.sharedPalette().update()
		self.view.texturesUpdated()
	
	def mouseDown(self, modifiers):
		if self.currentTexture.isBlank:
			self.openUndoGroup(u"Remove Texture")
		else:
			self.openUndoGroup(u"Apply Texture '%s'" % (self.texture, ))
		self.mouseDragged(modifiers)
	
	def mouseDragged(self, modifiers):
		pos = self.mouse1.convertTo('object')
		for p in self.data.polygons.itervalues():
			if pos in p:
				if getattr(p, self.which).texture is not self.currentTexture:
					self.data.setSurfaceTexture(getattr(p, self.which), self.currentTexture)
				break
	
	def mouseUp(self, modifiers):
		self.closeUndoGroup()
	
	# PyObjC
	
	def awakeFromNib(self):
		self.paletteDelegate = ForgeryTexturePalette.ForgeryTexturePalette.alloc().initWithMode_(self)
	
	# wxPython
	
	if not usePyObjC:
		
		def __init__(self, *posArgs, **kwdArgs):
			super(ForgeryTextureMode, self).__init__(*posArgs, **kwdArgs)
			self.viewDelegate = ForgeryTextureView.ForgeryTextureView(self.document)
			self.paletteDelegate = ForgeryTexturePalette.ForgeryTexturePalette(self)

class ForgeryCeilingTextureMode(ForgeryTextureMode):
	modeID = ID.CEILING_TEXTURES_MODE
	which = 'ceiling'

class ForgeryFloorTextureMode(ForgeryTextureMode):
	modeID = ID.FLOOR_TEXTURES_MODE
	which = 'floor'

ForgeryMode.modes[ForgeryCeilingTextureMode.modeID] = ForgeryCeilingTextureMode
ForgeryMode.modes[ForgeryFloorTextureMode.modeID] = ForgeryFloorTextureMode
