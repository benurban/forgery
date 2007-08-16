# ForgeryElements.py
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
	'ForgeryAction',
	'ForgeryElement',
	'ForgeryLayer',
	'ForgeryLight',
	'ForgeryLine',
	'ForgeryMoveableElement',
	'ForgeryPatternBufferAction',
	'ForgeryPolygon',
	'ForgeryRechargerAction',
	'ForgerySide',
	'ForgerySurface',
	'ForgerySwitchAction',
	'ForgeryTerminalAction',
	'ForgeryTexture',
	'ForgeryVertex',
	'uniqueID',
)

from OpenGL.GL import *

import math

class ForgeryElement(object):
	elementID = None
	parents = None
	parentCategories = None
	xmlClass = None
	category = None
	
	def __init__(self, elementID):
		super(ForgeryElement, self).__init__()
		self.elementID = elementID
		self.parents = {}
	
	def findParents(self, elements):
		for key, value in self.parents.copy().iteritems():
			if not isinstance(value, ForgeryElement) and value is not None:
				setattr(self, key, elements[self.parentCategories[key]][value])
	
	def __getitem__(self, key):
		return self.parents.__getitem__(key)
	
	def __setitem__(self, key, value):
		return self.parents.__setitem__(key, value)
	
	def __delitem__(self, key):
		return self.parents.__delitem__(key)
	
	def __str__(self):
		return "<%s id %r: %s>" % (self.__class__.__name__, self.elementID, self.parents)
	
	def __repr__(self):
		return '%s.%s%s' % (__name__, self.__class__.__name__, self.getParams())
	
	def getParams(self):
		return '(%r)' % (self.elementID, )
	
	def getChildren(self, data):
		result = []
		return tuple(result)
	
	def drawSelf(self):
		pass
	
	def toXML(self):
		result = []
		result.append('<%s id="%s"/>' % (self.xmlClass, self.elementID))
		return '\n'.join(result)
	
	def xmlReference(self, **extraAttributes):
		result = '<%s id="%s"' % (self.xmlClass, self.elementID)
		for name, value in extraAttributes.iteritems():
			result += ' %s="%s"' % (name, value)
		result += '/>'
		return result
	
	def getParents(self):
		return self.parents.itervalues()
	
	def isAncestor(self, other):
		if other is None:
			return False
		try:
			parents = other.getParents()
		except AttributeError:
			print "%r has no getParents method" % other
			return False
		for obj in parents:
			if self is obj or self.isAncestor(obj):
				return True
		else:
			return False

class ForgeryMoveableElement(ForgeryElement):
	def move(self, dx, dy):
		for v in self.getAllVertexAncestors():
			v.move(dx, dy)
	
	def getAllVertexAncestors(self):
		return set()

class ForgeryAction(object):
	kinds = {}
	kind = None
	event = 'actionButton'
	xmlClass = u'action'
	
	@classmethod
	def __new__(cls, kind, *posArgs, **kwdArgs):
		cls = ForgeryAction.kinds.get(kind, cls)
		return object.__new__(cls)
	
	def __init__(self, event = 'actionButton'):
		super(ForgeryAction, self).__init__()
		self.event = event
	
	def __repr__(self):
		return '%s.%s%s' % (__name__, self.__class__.__name__, self.getParams())
	
	def getParams(self):
		return repr((self.event, ))
	
	def findChildren(self, data):
		return
	
	def toXML(self):
		return '<%s kind="%s" event="%s"/>' % (self.xmlClass, self.kind, self.event)

class ForgerySwitchAction(ForgeryAction):
	kind = 'switch'
	stateChanges = None
	
	def __init__(self, event = 'actionButton', *stateChanges):
		super(ForgerySwitchAction, self).__init__(event)
		self.stateChanges = list(stateChanges)
	
	def findChildren(self, data):
		for i, (element, state) in enumerate(self.stateChanges):
			if not isinstance(element, (ForgeryElement, ForgerySide)):
				(tag, elementID) = element
				category = {
					'annotation': 'annotations',
					'layer':      'layers',
					'light':      'lights',
					'line':       'lines',
					'media':      'media',
					'object':     'objects',
					'polygon':    'polygons',
					'surface':    'surfaces',
					'texture':    'textures',
					'vertex':     'vertices',
				}[tag]
				self.stateChanges[i] = (data[category][elementID], state)
	
	def getParams(self):
		result = []
		result.append(repr(self.event))
		if not self.stateChanges:
			result.append('()')
		elif len(self.stateChanges) == 1:
			result.append('((self[%r][%r]' % (self.stateChanges[0][0].category, self.stateChanges[0][0].elementID))
			result.append('%r))' % (self.stateChanges[0][1], ))
		else:
			result.append('((self[%r][%r]' % (self.stateChanges[0][0].category, self.stateChanges[0][0].elementID))
			result.append('%r)' % (self.stateChanges[0][1], ))
			for element, state in self.stateChanges[1:-1]:
				result.append('(self[%r][%r]' % (element.category, element.elementID))
				result.append('%r)' % (state, ))
			result.append('(self[%r][%r]' % (self.stateChanges[-1][0].category, self.stateChanges[-1][0].elementID))
			result.append('%r))' % (self.stateChanges[-1][1], ))
		return '(' + ', '.join(result) + ')'
	
	def toXML(self):
		result = []
		tag = '<%s kind="%s" event="%s"' % (self.xmlClass, self.kind, self.event)
		if self.stateChanges:
			tag += '>'
			result.append(tag)
			for element, state in self.stateChanges:
				result.append(element.xmlReference(state = state))
		else:
			tag += '/>'
			result.append(tag)
		return '\n'.join(result)
