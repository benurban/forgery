# ForgeryXMLParser.py
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

__all__ = (
	'ForgeryXMLParser',
	'parse',
)

import ForgeryElements

import xml.sax, xml.sax.handler

class ForgeryXMLParser(xml.sax.handler.ContentHandler):
	data = None
	elementStack = None
	
	def __init__(self, data):
		xml.sax.handler.ContentHandler.__init__(self)
		#super(ForgeryXMLParser, self).__init__()
		self.data = data
	
	def startDocument(self):
		self.elementStack = []
		self.maps = {}
	
	def startElement(self, name, attrs):
		try:
			method = getattr(self, 'start' + capitalize(name) + 'Element')
		except AttributeError:
			pass
		else:
			method(attrs)
	
	def endElement(self, name):
		try:
			method = getattr(self, 'end' + capitalize(name) + 'Element')
		except AttributeError:
			pass
		else:
			method()
	
	def startActionElement(self, attrs):
		info = dict(attrs)
		info['tag'] = 'action'
		self.elementStack.append(info)
	
	def endActionElement(self):
		info = self.elementStack.pop()
		parent = self.elementStack[-1]
		if info['tag'] != 'action':
			raise ValueError, "Expected </%s> here" % info['tag']
		if parent['tag'] == 'surface':
			parent['actions'][info['kind']] = dict(info)
			del parent['actions'][info['kind']]['tag']
			del parent['actions'][info['kind']]['kind']
		else:
			raise ValueError, "<action> tags can only be children of <surface> tags"
	
	def startEffectElement(self, attrs):
		info = dict(attrs)
		info['tag'] = 'effect'
		self.elementStack.append(info)
	
	def endEffectElement(self):
		info = self.elementStack.pop()
		parent = self.elementStack[-1]
		if info['tag'] != 'effect':
			raise ValueError, "Expected </%s> here" % info['tag']
		if parent['tag'] == 'surface':
			parent['effects'][info['kind']] = dict(info)
			del parent['effects'][info['kind']]['tag']
			del parent['effects'][info['kind']]['kind']
		else:
			raise ValueError, "<effect> tags can only be children of <surface> tags"
	
	def startLayerElement(self, attrs):
		info = dict(attrs)
		info['tag'] = 'layer'
		self.elementStack.append(info)
	
	def endLayerElement(self):
		info = self.elementStack.pop()
		parent = self.elementStack[-1]
		if info['tag'] != 'layer':
			raise ValueError, "Expected </%s> here" % info['tag']
		if parent['tag'] == 'map':
			self.data.addElement(ForgeryElements.ForgeryLayer(
				elementID = info['id'],
				offset = float(info.get('offset', 0)),
			))
		else:
			raise ValueError, "<layer> tags can only be children of <map> tags"
	
	def startLineElement(self, attrs):
		info = dict(attrs)
		info['tag'] = 'line'
		info['vertices'] = []
		info['sides'] = [None, None]
		self.elementStack.append(info)
	
	def endLineElement(self):
		info = self.elementStack.pop()
		parent = self.elementStack[-1]
		if info['tag'] != 'line':
			raise ValueError, "Expected </%s> here" % info['tag']
		if parent['tag'] == 'map':
			if len(info['vertices']) == 2:
				vertex0, vertex1 = info['vertices']
				side0, side1 = info['sides']
				self.data.addElement(ForgeryElements.ForgeryLine(
					elementID = info['id'],
					vertex0 = vertex0,
					vertex1 = vertex1,
					side0 = side0,
					side1 = side1,
				))
			else:
				raise ValueError, "A line must have exactly two vertices"
		elif parent['tag'] == 'polygon':
			if info['vertices'] or info['sides'] != [None, None]:
				raise ValueError, "A line reference must not have any children or attributes other than id"
			else:
				parent['lines'].append(info['id'])
		else:
			raise ValueError, "<line> tags can only be children of <map> and <polygon> tags"

	def startMapElement(self, attrs):
		self.data.lights['light 020'] = None
		self.data.addElement(ForgeryElements.ForgeryLayer(elementID = 'layer 000'))
		info = dict(attrs)
		info['tag'] = 'map'
		self.elementStack.append(info)
	
	def endMapElement(self):
		info = self.elementStack.pop()
		parent = self.elementStack[-1]
		if info['tag'] != 'map':
			raise ValueError, "Expected </%s> here" % info['tag']
		if parent['tag'] == 'mapPack':
			del info['tag']
			self.data.mapinfo = info
			for element in self.data.lines.values() + self.data.polygons.values() + self.data.vertices.values() + self.data.surfaces.values():
				element.findParents(self.data)
		else:
			raise ValueError, "<map> tags must be children of the <mapPack> tag"
	
	def startMapPackElement(self, attrs):
		if self.elementStack:
			raise ValueError, "Only one <mapPack> tag is allowed per file"
		info = dict(attrs)
		info['tag'] = 'mapPack'
		self.elementStack = [info]
		try:
			self.version = info['version']
		except KeyError:
			raise ValueError, "The <mapPack> tag requires a version attribute"
	
	def endMapPackElement(self):
		info = self.elementStack.pop()
		if info['tag'] != 'mapPack':
			raise ValueError, "Expected </%s> here" % info['tag']
		self.elementStack = None
	
	def startPolygonElement(self, attrs):
		info = dict(attrs)
		info['tag'] = 'polygon'
		info['lines'] = []
		info['surfaces'] = {}
		self.elementStack.append(info)
	
	def endPolygonElement(self):
		info = self.elementStack.pop()
		parent = self.elementStack[-1]
		if info['tag'] != 'polygon':
			raise ValueError, "Expected </%s> here" % info['tag']
		if parent['tag'] == 'map':
			if len(info['lines']) >= 3:
				self.data.addElement(ForgeryElements.ForgeryPolygon(
					elementID = info['id'],
					layer = info.get('layer', 'layer 000'),
					lines = info['lines'],
					floorOffset = float(info.get('floorOffset', '0')),
					floor = info['surfaces'].get('floor', None),
					ceilingOffset = float(info.get('ceilingOffset', '1')),
					ceiling = info['surfaces'].get('ceiling', None),
				))
			else:
				raise ValueError, "A polygon must have at least 3 lines"
		else:
			raise ValueError, "<polygon> tags can only be children of <map> tags"
	
	def startSideElement(self, attrs):
		info = dict(attrs)
		info['tag'] = 'side'
		info['surfaces'] = {}
		self.elementStack.append(info)
	
	def endSideElement(self):
		info = self.elementStack.pop()
		parent = self.elementStack[-1]
		if info['tag'] != 'side':
			raise ValueError, "Expected </%s> here" % info['tag']
		if parent['tag'] == 'line':
			if 'index' not in info or info['index'] not in ('0', '1'):
				raise ValueError, "A side must have an index of 0 or 1"
			parent['sides'][int(info['index'])] = ForgeryElements.ForgerySide(
				upperSurface = info['surfaces'].get('upperSurface', None),
				middleSurface = info['surfaces'].get('middleSurface', None),
				lowerSurface = info['surfaces'].get('lowerSurface', None),
			)
		else:
			raise ValueError, "<side> tags can only be children of <line> tags"
	
	def startSurfaceElement(self, attrs):
		info = dict(attrs)
		info['tag'] = 'surface'
		info['light'] = None
		info['texture'] = None
		info['textureStyle'] = attrs.get('textureStyle', None)
		info['dx'] = int(attrs.get('dx', 0))
		info['dy'] = int(attrs.get('dy', 0))
		info['location'] = attrs.get('location', None)
		info['effects'] = {}
		info['actions'] = {}
		self.elementStack.append(info)
	
	def endSurfaceElement(self):
		info = self.elementStack.pop()
		parent = self.elementStack[-1]
		if info['tag'] != 'surface':
			raise ValueError, "Expected </%s> here" % info['tag']
		if parent['tag'] == 'map':
			if info['location']:
				raise ValueError, "A surface definition must not specify a location"
			self.data.addElement(ForgeryElements.ForgerySurface(
				elementID = info['id'],
				light = info['light'] or 'light 020',
				texture = info['texture'],
				textureStyle = info['textureStyle'],
				dx = info['dx'],
				dy = info['dy'],
				effects = info['effects'],
				actions = info['actions'],
			))
		elif parent['tag'] in ('side', 'polygon'):
			if info['light'] or info['texture'] or info['textureStyle'] or info['dx'] or info['dy']:
				raise ValueError, "A surface reference must not have any children or attributes other than id and location"
			if not info['location']:
				raise ValueError, "A surface reference must specify a location"
			parent['surfaces'][info['location']] = info['id']
		else:
			raise ValueError, "<surface> tags can only be children of <map>, <side>, and <polygon> tags"
	
	def startTextureElement(self, attrs):
		info = dict(attrs)
		info['tag'] = 'texture'
		self.elementStack.append(info)
	
	def endTextureElement(self):
		info = self.elementStack.pop()
		parent = self.elementStack[-1]
		if info['tag'] != 'texture':
			raise ValueError, "Expected </%s> here" % info['tag']
		if parent['tag'] == 'map':
			if 'filename' in info:
				if 'collection' in info or 'index' in info:
					raise ValueError, "A texture definition may specify a filename, or a collection and index, or neither, but not both"
				else:
					self.data.addElement(ForgeryElements.ForgeryTexture(
						elementID = info['id'],
						filename = info['filename'],
					))
			elif 'collection' in info and 'index' in info:
				self.data.addElement(ForgeryElements.ForgeryTexture(
					elementID = info['id'],
					collection = long(info['collection']),
					index = long(info['index']),
				))
			elif 'collection' not in info and 'index' not in info:
				self.data.addElement(ForgeryElements.ForgeryTexture(
					elementID = info['id'],
				))
			else:
				raise ValueError, "A texture definition may not specify a collection without an index or an index without a collection"
		elif parent['tag'] == 'surface':
			if set(info.keys()) == set(['tag', 'id']):
				parent['texture'] = info['id']
			else:
				raise ValueError, "A texture reference must not have any attributes other than id"
		else:
			raise ValueError, "<texture> tags can only be children of <map> and <surface> tags"
	
	def startVertexElement(self, attrs):
		info = dict(attrs)
		info['tag'] = 'vertex'
		self.elementStack.append(info)
	
	def endVertexElement(self):
		info = self.elementStack.pop()
		parent = self.elementStack[-1]
		if info['tag'] != 'vertex':
			raise ValueError, "Expected </%s> here" % info['tag']
		if parent['tag'] == 'map':
			self.data.addElement(ForgeryElements.ForgeryVertex(
				elementID = info['id'],
				x = float(info['x']),
				y = float(info['y']),
			))
		elif parent['tag'] == 'line':
			if len(parent['vertices']) > 1:
				raise ValueError, "A line can only have two vertices"
			elif set(info.keys()) == set(['tag', 'id']):
				parent['vertices'].append(info['id'])
			else:
				raise ValueError, "A vertex reference must not have any attributes other than id"
		else:
			raise ValueError, "<vertex> tags can only be children of <map> and <line> tags"

def parse(f, data):
	xml.sax.parse(f, ForgeryXMLParser(data))
	return data
