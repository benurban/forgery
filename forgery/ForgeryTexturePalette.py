# ForgeryTexturePalette.py
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
	'ForgeryTexturePalette',
)

import ForgeryPalette

class ForgeryTexturePalette(ForgeryPalette.ForgeryPaletteDelegate):
	title = "Textures"
	textures = property(fget = lambda self: self.mode.textures)
	currentObject = property(
		fget = lambda self: getattr(self.mode, 'texture'),
		fset = lambda self, value: setattr(self.mode, 'texture', value),
	)
	
	def setupElements(self):
		cols = 16
		self.elements = {}
		self.icons = {}
		keys = self.textures.keys()
		keys.sort()
		for index, key in enumerate(keys):
			col = index % cols
			row = long((index - col) / cols)
			self.elements[(row, col)] = key
			self.icons[(row, col)] = self.textures[key] and self.textures[key].thumbnail