ForgeryAction.kinds[ForgerySwitchAction.kind] = ForgerySwitchAction

class ForgeryPatternBufferAction(ForgeryAction):
	kind = 'pattern buffer'
ForgeryAction.kinds[ForgeryPatternBufferAction.kind] = ForgeryPatternBufferAction

class ForgeryTerminalAction(ForgeryAction):
	kind = 'terminal'
ForgeryAction.kinds[ForgeryTerminalAction.kind] = ForgeryTerminalAction

class ForgeryRechargerAction(ForgeryAction):
	kind = 'recharger'
	shieldRate = 0.0
	oxygenRate = 0.0
	shieldLimit = None
	oxygenLimit = None
	
	def __init__(self, shieldRate = 0.0, oxygenRate = 0.0, shieldLimit = None, oxygenLimit = None, event = 'actionButton'):
		super(ForgeryRechargerAction, self).__init__(event)
		self.shieldRate = shieldRate
		self.oxygenRate = oxygenRate
		self.shieldLimit = shieldLimit
		self.oxygenLimit = oxygenLimit
	
	def getParams(self):
		result = []
		result.append(repr(self.shieldRate))
		result.append(repr(self.oxygenRate))
		result.append(repr(self.shieldLimit))
		result.append(repr(self.oxygenLimit))
		result.append(repr(self.event))
		return '(' + ', '.join(result) + ')'
	
	def toXML(self):
		result = '<%s kind="%s" event="%s"' % (self.xmlClass, self.kind, self.event)
		if self.shieldRate:
			result += ' shieldRate="%s"' % (self.shieldRate, )
		if self.oxygenRate:
			result += ' oxygenRate="%s"' % (self.oxygenRate, )
		if self.shieldLimit is not None:
			result += ' shieldLimit="%s"' % (self.shieldLimit, )
		if self.oxygenLimit is not None:
			result += ' oxygenLimit="%s"' % (self.oxygenLimit, )
		result += '/>'
		return result
ForgeryAction.kinds[ForgeryRechargerAction.kind] = ForgeryRechargerAction

class ForgeryLayer(ForgeryElement):
	offset = 0
	
	parentCategories = {
	}
	xmlClass = u'layer'
	category = 'layers'
	
	def __init__(self, elementID, offset = 0):
		super(ForgeryLayer, self).__init__(elementID)
		self.offset = offset
	
	def getParams(self):
		result = []
		result.append(repr(self.elementID))
		result.append(repr(self.offset))
		return '(' + ','.join(result) + ')'
	
	def getChildren(self, data):
		result = []
		return tuple(result)
	
	def drawSelf(self):
		pass
	
	def toXML(self):
		result = []
		result.append('<%s id="%s" offset="%s"/>' % (self.xmlClass, self.elementID, self.offset))
		return '\n'.join(result)

