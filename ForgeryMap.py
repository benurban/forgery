#!/usr/bin/env python

# ForgeryMap.py
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
	'ForgeryMap',
)

import ForgeryApplication, ForgeryElements, ForgeryUndoManager, ForgeryXMLParser

if usePyObjC:
	from Foundation import *
	import objc

import os

from tracer import traced

class ForgeryMap(NSObject if usePyObjC else object):
	annotations = None
	layers      = None
	lights      = None
	lines       = None
	mapinfo     = None
	objects     = None
	polygons    = None
	preferences = None
	surfaces    = None
	textures    = None
	vertices    = None
	layer = 'layer 000'
	
	@property
	def currentLayer(self):
		return self.layers[self.layer]
	
	undoManager = objc.ivar('undoManager') if usePyObjC else None
	
	if usePyObjC:
		@traced
		def init(self):
			self = super(ForgeryMap, self).init()
			if self:
				self.undoManager = ForgeryUndoManager.ForgeryUndoManager.alloc().init()
				self.flush()
			return self
	else:
		def __init__(self):
			super(ForgeryMap, self).__init__()
			self.undoManager = ForgeryUndoManager.ForgeryUndoManager(self)
			self.flush()
	
	@traced
	def flush(self):
		self.annotations = {}
		self.layers      = {
			'layer 000': ForgeryElements.ForgeryLayer(elementID = 'layer 000'),
		}
		self.lights      = {
			'light 020': None,
		}
		self.lines       = {}
		self.mapinfo     = {}
		self.objects     = {}
		self.polygons    = {}
		self.preferences = {}
		self.surfaces    = {}
		self.textures    = {
			'': ForgeryElements.ForgeryTexture(elementID = ''),
		}
		self.vertices    = {}
		self.layer = 'layer 000'
		if self.undoManager:
			self.undoManager.flush()
	
	def __getitem__(self, key):
		return getattr(self, key)
	
	@traced
	def readFromXMLFile(self, f):
		self.flush()
		if f:
			self.undoManager.openUndoGroup()
			ForgeryXMLParser.parse(f, self)
			self.undoManager.closeUndoGroup()
			self.undoManager.flush()
	
	@traced
	def writeToXMLFile(self, f):
		print >> f, self.toXML()
	
	@traced
	def toXML(self):
		return self.elementsToXML(
			self.annotations.values() +
			self.layers.values() +
			self.lights.values() +
			self.lines.values() +
			self.objects.values() +
			self.polygons.values() +
			self.surfaces.values() +
			self.textures.values() +
			self.vertices.values()
		)
	
	@traced
	def elementsToXML(self, elements):
		elements = [element for element in elements if element]
		elements.sort(cmp = lambda lhs, rhs: cmp(lhs.elementID, rhs.elementID))
		layers = [(element.elementID, element) for element in elements if isinstance(element, ForgeryElements.ForgeryLayer)]
		lines = [(element.elementID, element) for element in elements if isinstance(element, ForgeryElements.ForgeryLine)]
		polygons = [(element.elementID, element) for element in elements if isinstance(element, ForgeryElements.ForgeryPolygon)]
		surfaces = [(element.elementID, element) for element in elements if isinstance(element, ForgeryElements.ForgerySurface)]
		textures = [(element.elementID, element) for element in elements if isinstance(element, ForgeryElements.ForgeryTexture)]
		vertices = [(element.elementID, element) for element in elements if isinstance(element, ForgeryElements.ForgeryVertex)]
		result = []
		result.append('<mapPack version="1">')
		result.append('<map name="%s" displayName="%s">' % (
			self.mapinfo.get('name', self.mapinfo.get('displayName', u"untitled map")),
			self.mapinfo.get('displayName', self.mapinfo.get('name', u"untitled map")),
		))
		for key, value in vertices + lines + polygons + layers + surfaces + textures:
			result.extend(value.toXML().split('\n'))
		result.append('</map>')
		result.append('</mapPack>')
		i = 0
		for index, line in enumerate(result):
			if line.startswith('</'):
				i -= 1
				result[index] = ('\t' * i) + line
			elif line.endswith('>') and not line.endswith('/>'):
				result[index] = ('\t' * i) + line
				i += 1
			else:
				result[index] = ('\t' * i) + line
		return '\n'.join(result)
	
	def getChildren(self, element):
		return element.getChildren(self)
	
	def linesWithVertex(self, vertex):
		for line in self.lines.itervalues():
			if line.vertex0 == vertex or line.vertex1 == vertex:
				yield line
	
	def polygonForSide(self, line, sideIndex):
		polygons = [child for child in self.getChildren(line) if isinstance(child, ForgeryElements.ForgeryPolygon)]
		for polygon in polygons:
			polygon.findSides()
			if sideIndex == polygon.sides[list(polygon).index(line)]:
				return polygon
	
	def undoableAction(self, undofunc, params):
		return self.undoManager.undoableAction(undofunc, params)
	
	def addElement(self, element):
		if element.elementID in self[element.category]:
			self.undoableAction(self.addElement, (element, ))
		else:
			self.undoableAction(self.delElement, (element, ))
		kind = element.__class__.__name__.split('Forgery', 1)[1]
		return getattr(self, 'add' + kind)(element)
	
	def delElement(self, element):
		self.undoableAction(self.addElement, (element, ))
		kind = element.__class__.__name__.split('Forgery', 1)[1]
		return getattr(self, 'del' + kind)(element)
	
	def addLayer(self, layer):
		self.layers[layer.elementID] = layer
	
	def delLayer(self, layer):
		for element in self.getChildren(layer):
			self.delElement(element)
		del self.layers[layer.elementID]
	
	def addLine(self, line):
		self.lines[line.elementID] = line
	
	def delLine(self, line):
		for element in self.getChildren(line):
			self.delElement(element)
		del self.lines[line.elementID]
	
	def addPolygon(self, polygon):
		self.polygons[polygon.elementID] = polygon
		try:
			polygon.findSides()
		except AttributeError: # this happens while the map is being loaded
			pass
		else:
			for line, index in zip(polygon, polygon.sides):
				self.setLineSide(line, index, ForgeryElements.ForgerySide())
			if not polygon.ceiling:
				polygon.ceiling = ForgeryElements.ForgerySurface(
					elementID = ForgeryElements.uniqueID('ceiling %03d', self.surfaces.keys()),
					texture = self.textures[''],
					light = self.lights['light 020'],
				)
				self.addSurface(polygon.ceiling)
			if not polygon.floor:
				polygon.floor = ForgeryElements.ForgerySurface(
					elementID = ForgeryElements.uniqueID('floor %03d', self.surfaces.keys()),
					texture = self.textures[''],
					light = self.lights['light 020'],
				)
				self.addSurface(polygon.floor)
	
	def delPolygon(self, polygon):
		polygon.findSides()
		for line, index in zip(polygon, polygon.sides):
			self.delLineSide(line, index)
		del self.polygons[polygon.elementID]
	
	def addSurface(self, surface):
		self.surfaces[surface.elementID] = surface
	
	def delSurface(self, surface):
		for element in self.getChildren(surface):
			self.delElement(element)
		for line in self.lines.itervalues():
			if line.side0:
				if line.side0.upperSurface is surface:
					self.delLineSurface(line, 0, 'upper')
				if line.side0.middleSurface is surface:
					self.delLineSurface(line, 0, 'middle')
				if line.side0.lowerSurface is surface:
					self.delLineSurface(line, 0, 'lower')
			if line.side1:
				if line.side1.upperSurface is surface:
					self.delLineSurface(line, 1, 'upper')
				if line.side1.middleSurface is surface:
					self.delLineSurface(line, 1, 'middle')
				if line.side1.lowerSurface is surface:
					self.delLineSurface(line, 1, 'lower')
		for polygon in self.polygons.itervalues():
			if polygon.floor is surface:
				self.delPolygonSurface(polygon, 'floor')
			if polygon.ceiling is surface:
				self.delPolygonSurface(polygon, 'ceiling')
		del self.surfaces[surface.elementID]
	
	def addTexture(self, texture):
		self.textures[texture.elementID] = texture
	
	def delTexture(self, texture):
		if texture.elementID == '':
			raise Exception, u"Can't delete the null texture"
		for element in self.getChildren(texture):
			self.delElement(element)
		for surface in self.surfaces.itervalues():
			if surface.texture is texture:
				self.delSurfaceTexture(surface)
		del self.textures[texture.elementID]
	
	def addVertex(self, vertex):
		self.vertices[vertex.elementID] = vertex
	
	def delVertex(self, vertex):
		for element in self.getChildren(vertex):
			self.delElement(element)
		del self.vertices[vertex.elementID]
	
	def setLayerOffset(self, layer, offset):
		self.undoableAction(self.setLayerOffset, (layer, layer.offset))
		layer.offset = offset
	
	def setLineSide(self, line, index, side):
		if line.sides[index]:
			self.undoableAction(self.setLineSide, (line, index, line.sides[index]))
		elif side: # otherwise the unnecessary deletions keep building up in the undo stacks
			self.undoableAction(self.delLineSide, (line, index))
		if index:
			line.side1 = side
		else:
			line.side0 = side
	
	def delLineSide(self, line, index):
		self.setLineSide(line, index, None)
	
	def delLineSurface(self, line, side, which):
		return self.setLineSurface(line, side, which, None)
	
	def setLineSurface(self, line, side, which, surface):
		if getattr(line.sides[side], which + 'Surface'):
			self.undoableAction(self.setLineSurface, (line, side, which, getattr(line.sides[side], which + 'Surface')))
		elif surface: # otherwise the unnecessary deletions keep building up in the undo stacks
			self.undoableAction(self.delLineSurface, (line, side, which))
		setattr(line.sides[side], which + 'Surface', surface)
	
	def setPolygonCeilingOffset(self, polygon, offset):
		self.setPolygonOffset(polygon, 'ceiling', offset)
	
	def setPolygonFloorOffset(self, polygon, offset):
		self.setPolygonOffset(polygon, 'floor', offset)
	
	def setPolygonLayer(self, polygon, layer):
		self.undoableAction(self.setPolygonLayer, (polygon, polygon.layer))
		polygon.layer = layer
	
	def setPolygonOffset(self, polygon, which, offset):
		self.undoableAction(self.setPolygonOffset, (polygon, which, getattr(polygon, which + 'Offset')))
		setattr(polygon, which + 'Offset', offset)
	
	def delPolygonSurface(self, polygon, which):
		self.setPolygonSurface(polygon, which, None)
	
	def setPolygonSurface(self, polygon, which, surface):
		if getattr(polygon, which):
			self.undoableAction(self.setPolygonSurface, (polygon, which, getattr(polygon, which)))
		elif surface: # otherwise the unnecessary deletions keep building up in the undo stacks
			self.undoableAction(self.delPolygonSurface, (polygon, which))
		setattr(polygon, which, surface)
	
	def delSurfaceTexture(self, surface):
		self.setSurfaceTexture(surface, '')
	
	def setSurfaceTexture(self, surface, texture):
		self.undoableAction(self.setSurfaceTexture, (surface, surface.texture))
		surface.texture = texture
	
	def setSurfaceOffset(self, surface, (dx, dy)):
		self.undoableAction(self.setSurfaceOffset, (surface, (surface.dx, surface.dy)))
		surface.dx = dx
		surface.dy = dy
	
	def addSurfaceAction(self, surface, action):
		if action.kind not in surface.actions:
			self.addSurfaceActionKind(surface, action.kind)
		if action.event in surface.actions[action.kind]:
			self.undoableAction(self.addSurfaceAction, (surface, surface.actions[action.kind][action.event]))
		else:
			self.undoableAction(self.delSurfaceAction, (surface, action))
		surface.actions[action.kind][action.event] = action
	
	def delSurfaceAction(self, surface, action):
		self.undoableAction(self.addSurfaceAction, (surface, action))
		del surface.actions[action.kind][action.event]
	
	def addSurfaceActionKind(self, surface, kind):
		if kind not in surface.actions:
			self.undoableAction(self.delSurfaceActionKind, (surface, kind))
			surface.actions[kind] = {}
	
	def delSurfaceActionKind(self, surface, kind):
		if kind in surface.actions:
			for action in surface.actions[kind].values():
				self.delSurfaceAction(surface, action)
			self.undoableAction(self.addSurfaceActionKind, (surface, kind))
			del surface.actions[kind]
		else:
			print u"Action kind %r not found on surface %r" % (kind, surface)
	
	def addSurfaceEffect(self, surface, effect, properties):
		if effect in surface.effects:
			self.undoableAction(self.addSurfaceEffect, (surface, effect, surface.effects[effect]))
		else:
			self.undoableAction(self.delSurfaceEffect, (surface, effect))
			surface.effects[effect] = properties
	
	def delSurfaceEffect(self, surface, effect):
		if effect in surface.effects:
			self.undoableAction(self.addSurfaceEffect, (surface, effect, surface.effects[effect]))
			del surface.effects[effect]
		else:
			print u"Effect %r not found on surface %r" % (effect, surface)
	
	def changeID(self, element, newID):
		self.undoableAction(self.changeID, (element, element.elementID))
		self[element.category][newID] = element
		del self[element.category][element.elementID]
		element.elementID = newID
	
	def deleteElements(self, elements):
		allElements = [set(elements)]
		while allElements[-1]:
			allElements.append(set())
			for element in allElements[-2]:
				for obj in self.getChildren(element):
					allElements[-1].add(obj)
		for index, childGroup in tuple(enumerate(allElements))[::-1]:
			for obj in childGroup:
				for group in allElements[:index]:
					if obj in group:
						group.remove(obj)
		
		for group in allElements:
			print [element.elementID for element in group]
		for group in allElements[::-1]:
			for element in group:
				self.delElement(element)
	
	def moveVertex(self, vertex, (dx, dy)):
		self.undoableAction(self.moveVertex, (vertex, (-dx, -dy)))
		vertex.move(dx, dy)
	
	def moveElements(self, elements, (dx, dy)):
		vertices = set()
		for element in elements:
			vertices.update(element.getAllVertexAncestors())
		for vertex in vertices:
			self.moveVertex(vertex, (dx, dy))
	
	def fillPolygon(self, (x, y)):
		# This algorithm was blatantly stolen from Pfhorge, and then heavily pythonified and simplified.
		for polygon in self.polygons.itervalues():
			if (x, y) in polygon:
				raise ForgerySpaceOccupiedError(polygon)
		
		intersections = []
		for l in self.lines.itervalues():
			x0, y0 = l.x0, l.y0
			x1, y1 = l.x1, l.y1
			dx, dy = l.dx, l.dy
			if y0 < y < y1 or y1 < y < y0:
				distance = (y0 - y) * dx / dy - (x0 - x)
				if distance > 0:
					intersections.append((distance, l))
		if not intersections:
			raise ForgeryNoPolygonFoundError
		intersections.sort()
		intersections = [l for distance, l in intersections]
		
		firstException = None # keep track of the first exception encountered, in case we want to display it
		
		for line0 in intersections:
			try:
				# If a line was found, follow it around, always choosing
				# the innermost line, to see if it completes a polygon
				
				x0, y0 = line0.x0, line0.y0
				x1, y1 = line0.x1, line0.y1
				
				if y0 > y1 or x0 == x1:
					vertex1 = line0.vertex0
					vertex0 = line0.vertex1
				else: # y0 < y1 and x0 != x1
					vertex1 = line0.vertex1
					vertex0 = line0.vertex0
				
				lines = [line0]
				vertices = [vertex0, vertex1]
				
				while True:
					line1 = None
					vertex2 = None
					thetaMin = None
					
					connectedLines = tuple(self.linesWithVertex(vertex1))
					
					for l in connectedLines:
						if l is line0:
							continue
						
						if l in lines[1:]: # if it's lines[0], we're making sure the polygon is closed
							continue
						
						v = (vertex1 is l.vertex0) and l.vertex1 or l.vertex0
						
						theta = angleBetween(
							(vertex0.x - vertex1.x, vertex0.y - vertex1.y),
							(v.x - vertex1.x, v.y - vertex1.y),
						)
						if theta > 0 and (thetaMin is None or theta < thetaMin):
							line1 = l
							vertex2 = v
							thetaMin = theta
					
					if not line1: # did not find a line that met the requirements
					    raise ForgeryDeadEndError(line0, vertex1)
					
					vertex0, vertex1, vertex2 = vertex1, vertex2, None
					line0, line1 = line1, None
					
					if vertices[0] is vertex0:
						if lines[0] is line0:
							break
						else:
						    raise ForgeryOpenPolygonError(line0)
					else:
						lines.append(line0)
						if vertices[0] is not vertex1:
							vertices.append(vertex1)
				
				for l in lines:
					if not len(l):
						raise ForgeryZeroLengthLineError(l)
					if l.side0 and l.side1:
						raise ForgerySideConflictError(l)
					if not l.isValid(self):
						raise ForgeryInvalidLineError(l)
				result = ForgeryElements.ForgeryPolygon(
					ForgeryElements.uniqueID('polygon %03d', self.polygons.keys()),
					self.currentLayer,
					lines,
				)
				if (x, y) not in result:
					raise ForgeryPointOutsidePolygonError
				else:
					return result
			except ForgeryFillError, e:
				if not firstException:
					firstException = e
		raise firstException
	
	@traced
	def importTextures(self, shpA):
		# FIXME: delete textures from other shapes files
		collectionIDs = [
			('water',     17),
			('lava',      18),
			('sewage',    19),
			('jjaro',     20),
			('pfhor',     21),
			('landscape', 27),
			('landscape', 28),
			('landscape', 29),
			('landscape', 30),
		]
		if usePyObjC:
			loader = ForgeryShapesLoader.alloc().initWithPath_(shpA)
		else:
			loader = ForgeryShapesLoader(shpA)
		import ForgeryProgressWindow
		#progressWindow = ForgeryProgressWindow.ForgeryProgressWindow.alloc().initWithWindowNibName_('ForgeryApplication')
		progressWindow = ForgeryApplication.sharedApplication().progressWindow
		print repr(progressWindow)
		progressWindow.setup(u"Loading Textures", u"Reading %s..." % (os.path.basename(shpA), ))
		progressWindow.setProgressMaximum(len(collectionIDs))
		if usePyObjC:
			self.performSelectorInBackground_withObject_('doImportTextures:', (collectionIDs, loader, progressWindow))
		else:
			import threading
			threading.Thread(target = self.doImportTextures, args = (collectionIDs, loader, progressWindow)).start()
	
	if usePyObjC:
		def doImportTextures_(self, args):
			pool = NSAutoreleasePool.alloc().init()
			self.doImportTextures(*args)
			del self, args
	
	@traced
	def doImportTextures(self, collectionIDs, loader, progressWindow):
		for index, (name, collectionID) in enumerate(collectionIDs):
			progressWindow.updateProgress(index, u"%s collection (ID %s)" % (name.capitalize(), collectionID), u"%s of %s" % (index + 1, len(collectionIDs)))
			tex = sorted(loader.loadAllTextures(collectionID = collectionID).items())
			for (collectionID, bitmapID, clutID), (width, height, pixels) in tex:
				texture = ForgeryElements.ForgeryTexture(
					elementID = 'collection %03d bitmap %03d clut %03d' % (collectionID, bitmapID, clutID),
					collectionID = collectionID,
					bitmapID = bitmapID,
					clutID = clutID,
					width = width,
					height = height,
					pixels = pixels,
				)
				self.addTexture(texture)
				for surface in self.surfaces.itervalues():
					surface.texturesUpdated(self)
				ForgeryApplication.sharedApplication().palette.update()
		progressWindow.cleanUp()

