# ForgerysceBLoader.py
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
	'ForgerysceBLoader',
	'ForgerysceBMapLoader',
	'loadsceB',
)

import ForgeryElements

import plistlib

class ForgerysceBLoader(object):
	result = None
	version = 1
	
	def __init__(self, result):
		super(ForgerysceBLoader, self).__init__()
		self.result = result
	
	def loadsceB(self, sceB):
		self.version = sceB['version']
		# FIXME: Load more than one map
		# FIXME: Check version
		ForgerysceBMapLoader(self.version, self.result).loadMap(sceB['maps'][0])
		
class ForgerysceBMapLoader(object):
	result = None
	version = 1
	
	def __init__(self, version, result):
		super(ForgerysceBMapLoader, self).__init__()
		self.result = result
		self.version = version
	
	def loadMap(self, plist):
		self.result.lights['light 020'] = None
		self.result.addElement(ForgeryElements.ForgeryLayer(elementID = 'layer 000'))
		self.loadTextures(plist.get('textures', {}))
		self.loadSurfaces(plist.get('surfaces', {}))
		self.loadVertices(plist.get('vertices', {}))
		self.loadLines   (plist.get('lines',    {}))
		self.loadLayers  (plist.get('layers',   {}))
		self.loadPolygons(plist.get('polygons', {}))
	
	def loadTextures(self, data):
		for elementID, t in data.iteritems():
			self.result.addElement(ForgeryElements.ForgeryTexture(
				elementID = elementID,
				collectionID = t['collectionID'],
				bitmapID = t['bitmapID'],
				clutID = t['clutID'],
			))
	
	def loadActions(self, data):
		if data:
			return dict((kind, self.loadAction(action)) for kind, action in data.iteritems())
		else:
			return {}
			actions = {}
			for action in info['actions']:
				if action.kind not in actions:
					actions[action.kind] = {}
				actions[action.kind][action.event] = action
	
	def loadEvents(self, parent, data):
		# FIXME: What types of objects can trigger these events?
		if not isinstance(parent, (ForgeryElements.ForgeryPolygon, ForgeryElements.ForgerySurface, ForgeryElements.ForgeryCreature, ForgeryElements.ForgeryDecor)):
			# This should never happen; the other loaders should not call this function
			raise TypeError, "%s %s does not support events" % (parent.__class__.__name__.split('Forgery', 1)[1], parent.elementID)
		result = {}
		for kind, actions in data.iteritems():
			if isinstance(parent, ForgeryElements.ForgeryPolygon) and kind not in ('enterPolygon', 'standInPolygon', 'floatInPolygon', 'swimInPolygon', 'leavePolygon', 'enterState', 'leaveState'):
				raise ValueError, "Polygon %s does not support event '%s'" % (parent.elementID, kind)
			elif isinstance(parent, ForgeryElements.ForgerySurface) and kind not in ('activateSurface', 'deactivateSurface', 'punchSurface', 'damageSurface', 'enterState', 'leaveState'):
				raise ValueError, "Surface %s does not support event '%s'" % (parent.elementID, kind)
			elif isinstance(parent, ForgeryElements.ForgeryCreature) and kind not in ('spawnCreature', 'awakenCreature', 'damageCreature', 'killCreature', 'enterState', 'leaveState'):
				raise ValueError, "Creature %s does not support event '%s'" % (parent.elementID, kind)
			elif isinstance(parent, ForgeryElements.ForgeryDecor) and kind not in ('spawnDecor', 'damageDecor', 'destroyDecor', 'enterState', 'leaveState'):
				raise ValueError, "Decor %s does not support event '%s'" % (parent.elementID, kind)
			result[kind] = [self.result.actions[elementID] for elementID in actions]
		return result
	
	def loadAction(self, data):
		pass
	
	def startActionElement(self, attrs):
		if info['kind'] == 'switch':
			info['elements'] = []
	
	def endActionElement(self):
		event = info.get('event', 'actionButton')
		if event in ('actionButton', 'walkOnPolygon', 'walkOffPolygon', 'floatOverPolygon', 'floatOffPolygon', 'enterState', 'leaveState'):
			if info['kind'] == 'switch':
				parent['actions'].append(ForgeryElements.ForgerySwitchAction(
					event = info.get('event', 'actionButton'),
					*info['elements']
				))
			elif info['kind'] == 'pattern buffer':
				parent['actions'].append(ForgeryElements.ForgeryPatternBufferAction(
					event = info.get('event', 'actionButton'),
				))
			elif info['kind'] == 'terminal':
				parent['actions'].append(ForgeryElements.ForgeryTerminalAction(
					event = info.get('event', 'actionButton'),
				))
			elif info['kind'] == 'recharger':
				parent['actions'].append(ForgeryElements.ForgeryRechargerAction(
					shieldRate = info.get('shieldRate', 0.0),
					oxygenRate = info.get('oxygenRate', 0.0),
					shieldLimit = info.get('shieldLimit'),
					oxygenLimit = info.get('oxygenLimit'),
					event = info.get('event', 'actionButton'),
				))
			else:
				raise ValueError, "<action> tags must have a kind attribute matching one of: \"switch\", \"pattern buffer\", \"terminal\", or \"recharger\""
		else:
			raise ValueError, "<action> tag event attributes must match one of: \"actionButton\", \"walkOnPolygon\", \"walkOffPolygon\", \"floatOverPolygon\", \"floatOffPolygon\", \"enterState\", or \"leaveState\""
	
	def loadSurfaces(self, data):
		for elementID, s in data.iteritems():
			self.result.addElement(ForgeryElements.ForgerySurface(
				elementID = elementID,
				light = s.get('light', 'light 020'),
				texture = s.get('texture', ''),
				textureStyle = s.get('textureStyle'),
				dx = s.get('dx', 0),
				dy = s.get('dy', 0),
				effects = s.get('effects', {}),
				actions = loadActions(s['actions']),
			))
	
	def endSurfaceElement(self):
		if parent['tag'] == 'map':
		elif parent['tag'] == 'action':
			if parent['kind'] == 'switch':
				if set(info) == set(('actions', 'dx', 'dy', 'effects', 'id', 'light', 'location', 'state', 'tag', 'texture', 'textureStyle')) and not info['actions'] and not info['dx'] and not info['dy'] and not info['effects'] and not info['light'] and not info['location'] and not info['texture'] and not info['textureStyle']:
					parent['elements'].append((info['id'], info['state']))
				else:
					raise ValueError, "State change tags must not have any children or attributes other than id and state"
			else:
				raise ValueError, "<surface> tags cannot be children of non-switch <action> tags"
	
	def loadVertices(self, data):
		for elementID, v in data.iteritems():
			self.result.addElement(ForgeryElements.ForgeryVertex(
				elementID = elementID,
				x = v['x'],
				y = v['y'],
			))
	
	def loadLines(self, data):
		for elementID, l in data.iteritems():
			self.result.addElement(ForgeryElements.ForgeryLine(
				elementID = elementID,
				vertex0 = self.result.vertices[l['vertices'][0]],
				vertex1 = self.result.vertices[l['vertices'][1]],
				side0 = self.loadSide(l.get('sides', (False, False))[0]),
				side1 = self.loadSide(l.get('sides', (False, False))[1]),
			))
	
	def loadSide(self, data):
		if isinstance(data, dict):
			return ForgeryElements.ForgerySide(
				upperSurface = (self.result.surfaces[data['upperSurface']] if 'upperSurface' in data else None),
				middleSurface = (self.result.surfaces[data['middleSurface']] if 'middleSurface' in data else None),
				lowerSurface = (self.result.surfaces[data['lowerSurface']] if 'lowerSurface' in data else None),
			)
		else:
			return None
	
	def loadLayers(self, data):
		for elementID, l in data.iteritems():
			self.result.addElement(ForgeryElements.ForgeryLayer(
				elementID = elementID,
				offset = l.get('offset', 0.0),
			))
	
	def startPolygonElement(self, attrs):
		info['lines'] = []
		info['surfaces'] = {}
	
	def endPolygonElement(self):
		if parent['tag'] == 'map':
			if len(info['lines']) >= 3:
				self.data.addElement(ForgeryElements.ForgeryPolygon(
					elementID = info['id'],
					layer = info.get('layer', 'layer 000'),
					lines = info['lines'],
					floorOffset = float(info.get('floorOffset', '0')),
					floor = info['surfaces'].get('floor', None),
					ceilingOffset = float(info.get('ceilingOffset', '1024')),
					ceiling = info['surfaces'].get('ceiling', None),
				))
			else:
				raise ValueError, "A polygon must have at least 3 lines"
		elif parent['tag'] == 'action':
			if parent['kind'] == 'switch':
				if set(info) == set(('id', 'lines', 'state', 'surfaces', 'tag')) and not info['lines'] and not info['surfaces']:
					parent['elements'].append((info['id'], info['state']))
				else:
					raise ValueError, "State change tags must not have any children or attributes other than id and state"
			else:
				raise ValueError, "<polygon> tags cannot be children of non-switch <action> tags"
		else:
			raise ValueError, "<polygon> tags can only be children of <map> tags and <action> tags"
	
	def endMapElement(self):
		self.data.mapinfo = info
		for element in self.data.lines.values() + self.data.polygons.values() + self.data.vertices.values() + self.data.surfaces.values():
			element.findParents(self.data)

def loadsceB(f, data):
	ForgerysceBLoader(data).loadsceB(plistlib.readPlist(f))
	return data