class ForgeryLine(ForgeryMoveableElement):
	vertex0 = property(
		fget = lambda self: self.__getitem__('vertex0'),
		fset = lambda self, value: self.__setitem__('vertex0', value),
	)
	vertex1 = property(
		fget = lambda self: self.__getitem__('vertex1'),
		fset = lambda self, value: self.__setitem__('vertex1', value),
	)
	x0 = property(
		fget = lambda self: getattr(self.vertex0, 'x'),
		fset = lambda self, value: setattr(self.vertex0, 'x', value),
	)
	y0 = property(
		fget = lambda self: getattr(self.vertex0, 'y'),
		fset = lambda self, value: setattr(self.vertex0, 'y', value),
	)
	x1 = property(
		fget = lambda self: getattr(self.vertex1, 'x'),
		fset = lambda self, value: setattr(self.vertex1, 'x', value),
	)
	y1 = property(
		fget = lambda self: getattr(self.vertex1, 'y'),
		fset = lambda self, value: setattr(self.vertex1, 'y', value),
	)
	dx = property(fget = lambda self: self.x1 - self.x0)
	dy = property(fget = lambda self: self.y1 - self.y0)
	side0 = None
	side1 = None
	sides = property(fget = lambda self: (self.side0, self.side1))
	parentCategories = {
		'vertex0': 'vertices',
		'vertex1': 'vertices',
	}
	xmlClass = u'line'
	category = 'lines'
	
	def __init__(self, elementID, vertex0, vertex1, side0 = None, side1 = None):
		super(ForgeryLine, self).__init__(elementID = elementID)
		self.vertex0 = vertex0
		self.vertex1 = vertex1
		self.side0 = side0
		self.side1 = side1
	
	def __len__(self):
		return math.sqrt(self.lengthSquared())
	
	def getParams(self):
		result = []
		result.append(repr(self.elementID))
		result.append('self.vertices[%r]' % (self.vertex0.elementID, ))
		result.append('self.vertices[%r]' % (self.vertex1.elementID, ))
		result.append(repr(self.side0))
		result.append(repr(self.side1))
		return '(' + ', '.join(result) + ')'
	
	def getChildren(self, data):
		result = []
		for p in data.polygons.itervalues():
			if self in iter(p):
				result.append(p)
		return tuple(result)
	
	def drawSelf(self):
		glVertex2f(self.x0, self.y0)
		glVertex2f(self.x1, self.y1)
	
	def findParents(self, data):
		super(ForgeryLine, self).findParents(data)
		if self.side0:
			self.side0.findSurfaces(data)
		if self.side1:
			self.side1.findSurfaces(data)
	
	def toXML(self):
		result = []
		result.append('<%s id="%s">' % (self.xmlClass, self.elementID))
		result.append(self.vertex0.xmlReference())
		result.append(self.vertex1.xmlReference())
		if self.side0:
			result.append(self.side0.toXML(0))
		if self.side1:
			result.append(self.side1.toXML(1))
		result.append('</%s>' % (self.xmlClass, ))
		return '\n'.join(result)
	
	def lengthSquared(self):
		return (self.x1 - self.x0) * (self.x1 - self.x0) \
		     + (self.y1 - self.y0) * (self.y1 - self.y0)
	
	def distanceToPoint(self, x, y):
		# Algorithm obtained from http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/
		# (First Google hit for "distance between a point and a line")
		x0, y0 = self.x0, self.y0
		x1, y1 = self.x1, self.y1
		dx, dy = self.dx, self.dy
		if dx or dy:
			t = ((x - x0) * dx + (y - y0) * dy) / self.lengthSquared()
			if t < 0:
				return math.sqrt((x - x0) * (x - x0) + (y - y0) * (y - y0))
			elif t > 1:
				return math.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
			else:
				x2 = x0 + t * dx
				y2 = y0 + t * dy
				return math.sqrt((x - x2) * (x - x2) + (y - y2) * (y - y2))
		else:
			return math.sqrt((x - x0) * (x - x0) + (y - y0) * (y - y0))
	
	def isValid(self, data):
		if not len(self):
			return False
		else:
			polygons = self.getChildren(data)
			[polygon.findSides() for polygon in polygons]
			for polygon0 in polygons:
				i0 = list(polygon0).index(self)
				for polygon1 in polygons:
					if polygon0 is polygon1:
						continue
					else:
						i1 = list(polygon1).index(self)
						if polygon0.sides[i0] == polygon1.sides[i1]:
							return False
			else:
				return True
	
	def addSide(self, index, *posArgs, **kwdArgs):
		if index:
			self.side1 = ForgerySide(*posArgs, **kwdArgs)
		else:
			self.side0 = ForgerySide(*posArgs, **kwdArgs)
	
	def delSide(self, index):
		if index:
			self.side1 = None
		else:
			self.side0 = None
	
	def switchSide(self, index):
		side = 'side' + str(index)
		otherSide = 'side' + str(1 - index)
		if getattr(self, otherSide):
			if getattr(self, side): # there is a conflict
				pass # this will allow the side data to be kept when the conflict is resolved
			else:
				pass
		else:
			setattr(self, otherSide, getattr(self, side))
			setattr(self, side, None)
	
	def getAllVertexAncestors(self):
		result = set()
		result.update(self.vertex0.getAllVertexAncestors())
		result.update(self.vertex1.getAllVertexAncestors())
		return result