def getUInt8(data):
	return ord(data[0])

def getSInt8(data):
	result = getUInt8(data)
	if result > 127:
		result -= 256
	return result

def getUInt16(data):
	a, b = getUInt8(data[0]), getUInt8(data[1])
	return (a << 8) | (b << 0)
	#msb, lsb = getUInt8(data[0]), getUInt8(data[1])
	#return (msb << 8) | (lsb << 0)

def getSInt16(data):
	result = getUInt16(data)
	if result > 32767:
		result -= 65536
	return result

def getUInt32(data):
	a, b, c, d = getUInt8(data[0]), getUInt8(data[1]), getUInt8(data[2]), getUInt8(data[3])
	return (a << 24) | (b << 16) | (c << 8) | (d << 0)
	#msw, lsw = getUInt16(data[0:2]), getUInt16(data[2:4])
	#return (msw << 16) | (lsw << 0)

def getSInt32(data):
	result = getUInt32(data)
	if result > 2147483647:
		result -= 4294967296
	return result

def readUInt8(f):
	return getUInt8(f.read(1))

def readSInt8(f):
	return getSInt8(f.read(1))

def readUInt16(f):
	return getUInt16(f.read(2))

def readSInt16(f):
	return getSInt16(f.read(2))

def readUInt32(f):
	return getUInt32(f.read(4))

