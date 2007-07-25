# ForgeryPreferences.py
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
	'ForgeryDocumentPreferences',
	'ForgeryPreferences',
	'sharedPreferences',
)

if usePyObjC:
	
	from PyObjCTools import NibClassBuilder
	
	Superclass = NibClassBuilder.AutoBaseClass
	
else:
	
	Superclass = object

def unsetValue(key):
	return property(
		fget = lambda self: self.__dict__.get(key, getattr(sharedPreferences(), key)),
		fset = lambda self, value: self.__dict__.__setitem__(key, value),
		fdel = lambda self: self.__dict__.__delitem__(key),
	)

class ForgeryDocumentPreferences(Superclass):
	attributes = (
		'anchorPointColor',
		'backgroundColor',
		'centerPosition',
		'externalLineColor',
		'gridColor',
		'gridSpacing',
		'inspectorIsDocked',
		'inspectorIsVisible',
		'inspectorPosition',
		'internalLineColor',
		'layerChangeAltersHeights',
		'paletteIsDocked',
		'paletteIsVisible',
		'palettePosition',
		'platformEdgeColor',
		'playerPosition',
		'polygonColor',
		'selectionColor',
		'snapToGrid',
		'vertexColor',
		'windowPosition',
		'windowSize',
		'zoomFactor',
	)
	
	def isDefault(self, key):
		if key in self.__dict__:
			return False
		else:
			return True
	
	def update(self, other):
		for key in self.attributes:
			if not other.isDefault(key):
				setattr(self, key, getattr(other, key))

for key in ForgeryDocumentPreferences.attributes:
	setattr(ForgeryDocumentPreferences, key, unsetValue(key))
del key

class ForgeryPreferences(ForgeryDocumentPreferences):
	_sharedPreferences = None
	
	anchorPointColor = (0.0 / 255.0, 200.0 / 255.0, 197.0 / 255.0)
	backgroundColor = (67.0 / 255.0, 67.0 / 255.0, 67.0 / 255.0)
	centerPosition = (0.0, 0.0)
	externalLineColor = (0.0 / 255.0, 0.0 / 255.0, 0.0 / 255.0)
	gridColor = (137.0 / 255.0, 137.0 / 255.0, 137.0 / 255.0)
	gridSpacing = 8
	inspectorIsDocked = True
	inspectorIsVisible = True
	inspectorPosition = None
	internalLineColor = (0.0 / 255.0, 200.0 / 255.0, 197.0 / 255.0)
	layerChangeAltersHeights = True
	paletteIsDocked = True
	paletteIsVisible = True
	palettePosition = None
	platformEdgeColor = (0.0 / 255.0, 255.0 / 255.0, 45.0 / 255.0)
	playerPosition = (0.0, 0.0)
	polygonColor = (214.0 / 255.0, 214.0 / 255.0, 214.0 / 255.0)
	selectionColor = (255.0 / 255.0, 196.0 / 255.0, 51.0 / 255.0)
	snapToGrid = True
	vertexColor = (255.0 / 255.0, 0.0 / 255.0, 0.0 / 255.0)
	windowPosition = None
	windowSize = (514, 456)
	#windowSize = (272, 272)
	zoomFactor = 16.0
	
	def createDocument(self, data):
		if usePyObjC:
			result = ForgeryDocumentPreferences.alloc().init()
		else:
			result = ForgeryDocumentPreferences()
		result.update(self)
		return result
	
	@classmethod
	def sharedPreferences(cls):
		if not cls._sharedPreferences:
			if usePyObjC:
				cls._sharedPreferences = cls.alloc().init()
			else:
				cls._sharedPreferences = cls()
		return cls._sharedPreferences

def sharedPreferences():
	return ForgeryPreferences.sharedPreferences()