class ForgeryPolygon(ForgeryMoveableElement):
	layer = None
	floor = None
	floorOffset = 0.0
	ceiling = None
	ceilingOffset = 1.0
	xmlClass = u'polygon'
	category = 'polygons'
	sides = None
	vertices = property(fget = lambda self: self.getVertices())
	floorHeight = property(
		fget = lambda self: self.layer.offset + self.floorOffset,
		fset = lambda self, value: setattr(self, 'floorOffset', self.layer.offset - value),
	)
	ceilingHeight = property(
		fget = lambda self: self.layer.offset + self.ceilingOffset,
		fset = lambda self, value: setattr(self, 'ceilingOffset', self.layer.offset - value),
	)
	
	def __init__(self, elementID, layer, lines = (), floorOffset = 0.0, floor = None, ceilingOffset = 1.0, ceiling = None):
		super(ForgeryPolygon, self).__init__(elementID = elementID)
		self.parents = list(lines)
		self.floorOffset = floorOffset
		self.floor = floor
		self.ceilingOffset = ceilingOffset
		self.ceiling = ceiling
		self.layer = layer
	
	def findParents(self, elements):
		for index, parent in enumerate(self.parents):
			if not isinstance(parent, ForgeryElement) and parent is not None:
				self[index] = elements.lines[parent]
		if not isinstance(self.layer, ForgeryElement):
			self.layer = elements.layers[self.layer]
		if not isinstance(self.ceiling, ForgeryElement) and self.ceiling is not None:
			self.ceiling = elements.surfaces[self.ceiling]
		if not isinstance(self.floor, ForgeryElement) and self.floor is not None:
			self.floor = elements.surfaces[self.floor]
	
	def __iter__(self):
		return self.parents.__iter__()
	
	def __len__(self):
		return self.parents.__len__()
	
	def __contains__(self, other):
		x, y = iter(other)
		result = False
		for s in self:
			x0, y0, x1, y1 = s.x0, s.y0, s.x1, s.y1
			if (y0 <= y < y1 or y1 <= y < y0) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
				result = not result
		return result
	
	def getParams(self):
		result = []
		result.append(repr(self.elementID))
		result.append('self.layers[%r]' % (self.layer.elementID, ))
		result.append('(self.lines[%r]' % (self.parents[0].elementID, ))
		for l in self.parents[1:-1]:
			result.append('self.lines[%r]' % (l.elementID, ))
		result.append('self.lines[%r])' % (self.parents[-1].elementID, ))
		result.append(repr(self.floorOffset))
		if self.floor:
			result.append('self.surfaces[%r]' % (self.floor.elementID, ))
		else:
			result.append(repr(self.floor))
		result.append(repr(self.ceilingOffset))
		if self.ceiling:
			result.append('self.surfaces[%r]' % (self.ceiling.elementID, ))
		else:
			result.append(repr(self.ceiling))
		return '(' + ', '.join(result) + ')'
	
	def getChildren(self, data):
		result = []
		return tuple(result)
	
	def drawSelf(self, textured = False):
		for v in self.vertices:
			if textured == 'floor':
				glTexCoord2f(
					v.x / float(WU) + self.floor.scaledDx,
					v.y / float(WU) + self.floor.scaledDy,
				)
			elif textured == 'ceiling':
				glTexCoord2f(
					v.x / float(WU) + self.ceiling.scaledDx,
					v.y / float(WU) + self.ceiling.scaledDy,
				)
			elif textured:
				glTexCoord2f(v.x / float(WU), v.y / float(WU))
			glVertex2f(v.x, v.y)
	
	def findSides(self):
		v0 = self.parents[0].vertex0
		v1 = self.parents[0].vertex1
		if self.parents[1].vertex0 is v0 or self.parents[1].vertex1 is v0:
			v0, v1 = v1, v0
		v2 = (self.parents[1].vertex0 in (v0, v1)) and self.parents[1].vertex1 or self.parents[1].vertex0
		if angleBetween((v1.x - v0.x, v1.y - v0.y), (v2.x - v1.x, v2.y - v1.y)) > 0.0:
			self.reverse()
		# the polygon is now clockwise
		if self.parents[0].vertex0 is self.parents[1].vertex0 or \
		   self.parents[0].vertex0 is self.parents[1].vertex1:
			v = self.parents[0].vertex1
		else:
			v = self.parents[0].vertex0
		self.sides = []
		for l in self.parents:
			if v is l.vertex0:
				self.sides.append(0)
				v = l.vertex1
			else:
				self.sides.append(1)
				v = l.vertex0
	
	def reverse(self):
		if self.parents[0].vertex0 is self.parents[1].vertex0 or \
		   self.parents[0].vertex0 is self.parents[1].vertex1:
			v = self.parents[0].vertex1
		else:
			v = self.parents[0].vertex0
		for l in self.parents:
			if v is l.vertex0:
				l.switchSide(0)
				v = l.vertex1
			else:
				l.switchSide(1)
				v = l.vertex0
		self.parents.reverse()
	
	def getVertices(self):
		self.findSides()
		return [s and l.vertex1 or l.vertex0 for l, s in zip(self, self.sides)]
	
	def isConvex(self):
		vertices = self.vertices
		for A, B, C in zip(vertices[0:] + vertices[:0], vertices[1:] + vertices[:1], vertices[2:] + vertices[:2]):
			if angleBetween((B.x - A.x, B.y - A.y), (C.x - B.x, C.y - B.y)) > 0.0:
				return False
		else:
			return True
	
	def area(self):
		vertices = self.vertices
		vertices.reverse() # area formula is for a counterclockwise polygon
		# formula obtained from http://en.wikipedia.org/wiki/Polygon#Area
		length = len(vertices)
		result = 0.0
		for i, v in enumerate(vertices):
			result += v.x * (vertices[(i + 1) % length].y - vertices[i - 1].y)
		result /= 2.0
		return result
	
	def volume(self):
		return self.area * (self.ceilingOffset - self.floorOffset)
	
	def toXML(self):
		result = []
		result.append('<%s id="%s" layer="%s" floorOffset="%s" ceilingOffset="%s">' % (self.xmlClass, self.elementID, self.layer.elementID, self.floorOffset, self.ceilingOffset))
		if self.floor:
			result.append(self.floor.xmlReference(location = 'floor'))
		if self.ceiling:
			result.append(self.ceiling.xmlReference(location = 'ceiling'))
		for l in self:
			result.append(l.xmlReference())
		result.append('</%s>' % (self.xmlClass, ))
		return '\n'.join(result)
	
	def getParents(self):
		return iter(self)
	
	def getAllVertexAncestors(self):
		result = set()
		for l in self:
			result.update(l.getAllVertexAncestors())
		return result

