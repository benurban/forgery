# ForgeryPoint.py
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
	'ForgeryPoint',
	'ForgerySize',
)

import ForgeryView

if usePyObjC:
	
	from Foundation import *
	
else:
	
	import wx

class ForgeryPoint(object):
	possibleCoordinates = (
		'screen',
		'window',
		'clip',
		'view',
		'object',
	)
	coordinatesIndex = None
	view = None
	x = None
	y = None
	r2 = property(fget = lambda self: self._getR2())
	r = property(fget = lambda self: math.sqrt(self.r2))
	theta = property(fget = lambda self: math.atan2(self.y, self.x))
	coordinates = property(
		fget = lambda self: self.possibleCoordinates[self.coordinatesIndex],
		fset = lambda self, value: setattr(self, 'coordinatesIndex', list(self.possibleCoordinates).index(value)),
	)
	asScreen = property(fget = lambda self: self.convertToScreen())
	asWindow = property(fget = lambda self: self.convertToWindow())
	asClip = property(fget = lambda self: self.convertToClip())
	asView = property(fget = lambda self: self.convertToView())
	asObject = property(fget = lambda self: self.convertToObject())
	
	def __init__(self, coordinates, view = None, x = None, y = None):
		if isinstance(coordinates, ForgeryPoint):
			if view is None:
				view = coordinates.view
				x, y = coordinates.x, coordinates.y
				coordinates = coordinates.coordinates
			elif y is None:
				raise TypeError, "__init__() takes exactly 2 arguments (5 given)"
			elif x is None:
				raise TypeError, "__init__() takes exactly 2 arguments (4 given)"
			else:
				raise TypeError, "__init__() takes exactly 2 arguments (3 given)"
		elif hasattr(x, '__iter__'):
			if y is None:
				x, y = x
			else:
				raise TypeError, "__init__() takes exactly 4 arguments (5 given)"
		elif usePyObjC and isinstance(x, NSPoint):
			if y is None:
				x, y = x.x, x.y
			else:
				raise TypeError, "__init__() takes exactly 4 arguments (5 given)"
		elif usePyObjC and isinstance(x, NSSize):
			if y is None:
				x, y = x.width, x.height
			else:
				raise TypeError, "__init__() takes exactly 4 arguments (5 given)"
		elif not usePyObjC and isinstance(x, (wx.Point, wx.Point2D)):
			if y is None:
				x, y = x.x, x.y
			else:
				raise TypeError, "__init__() takes exactly 4 arguments (5 given)"
		elif not usePyObjC and isinstance(x, wx.Size):
			if y is None:
				x, y = x.width, x.height
			else:
				raise TypeError, "__init__() takes exactly 4 arguments (5 given)"
		if view is None:
			raise TypeError, "__init__() takes exactly 5 arguments (2 given)"
		elif x is None:
			raise TypeError, "__init__() takes exactly 5 arguments (3 given)"
		elif y is None:
			raise TypeError, "__init__() takes exactly 5 arguments (4 given)"
		elif coordinates not in self.possibleCoordinates:
			raise ValueError, "%s must be one of %s" % (coordinates, self.possibleCoordinates)
		elif not isinstance(view, ForgeryView.ForgeryView):
			raise TypeError, "Expected a ForgeryView instance, but found %s instead" % (view, )
		self.coordinates = coordinates
		self.view = view
		self.x = x
		self.y = y
	
	def __str__(self):
		return '<%s.%s: %s(%s, %s)>' % (__name__, self.__class__.__name__, self.coordinates, self.x, self.y)
	
	def __repr__(self):
		return '%s.%s(%r, %r, %r, %r)' % (__name__, self.__class__.__name__, self.coordinates, self.view, self.x, self.y)
	
	def __iter__(self):
		yield self.x
		yield self.y
	
	def __getitem__(self, index):
		if index == 0:
			return self.x
		elif index in (1, -1):
			return self.y
		else:
			raise IndexError, index
	
	def __neg__(self):
		return self * -1
	
	def __iadd__(self, other):
		if isinstance(other, ForgeryPoint):
			other = other.convertTo(self.coordinates)
		else:
			other = self.__class__(self.coordinates, self.view, other)
		self.x += other.x
		self.y += other.y
		return self
	
	def __add__(self, other):
		return self.__class__(self).__iadd__(other)
	
	def __isub__(self, other):
		if isinstance(other, ForgeryPoint):
			other = other.convertTo(self.coordinates)
		else:
			other = self.__class__(self.coordinates, self.view, other)
		self.x -= other.x
		self.y -= other.y
		return self
	
	def __sub__(self, other):
		return self.__class__(self).__isub__(other)
	
	def __imul__(self, other):
		self.x *= other
		self.y *= other
		return self
	
	def __mul__(self, other):
		return self.__class__(self).__imul__(other)
	
	def __idiv__(self, other):
		self.x /= other
		self.y /= other
		return self
	
	def __div__(self, other):
		return self.__class__(self).__idiv__(other)
	
	def _getR2(self):
		return self.x * self.x + self.y * self.y
	
	def scale(self, (sx, sy)):
		return self.__class__(self.coordinates, self.view, self.x * sx, self.y * sy)
	
	def convertToScreen(self):
		return self.convertTo('screen')
	
	def convertToWindow(self):
		return self.convertTo('window')
	
	def convertToClip(self):
		return self.convertTo('clip')
	
	def convertToView(self):
		return self.convertTo('view')
	
	def convertToObject(self):
		return self.convertTo('object')
	
	def convertTo(self, newCoordinates):
		return self.__class__(self).changeTo(newCoordinates)
	
	def changeToScreen(self):
		return self.changeTo('screen')
	
	def changeToWindow(self):
		return self.changeTo('window')
	
	def changeToClip(self):
		return self.changeTo('clip')
	
	def changeToView(self):
		return self.changeTo('view')
	
	def changeToObject(self):
		return self.changeTo('object')
	
	def changeTo(self, newCoordinates):
		if newCoordinates not in self.possibleCoordinates:
			raise ValueError, "%s must be one of %s" % (newCoordinates, self.possibleCoordinates)
		else:
			index = list(self.possibleCoordinates).index(newCoordinates)
			while self.coordinatesIndex < index - 1:
				self.changeTo(self.possibleCoordinates[self.coordinatesIndex + 1])
			while self.coordinatesIndex > index + 1:
				self.changeTo(self.possibleCoordinates[self.coordinatesIndex - 1])
			if self.coordinates != newCoordinates:
				x, y = getattr(self.__class__, '_convert%sTo%s' % (self.coordinates.capitalize(), newCoordinates.capitalize()))(self.view, self.x, self.y)
				self.coordinatesIndex, self.x, self.y = index, x, y
			return self
	
	if usePyObjC:
		
		@staticmethod
		def _convertScreenToWindow(view, x, y):
			left, top, right, bottom = view.document.getFrame()
			return (x - left, y - bottom)
		
		@staticmethod
		def _convertWindowToClip(view, x, y):
			result = view.scrollView.contentView().convertPoint_fromView_((x, y), None)
			return (result.x, result.y)
		
		@staticmethod
		def _convertClipToView(view, x, y):
			return tuple(view.clipMin.asView + (x, y))
			#origin = view.frame().origin
			#return (x - origin.x, y - origin.y)
			#dx = view.scrollView.horizontalScroller().floatValue()
			#dy = view.scrollView.verticalScroller().floatValue()
			#dx *= view.scrollWidth / view.zoomFactor
			#dy *= view.scrollHeight / view.zoomFactor
			#return x - dx, y - dy
		
		@staticmethod
		def _convertViewToObject(view, x, y):
			return (x * view.zoomFactor + view.scrollMin.x, y * view.zoomFactor + view.scrollMin.y)
			#return (x * view.zoomFactor - (view.center.x + view.sizeInPixels.x / 2.0)), (y * view.zoomFactor - (view.center.y + view.sizeInPixels.y / 2.0))
			#origin = view.bounds().origin
			#return (x * view.zoomFactor - origin.x), (y * view.zoomFactor - origin.y)
		
		@staticmethod
		def _convertObjectToView(view, x, y):
			return ((x - view.scrollMin.x) / view.zoomFactor, (y - view.scrollMin.y) / view.zoomFactor)
			#return (x + (view.center.x + view.sizeInPixels.x / 2.0)) / view.zoomFactor, (y + (view.center.y + view.sizeInPixels.y / 2.0)) / view.zoomFactor
			#origin = view.bounds().origin
			#return (x + origin.x) / view.zoomFactor, (y + origin.y) / view.zoomFactor
		
		@staticmethod
		def _convertViewToClip(view, x, y):
			return tuple(-view.clipMin.asView + (x, y))
			#origin = view.frame().origin
			#return (x + origin.x, y + origin.y)
		
		@staticmethod
		def _convertClipToWindow(view, x, y):
			result = view.scrollView.contentView().convertPoint_toView_((x, y), None)
			return (result.x, result.y)
		
		@staticmethod
		def _convertWindowToScreen(view, x, y):
			left, top, right, bottom = view.document.getFrame()
			return (x + left, y + bottom)
		
	else:
		
		@staticmethod
		def _convertScreenToWindow(view, x, y):
			left, top, right, bottom = view.document.getFrame()
			return (x - left, y - top)
		
		@staticmethod
		def _convertWindowToClip(view, x, y):
			rect = view.GetRect()
			return (x - rect.GetLeft(), y - rect.GetTop())
		
		@staticmethod
		def _convertClipToView(view, x, y):
			return tuple(view.clipMin.asView + (x, y))
		
		@staticmethod
		def _convertViewToObject(view, x, y):
			return (view.scrollMin.x + x * view.zoomFactor, view.scrollMin.y - y * view.zoomFactor)
		
		@staticmethod
		def _convertObjectToView(view, x, y):
			return ((x - view.scrollMin.x) / view.zoomFactor, (view.scrollMin.y - y) / view.zoomFactor)
		
		@staticmethod
		def _convertViewToClip(view, x, y):
			return tuple(-view.clipMin.asView + (x, y))
		
		@staticmethod
		def _convertClipToWindow(view, x, y):
			rect = view.GetRect()
			return (x + rect.GetLeft(), y + rect.GetTop())
		
		@staticmethod
		def _convertWindowToScreen(view, x, y):
			left, top, right, bottom = view.document.getFrame()
			return (x + left, y + top)

class ForgerySize(ForgeryPoint):
	@staticmethod
	def _convertScreenToWindow(view, x, y):
		return (x, y)
	
	@staticmethod
	def _convertWindowToClip(view, x, y):
		return (x, y)
	
	@staticmethod
	def _convertClipToView(view, x, y):
		return (x, y)
	
	@staticmethod
	def _convertViewToObject(view, x, y):
		return (x * view.zoomFactor, y * view.zoomFactor)
	
	@staticmethod
	def _convertObjectToView(view, x, y):
		return (x / view.zoomFactor, y / view.zoomFactor)
	
	@staticmethod
	def _convertViewToClip(view, x, y):
		return (x, y)
	
	@staticmethod
	def _convertClipToWindow(view, x, y):
		return (x, y)
	
	@staticmethod
	def _convertWindowToScreen(view, x, y):
		return (x, y)