def readSInt32(f):
	return getSInt32(f.read(4))

def readChars(f, n):
	return f.read(n)

def uniformSplit(s, chunkSize):
	s = list(s)
	result = []
	while s:
		result.append(''.join(s[0:chunkSize]))
		del s[0:chunkSize]
	return result

class ForgeryShapesLoader(NSObject if usePyObjC else object):
	path = objc.ivar('path') if usePyObjC else None
	
	if usePyObjC:
		def initWithPath_(self, path):
			self = super(ForgeryShapesLoader, self).init()
			if self:
				self.path = path
			return self
	else:
		def __init__(self, path):
			self.path = path
	
	def loadAllTextures(self, collectionID = None, clutID = 0):
		collections = self.loadCollections(8)
		if collectionID is None:
			for collectionID, collection in enumerate(collections):
				collection = collections[collectionID]
				clut = self.extractCLUT(collection, clutID)
				result = []
				for bitmapID in xrange(getSInt16(collection[26:28])):
					width, height, flags, pixels = self.extractBitmap(collection, bitmapID)
					pixels = list(pixels)
					for i, pixel in enumerate(pixels):
						pixels[i] = (clut[pixel][1] >> 8, clut[pixel][2] >> 8, clut[pixel][3] >> 8, 0xFF)
					result.append(((collectionID, bitmapID, clutID), (width, height, pixels)))
		else:
			collection = collections[collectionID]
			clut = self.extractCLUT(collection, clutID)
			result = []
			for bitmapID in xrange(getSInt16(collection[26:28])):
				width, height, flags, pixels = self.extractBitmap(collection, bitmapID)
				pixels = list(pixels)
				for i, pixel in enumerate(pixels):
					color = clut[pixel]
					pixels[i] = (color[1] >> 8, color[2] >> 8, color[3] >> 8, 0xFF)
				result.append(((collectionID, bitmapID, clutID), (width, height, pixels)))
		return dict(result)

	def loadCollections(self, depth):
		with open(self.path, 'rb') as f:
			collections = []
			headers = uniformSplit(readChars(f, 1024), 32)
			for header in headers:
				status_flags, offset, length, offset16, length16 = uniformSplit(header[:20], 4)
				status = getSInt16(status_flags[0:2])
				flags = getUInt16(status_flags[2:4])
				offset = getSInt32(offset)
				length = getSInt32(length)
				offset16 = getSInt32(offset16)
				length16 = getSInt32(length16)
				collections.append(self.loadCollection(f, offset, length, offset16, length16, depth))
		return collections

	def loadCollection(self, f, offset, length, offset16, length16, depth):
		if depth != 8 and offset16 != -1 and length16 != -1:
			offset = offset16
			length = length16
		if offset <= 0:
			raise ValueError, offset
		if length <= 0:
			raise ValueError, length
		f.seek(offset)
		result = readChars(f, length)
		version = getSInt16(result[0:2])
		kind = getSInt16(result[2:4])
		if version < 0:
			raise ValueError, version
		if kind < 0:
			raise ValueError, kind
		return result

	def extractCLUT(self, collection, clutID):
		version, kind, flags, colorsPerClut, clutCount = uniformSplit(collection[0:10], 2)
		version = getSInt16(version)
		kind = getSInt16(kind)
		flags = getUInt16(flags)
		colorsPerClut = getSInt16(colorsPerClut)
		clutCount = getSInt16(clutCount)
		if clutID >= clutCount:
			raise IndexError, clutID
		clutOffset = getSInt32(collection[10:14])
		
		cluts = uniformSplit(collection[clutOffset:clutOffset + 8 * colorsPerClut * clutCount], 8 * colorsPerClut)
		clutData = uniformSplit(cluts[clutID], 8)
		result = []
		for colorData in clutData:
			value, red, green, blue = uniformSplit(colorData, 2)
			value = getUInt8(value[1:2])
			red = getUInt16(red)
			green = getUInt16(green)
			blue = getUInt16(blue)
			result.append((value, red, green, blue))
		return result

	def extractBitmap(self, collection, bitmapID):
		#print len(collection), bitmapID
		COLUMN_ORDER_BIT = 0x8000
		TRANSPARENT_BIT = 0x4000
		
		# calculate the pointer to the desired bitmap_definition
		p = collection[26:]
		bitmapCount = getSInt16(p[0:2])
		if bitmapID >= bitmapCount:
			raise IndexError, bitmapID
		bitmapOffsetTableOffset = getSInt32(p[2:6])
		bitmapOffsetTable = collection[bitmapOffsetTableOffset:]
		#print getSInt32(bitmapOffsetTable[4 * bitmapID:])
		p = collection[getSInt32(bitmapOffsetTable[4 * bitmapID:]):]
		
		# parse the bitmap_definition struct
		width = getSInt16(p[0:2])
		height = getSInt16(p[2:4])
		bytesPerRow = getSInt16(p[4:6])
		flags = getUInt16(p[6:8])
		if width < 0:
			raise ValueError, width
		if height < 0:
			raise ValueError, height
		
		# parse/decode pixel data
		p = p[22:]
		p = p[8:] # No clue what this is for, and it will probably cause problems
		if flags & COLUMN_ORDER_BIT: # skip scanline pointers
			p = p[width * 4:]
		else:
			p = p[height * 4:]
		if bytesPerRow != -1: # this is an uncompressed bitmap, so we can copy pixel by pixel
			pixels = []
			if flags & COLUMN_ORDER_BIT: # column-order pixels, transpose the image
				for y in xrange(height):
					for x in xrange(width):
						pixels.append(getUInt8(p[x * bytesPerRow + y]))
			else: # normal, plain, wonderful bitmap: just copy pixel by pixel
				for y in xrange(height):
					for x in xrange(width):
						pixels.append(getUInt8(p[y * bytesPerRow + x]))
		else:
			pixels = [None] * width * height
			# this is an RLE bitmap: for each column, read 2 values (p0 and p1),
			# leave p0 pixels blank, copy (p1 - p0) pixels and repeat for the next column
			for x in xrange(width):
				p0 = readInt16(p[0:2]) # y coord of the first non-transparent pixel
				p1 = readInt16(p[2:4]) # y coord of the last non-transparent pixel
				p = p[4:]
				for i in xrange(p1 - p0): # copy p1 - p0 pixels
					pixels[x + (p0 + i) * width] = getUInt8(p[i])
				p = p[p1 - p0:]
		return (width, height, flags, pixels)

if __name__ == '__main__':
	import Forgery
	Forgery.main()