class ForgerySide(object):
	upperSurface = None
	middleSurface = None
	lowerSurface = None
	
	def __init__(self, upperSurface = None, middleSurface = None, lowerSurface = None):
		super(ForgerySide, self).__init__()
		self.upperSurface = upperSurface
		self.middleSurface = middleSurface
		self.lowerSurface = lowerSurface
	
	def __repr__(self):
		return '%s.%s%s' % (__name__, self.__class__.__name__, self.getParams())
	
	def findSurfaces(self, data):
		if self.upperSurface and not isinstance(self.upperSurface, ForgerySurface):
			self.upperSurface = data.surfaces[self.upperSurface]
		if self.middleSurface and not isinstance(self.middleSurface, ForgerySurface):
			self.middleSurface = data.surfaces[self.middleSurface]
		if self.lowerSurface and not isinstance(self.lowerSurface, ForgerySurface):
			self.lowerSurface = data.surfaces[self.lowerSurface]
	
	def getParams(self):
		result = []
		if self.upperSurface:
			result.append('self.surfaces[%r]' % (self.upperSurface.elementID, ))
		else:
			result.append(repr(self.upperSurface))
		if self.middleSurface:
			result.append('self.surfaces[%r]' % (self.middleSurface.elementID, ))
		else:
			result.append(repr(self.middleSurface))
		if self.lowerSurface:
			result.append('self.surfaces[%r]' % (self.lowerSurface.elementID, ))
		else:
			result.append(repr(self.lowerSurface))
		return '(' + ', '.join(result) + ')'
	
	def toXML(self, index):
		result = []
		if self.upperSurface or self.middleSurface or self.lowerSurface:
			result.append('<side index="%s">' % (index, ))
			if self.upperSurface:
				result.append(self.upperSurface.xmlReference(location = 'upperSurface'))
			if self.middleSurface:
				result.append(self.middleSurface.xmlReference(location = 'middleSurface'))
			if self.lowerSurface:
				result.append(self.lowerSurface.xmlReference(location = 'lowerSurface'))
			result.append('</side>')
		else:
			result.append('<side index="%s"/>' % (index, ))
		return '\n'.join(result)

class ForgerySurface(ForgeryElement):
	light = property(
		fget = lambda self: self.__getitem__('light'),
		fset = lambda self, value: self.__setitem__('light', value),
	)
	texture = property(
		fget = lambda self: self.__getitem__('texture'),
		fset = lambda self, value: self.__setitem__('texture', value),
		fdel = lambda self: self.__setitem__('texture', None),
	)
	textureStyle = None
	dx = None
	dy = None
	effects = None
	actions = None
	size = 128
	scaledDx = property(fget = lambda self: self.dx / float(self.size))
	scaledDy = property(fget = lambda self: self.dy / float(self.size))
	image = property(fget = lambda self: self.generateImage())
	imageSize = size
	
	parentCategories = {
		'light':   'lights',
		'texture': 'textures',
	}
	xmlClass = u'surface'
	category = 'surfaces'
	
	def __init__(self, elementID, light, texture = '', textureStyle = None, dx = 0, dy = 0, effects = None, actions = None):
		super(ForgerySurface, self).__init__(elementID)
		self.light = light
		self.texture = texture or ''
		self.textureStyle = textureStyle
		self.dx = dx
		self.dy = dy
		self.effects = dict(effects or ())
		self.actions = dict(actions or ())
	
	def getParams(self):
		result = []
		result.append(repr(self.elementID))
		if self.light:
			result.append('self.lights[%r]' % (self.light.elementID, ))
		else:
			result.append(repr(self.light))
		if self.texture:
			result.append('self.textures[%r]' % (self.texture.elementID, ))
		else:
			result.append(repr(self.texture))
		result.append(repr(self.textureStyle))
		result.append(repr(self.dx))
		result.append(repr(self.dy))
		result.append(repr(self.effects))
		result.append(repr(self.actions))
		return '(' + ', '.join(result) + ')'
	
	def getChildren(self, data):
		result = []
		return tuple(result)
	
	def drawSelf(self):
		pass
	
	def toXML(self):
		result = []
		tag = '<%s id="%s"' % (self.xmlClass, self.elementID)
		if self.textureStyle:
			tag += ' textureStyle="%s"' % (self.textureStyle, )
		if self.dx or self.dy:
			tag += ' dx="%s" dy="%s"' % (self.dx, self.dy)
		if self.light or self.texture or self.effects or self.actions:
			tag += '>'
		else:
			tag += '/>'
		result.append(tag)
		if self.light:
			if isinstance(self.light, (str, unicode)):
				result.append('<light id="%s"/>' % (self.light))
			else:
				result.append(self.light.xmlReference())
		if self.texture:
			result.append(self.texture.xmlReference())
		for effect, data in self.effects.iteritems():
			tag = '<effect kind="%s"' % (effect, )
			for key, value in data.iteritems():
				tag += ' %s="%s"' % (key, value)
			tag += '/>'
			result.append(tag)
		for kind in self.actions.itervalues():
			for action in kind.itervalues():
				result.append(action.toXML())
		if self.light or self.texture or self.effects or self.actions:
			result.append('</%s>' % (self.xmlClass, ))
		return '\n'.join(result)
	
	def texturesUpdated(self, data):
		self.texture = data.textures[self.texture.elementID]
	
	def generateImage(self):
		size = self.imageSize
		dx, dy = self.dx, self.dy
		image = self.texture.image
		if usePyObjC:
			from AppKit import NSBitmapImageRep, NSCalibratedRGBColorSpace, NSGraphicsContext, NSCompositeCopy, NSImage
			from Foundation import NSRect
			rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
				None,
				int(size), int(size),
				8, 4,
				True,
				False,
				NSCalibratedRGBColorSpace,
				0, 32,
			)
			context = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
			oldContext = NSGraphicsContext.currentContext()
			NSGraphicsContext.setCurrentContext_(context)
			image.drawInRect_fromRect_operation_fraction_(
				NSRect((0, 0), (size, size)),
				NSRect((0, 0), image.size()),
				NSCompositeCopy,
				1.0,
			)
			NSGraphicsContext.setCurrentContext_(oldContext)
			image = NSImage.alloc().initWithSize_((size, size))
			image.addRepresentation_(rep)
			rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
				None,
				int(size), int(size),
				8, 4,
				True,
				False,
				NSCalibratedRGBColorSpace,
				0, 32,
			)
			context = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
			oldContext = NSGraphicsContext.currentContext()
			NSGraphicsContext.setCurrentContext_(context)
			srcPoints = (
				(0, 0),
				(size - dx, 0),
				(0, size - dy),
				(size - dx, size - dy),
			)
			dstPoints = (
				(dx, dy),
				(0, dy),
				(dx, 0),
				(0, 0),
			)
			sizes = (
				(size - dx, size - dy),
				(dx, size - dy),
				(size - dx, dy),
				(dx, dy),
			)
			for src, dst, siz in zip(srcPoints, dstPoints, sizes):
				if siz[0] > 0 and siz[1] > 0: # not sure if Cocoa appreciates trying to draw an image with invalid bounds
					image.drawInRect_fromRect_operation_fraction_(
						NSRect(dst, siz),
						NSRect(src, siz),
						NSCompositeCopy,
						1.0,
					)
			NSGraphicsContext.setCurrentContext_(oldContext)
			result = NSImage.alloc().initWithSize_((size, size))
			result.addRepresentation_(rep)
		else:
			import wx
			try:
				image = image.Scale(size, size, wx.IMAGE_QUALITY_HIGH)
			except AttributeError: # wx 2.6 can't do IMAGE_QUALITY_HIGH
				image = image.Scale(size, size)
			result = wx.BitmapFromImage(image)
		return result

class ForgeryTexture(ForgeryElement):
	filename = None
	collectionID = None
	bitmapID = None
	clutID = None
	thumbnailSize = 32
	_thumbnail = None
	_image = None
	thumbnail = property(fget = lambda self: self.generateThumbnail())
	image = property(fget = lambda self: self.generateImage())
	isBlank = property(fget = lambda self: (self.filename, self.collectionID, self.bitmapID, self.clutID) == (None, None, None))
	if usePyObjC:
		size = property(fget = lambda self: (self.image.size().width, self.image.size().height))
	else:
		size = property(fget = lambda self: (self.image.GetWidth(), self.image.GetHeight()))
	
	parentCategories = {
	}
	xmlClass = u'texture'
	category = 'textures'
	
	def __init__(self, elementID, filename = None, collectionID = None, bitmapID = None, clutID = None, width = None, height = None, pixels = None):
		super(ForgeryTexture, self).__init__(elementID)
		self.filename = filename
		self.collectionID = collectionID
		self.bitmapID = bitmapID
		self.clutID = clutID
		if self.collectionID is not None and self.bitmapID is not None and self.clutID is not None and width is not None and height is not None and pixels is not None:
			self.setFromPixels(width, height, pixels)
	
	def setFromPixels(self, width, height, pixels):
		if usePyObjC:
			from AppKit import NSImage, NSBitmapImageRep, NSCalibratedRGBColorSpace
			self._image = NSImage.alloc().initWithSize_((width, height))
			pixels = [(int(r * a / 255), int(g * a / 255), int(b * a / 255), a) for r, g, b, a in pixels]
			pixels = ''.join([chr(r) + chr(g) + chr(b) + chr(a) for r, g, b, a in pixels])
			rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
				(pixels, None, None, None, None),
				width, height,
				8, 4,
				True,
				False,
				NSCalibratedRGBColorSpace,
				width * 4, 32,
			)
			self._image.addRepresentation_(rep)
			self.__pixels = pixels # it seems that NSImageRep does not copy the pixel data, so we must retain it here
		else:
			import wx
			self._image = wx.EmptyImage(width, height)
			data = []
			for y in xrange(height):
				for x in xrange(width):
					pixel = pixels[x + width * y]
					self._image.SetRGB(x, y, pixel[0], pixel[1], pixel[2])
					if self._image.HasAlpha():
						self._image.SetAlpha(x, y, pixel[3])
	
	def getParams(self):
		result = []
		result.append(repr(self.elementID))
		if self.filename:
			result.append('filename = %r' % (self.filename, ))
		if self.collectionID is not None:
			result.append('collection = %r' % (self.collectionID, ))
		if self.bitmapID is not None:
			result.append('index = %r' % (self.bitmapID, ))
		if self.clutID is not None:
			result.append('index = %r' % (self.clutID, ))
		return '(' + ', '.join(result) + ')'
	
	def getChildren(self, data):
		result = []
		return tuple(result)
	
	def drawSelf(self):
		pass
	
	def toXML(self):
		result = []
		if self.filename:
			result.append('<%s id="%s" filename="%s"/>' % (self.xmlClass, self.elementID, self.filename))
		elif self.collectionID is not None and self.bitmapID is not None and self.clutID is not None:
			result.append('<%s id="%s" collectionID="%s" bitmapID="%s" clutID="%s"/>' % (self.xmlClass, self.elementID, self.collectionID, self.bitmapID, self.clutID))
		else:
			result.append('<%s id="%s"/>' % (self.xmlClass, self.elementID))
		return '\n'.join(result)
	
	def generateThumbnail(self):
		if not self._thumbnail:
			if usePyObjC:
				from AppKit import NSBitmapImageRep, NSCalibratedRGBColorSpace, NSGraphicsContext, NSCompositeCopy, NSImage
				from Foundation import NSRect
				image = self.image
				rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
					None,
					int(self.thumbnailSize), int(self.thumbnailSize),
					8, 4,
					True,
					False,
					NSCalibratedRGBColorSpace,
					0, 32,
				)
				context = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
				oldContext = NSGraphicsContext.currentContext()
				NSGraphicsContext.setCurrentContext_(context)
				image.drawInRect_fromRect_operation_fraction_(
					NSRect((0, 0), (self.thumbnailSize, self.thumbnailSize)),
					NSRect((0, 0), image.size()),
					NSCompositeCopy,
					1.0,
				)
				NSGraphicsContext.setCurrentContext_(oldContext)
				self._thumbnail = NSImage.alloc().initWithSize_((self.thumbnailSize, self.thumbnailSize))
				self._thumbnail.addRepresentation_(rep)
			else:
				import wx
				try:
					image = self.image.Scale(self.thumbnailSize, self.thumbnailSize, wx.IMAGE_QUALITY_HIGH)
				except AttributeError: # wx 2.6 can't do IMAGE_QUALITY_HIGH
					image = self.image.Scale(self.thumbnailSize, self.thumbnailSize)
				self._thumbnail = wx.BitmapFromImage(image)
		return self._thumbnail
	
	def toRGBA(self):
		if usePyObjC:
			from AppKit import NSBitmapImageRep, NSDeviceRGBColorSpace, NSGraphicsContext, NSCompositeCopy
			from Foundation import NSRect
			image = self.image
			size = image.size()
			rep = NSBitmapImageRep.alloc().initWithBitmapDataPlanes_pixelsWide_pixelsHigh_bitsPerSample_samplesPerPixel_hasAlpha_isPlanar_colorSpaceName_bytesPerRow_bitsPerPixel_(
				None,
				int(size.width), int(size.height),
				8, 4,
				True,
				False,
				NSDeviceRGBColorSpace,
				0, 32,
			)
			context = NSGraphicsContext.graphicsContextWithBitmapImageRep_(rep)
			oldContext = NSGraphicsContext.currentContext()
			NSGraphicsContext.setCurrentContext_(context)
			oldFlipped = image.isFlipped()
			image.setFlipped_(True)
			image.drawInRect_fromRect_operation_fraction_(
				NSRect((0, 0), size),
				NSRect((0, 0), size),
				NSCompositeCopy,
				1.0,
			)
			image.setFlipped_(oldFlipped)
			NSGraphicsContext.setCurrentContext_(oldContext)
			# FIXME: take bytesPerRow into account
			data = str(rep.bitmapData())
		else:
			image = self.image.Mirror(horizontally = False) # wxImage coordinates are flipped vertically
			data = image.GetData()
			data = list(data)
			rdata = data[0::3]
			gdata = data[1::3]
			bdata = data[2::3]
			if image.HasAlpha():
				adata = image.GetAlpha()
			else:
				adata = '\xFF' * len(rdata)
			data = ''.join([r + g + b + a for r, g, b, a in zip(rdata, gdata, bdata, adata)])
		return data
	
	def generateImage(self):
		if not self._image:
			if self.filename:
				if usePyObjC:
					from AppKit import NSImage
					self._image = NSImage.alloc().initWithContentsOfFile_(self.filename)
				else:
					import wx
					self._image = wx.NullImage
					self._image.LoadFile(self.filename, wx.BITMAP_TYPE_ANY)
			elif self.collectionID is not None and self.bitmapID is not None and self.clutID is not None:
				# We should never get here; the pixel data is loaded
				# when the texture is created.
				self._image = None
			else: # null image
				size = 32
				pixels = []
				for y in xrange(size):
					for x in xrange(size):
						# colors
						#color = (x * 255 / size, y * 255 / size, 0xFF - (x + y) * 255 / (2 * size), 0xFF)
						
						# diagonal lines
						if y % 8 == x % 8:
							color = (0xFF, 0x00, 0x00, 0xFF)
						else:
							color = (0xFF, 0xFF, 0xFF, 0x7F)
						
						# X
						#if y == x or y == size - x:
						#	color = (0xFF, 0x00, 0x00, 0xFF)
						#else:
						#	color = (0xFF, 0xFF, 0xFF, 0xFF)
						
						if usePyObjC:
							color = (
								int(color[0] * color[3] / 0xFF),
								int(color[1] * color[3] / 0xFF),
								int(color[2] * color[3] / 0xFF),
								color[3],
							)
						
						pixels.append(color)
				
				self.setFromPixels(size, size, pixels)
		return self._image

class ForgeryVertex(ForgeryMoveableElement):
	parentCategories = {}
	x = None
	y = None
	xmlClass = u'vertex'
	category = 'vertices'
	
	def __init__(self, elementID, x, y):
		super(ForgeryVertex, self).__init__(elementID = elementID)
		self.x = x
		self.y = y
	
	def __iter__(self):
		yield self.x
		yield self.y
	
	def __str__(self):
		return "<%s id %r: %s>" % (self.__class__.__name__, self.elementID, (self.x, self.y))
	
	def getParams(self):
		return '(%r, %r, %r)' % (self.elementID, self.x, self.y)
	
	def getChildren(self, data):
		result = []
		for l in data.lines.itervalues():
			if l.vertex0 is self or l.vertex1 is self:
				result.append(l)
		return tuple(result)
	
	def drawSelf(self):
		glVertex2f(self.x, self.y)
	
	def toXML(self):
		result = []
		result.append('<%s id="%s" x="%r" y="%r"/>' % (self.xmlClass, self.elementID, self.x, self.y))
		return '\n'.join(result)
	
	def move(self, dx, dy):
		self.x += dx
		self.y += dy
	
	def getAllVertexAncestors(self):
		return set([self])

def uniqueID(pattern, names):
	names = list(names)
	number = 0
	while pattern % number in names:
		number += 1
	return pattern % number
