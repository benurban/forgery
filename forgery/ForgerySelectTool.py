# ForgerySelectTool.py
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
	'ForgerySelectTool',
)

import ForgeryCursor, ForgeryElements, ForgeryInspector, ForgeryPoint, ForgeryTool

from OpenGL.GL import *

import math

class ForgerySelectTool(ForgeryTool.ForgeryTool):
	iconFileName = 'Arrow.png'
	cursor = ForgeryCursor.arrow
	toolID = ID.SELECT_TOOL
	position = (0, 0)
	
	selection = None
	drawingBox = False
	clickOrigin = None
	modifiers = (False, False, False) # command, option, shift
	
	#vertexOutlineCoords = ( # no longer used
	#	(3, 0),
	#	(3 / sqrt2, 3 / sqrt2),
	#	(0, 3),
	#	(-3 / sqrt2, 3 / sqrt2),
	#	(-3, 0),
	#	(-3 / sqrt2, -3 / sqrt2),
	#	(0, -3),
	#	(3 / sqrt2, -3 / sqrt2),
	#)
	
	inspector = property(fget = lambda self: ForgeryInspector.sharedInspector())
	player = property(
		fget = lambda self: getattr(self.view, 'player'),
		fset = lambda self, value: setattr(self.view, 'player', value),
	)
	
	selectionColor = property(fget = lambda self: self.preferences.selectionColor)
	
	def __init__(self, *posArgs, **kwdArgs):
		super(ForgerySelectTool, self).__init__(*posArgs, **kwdArgs)
		self.selection = set()
		self.drawingBox = False
		self.clickOrigin = None
		self.modifiers = (False, False, False) # command, option, shift
	
	def activate(self):
		super(ForgerySelectTool, self).activate()
		self.addDrawHook(self.drawSelection)
		self.refresh()
		self.inspector.update()
	
	def deactivate(self):
		self.removeDrawHook(self.drawSelection)
		super(ForgerySelectTool, self).deactivate()
		self.refresh()
		self.inspector.update()
	
	def validateUI(self, itemID):
		dispatchTable = {
			ID.CUT:        self.objectsAreSelected,
			ID.COPY:       self.objectsAreSelected,
			ID.PASTE:      False,
			ID.DELETE:     self.objectsAreSelected,
			ID.DUPLICATE:  self.objectsAreSelected,
			ID.SELECTALL:  True,
			ID.SELECTNONE: self.objectsAreSelected,
		}
		result = dispatchTable.get(itemID, None)
		if callable(result):
			result = result()
		return result
	
	def objectsAreSelected(self):
		if self.selection:
			return True
		else:
			return False
	
	def getStatusText(self):
		count = len(self.selection)
		if count == 1:
			return u"1 object selected"
		else:
			return u"%s objects selected" % count
	
	def cutSelection(self):
		if len(self.selection) == 1:
			undoName = u"Cut Object '%s'" % (tuple(self.selection)[0].elementID, )
		else:
			undoName = u"Cut %s Objects" % (len(self.selection, ))
		self.copySelection()
		self.deleteSelection(undoName = undoName)
	
	def copySelection(self): # note that this is not undoable
		self.sendXMLToPasteboard(self.data.elementsToXML(self.selection))
	
	def paste(self):
		self.openUndoGroup(u"Paste")
		# FIXME
		self.closeUndoGroup()
		self.refresh()
		self.adjustScrollbars()
		self.inspector.update()
	
	def deleteSelection(self, undoName = None):
		if not undoName:
			if len(self.selection) == 1:
				undoName = u"Delete Object '%s'" % (tuple(self.selection)[0].elementID, )
			else:
				undoName = u"Delete %s Objects" % (len(self.selection, ))
		self.openUndoGroup(undoName)
		self.data.deleteElements(set(self.selection))
		self.closeUndoGroup()
		self.refresh()
		self.adjustScrollbars()
		self.inspector.update()
	
	def duplicateSelection(self):
		if len(self.selection) == 1:
			self.openUndoGroup(u"Duplicate Object '%s'" % (tuple(self.selection)[0].elementID, ))
		else:
			self.openUndoGroup(u"Duplicate %s Objects" % (len(self.selection, )))
		# FIXME
		self.closeUndoGroup()
		pass
	
	def selectAll(self):
		self.selection = set( \
			self.data.polygons.values() + \
			self.data.lines.values() + \
			self.data.vertices.values() \
		)
		self.refresh()
		self.inspector.update()
	
	def selectNone(self):
		self.selection = set()
		self.refresh()
		self.inspector.update()
	
	def mouseDown(self, modifiers):
		self.modifiers = modifiers
		pos = self.clickOrigin = self.mouse1.convertTo('object')
		if self.modifiers == (True, False, False): # command key is down
			self.player = self.mouse1
		else:
			radius = self.vertexSelectionRadius * self.zoomFactor
			radius2 = radius * radius
			for v in self.data.vertices.values():
				if (pos - (v.x, v.y)).r2 <= radius2:
					if self.modifiers[2]: # shift key is down
						if v in self.selection:
							self.selection.remove(v)
						else:
							self.selection.add(v)
					elif v not in self.selection:
						self.selection = set([v])
					self.drawingBox = False
					break
			else:
				for l in self.data.lines.values():
					if l.distanceToPoint(*pos) <= radius:
						if self.modifiers[2]: # shift key is down
							if l in self.selection:
								self.selection.remove(l)
							else:
								self.selection.add(l)
						elif l not in self.selection:
							self.selection = set([l])
						self.drawingBox = False
						break
				else:
					for p in self.data.polygons.values():
						if pos in p:
							if self.modifiers[2]: # shift key is down
								if p in self.selection:
									self.selection.remove(p)
								else:
									self.selection.add(p)
							elif p not in self.selection:
								self.selection = set([p])
							self.drawingBox = False
							break
					else:
						if self.modifiers[2]: # shift key is down
							self.initialSelection = self.selection.copy()
						else:
							self.selection = set()
						self.drawingBox = True
						self.addDrawHook(self.drawBox)
		self.refresh()
		self.inspector.update()
	
	def mouseDragged(self, modifiers):
		pos0 = self.mouse0.convertTo('object')
		pos1 = self.mouse1.convertTo('object')
		if self.snapToGrid:
			gridSpacing = self.realGridSpacing
			pos0 = ForgeryPoint.ForgeryPoint(
				pos0.coordinates,
				pos0.view,
				roundToNearest(pos0.x, gridSpacing),
				roundToNearest(pos0.y, gridSpacing),
			)
			pos1 = ForgeryPoint.ForgeryPoint(
				pos1.coordinates,
				pos1.view,
				roundToNearest(pos1.x, gridSpacing),
				roundToNearest(pos1.y, gridSpacing),
			)
		if self.modifiers == (True, False, False): # command key is down
			self.player = pos1
		elif self.drawingBox:
			l = min(self.clickOrigin.x, pos1.x)
			b = min(self.clickOrigin.y, pos1.y)
			r = max(self.clickOrigin.x, pos1.x)
			t = max(self.clickOrigin.y, pos1.y)
			radius = self.vertexSelectionRadius * self.zoomFactor
			selection = set()
			for v in self.data.vertices.values():
				if self.__circleIntersectsSelectionBox((v.x, v.y), radius, (l, b), (r, t)):
					selection.add(v)
			if self.modifiers[2]: # shift key is down
				self.selection = self.initialSelection.copy()
				for obj in selection:
					if obj in self.selection:
						self.selection.remove(obj)
					else:
						self.selection.add(obj)
			else:
				self.selection = selection
		else:
			d = pos1 - pos0
			objs = set()
			for obj in self.selection:
				objs.update(obj.getAllVertexAncestors())
			for obj in objs:
				obj.move(*d)
		self.refresh()
		self.adjustScrollbars()
		self.inspector.update()
	
	def mouseUp(self, modifiers):
		if self.modifiers == (True, False, False): # command key is down
			pass
		elif self.drawingBox:
			if self.modifiers[2]: # shift key is down
				del self.initialSelection
			self.drawingBox = False
			self.removeDrawHook(self.drawBox)
		else:
			pos0 = self.clickOrigin
			pos1 = self.mouse1.convertTo('object')
			if self.snapToGrid:
				gridSpacing = self.realGridSpacing
				pos0 = ForgeryPoint.ForgeryPoint(
					pos0.coordinates,
					pos0.view,
					roundToNearest(pos0.x, gridSpacing),
					roundToNearest(pos0.y, gridSpacing),
				)
				pos1 = ForgeryPoint.ForgeryPoint(
					pos1.coordinates,
					pos1.view,
					roundToNearest(pos1.x, gridSpacing),
					roundToNearest(pos1.y, gridSpacing),
				)
			d = pos1 - pos0
			if d.x or d.y: # maybe the user clicked without dragging
				vertices = set()
				for element in self.selection:
					vertices.update(element.getAllVertexAncestors())
				for vertex in vertices:
					vertex.move(*(-d))
				if len(self.selection) == 1:
					self.openUndoGroup(u"Move Object '%s'" % (tuple(self.selection)[0].elementID, ))
				else:
					self.openUndoGroup(u"Move %s Objects" % (len(self.selection), ))
				self.data.moveElements(self.selection, d)
				self.closeUndoGroup()
				self.adjustScrollbars()
		self.refresh()
		self.inspector.update()
	
	def sendXMLToPasteboard(self, xml):
		# FIXME
		pass
	
	def getXMLFromPasteboard(self):
		# FIXME
		return None
	
	def __circleIntersectsSelectionBox(self, (x, y), r, (x0, y0), (x1, y1)):
		if x + r > x0 and y + r > y0 and x - r < x1 and y - r < y1:
			if x0 > x and y0 > y:
				if (x0 - x) * (x0 - x) + (y0 - y) * (y0 - y) < r * r:
					return True
				else:
					return False
			elif x0 > x and y1 < y:
				if (x0 - x) * (x0 - x) + (y1 - y) * (y1 - y) < r * r:
					return True
				else:
					return False
			elif x1 < x and y0 > y:
				if (x1 - x) * (x1 - x) + (y0 - y) * (y0 - y) < r * r:
					return True
				else:
					return False
			elif x1 < x and y1 < y:
				if (x1 - x) * (x1 - x) + (y1 - y) * (y1 - y) < r * r:
					return True
				else:
					return False
			else:
				return True
		else:
			return False
	
	def drawSelection(self):
		#coords = [(x * self.zoomFactor, y * self.zoomFactor) for x, y in self.vertexOutlineCoords]
		for obj in self.selection.copy():
			# The object might not exist anymore if it was undone
			# while it was selected, or if it was deleted
			if self.data[obj.category].get(obj.elementID, None) is not obj:
				# I know, I shouldn't change the data while I'm
				# drawing, but when else can I change it?
				self.selection.remove(obj)
		polygons = (obj for obj in self.selection if isinstance(obj, ForgeryElements.ForgeryPolygon))
		lines = (obj for obj in self.selection if isinstance(obj, ForgeryElements.ForgeryLine))
		vertices = (obj for obj in self.selection if isinstance(obj, ForgeryElements.ForgeryVertex))
		
		color = self.selectionColor
		glColor4f(color[0], color[1], color[2], 0.5)
		#glColor4f(1.0, 0.0, 0.0, 0.2)
		for p in polygons:
			glBegin(GL_POLYGON)
			p.drawSelf()
			glEnd()
		
		#glColor3f(1.0, 0.5, 0.5)
		glLineWidth(3.0)
		glBegin(GL_LINES)
		for l in lines:
			l.drawSelf()
		glEnd()
		glLineWidth(1.0)
		
		glPointSize(6.0)
		#glColor3f(1.0, 0.0, 0.0)
		glBegin(GL_POINTS)
		for v in vertices:
			#glBegin(GL_LINE_LOOP)
			#for x, y in coords:
			#	glVertex2f(x + v.x, y + v.y)
			#glEnd()
			v.drawSelf()
		glEnd()
		glPointSize(1.0)
	
	def drawBox(self):
		x0, y0 = self.clickOrigin.asObject
		x1, y1 = self.mouse1.asObject
		glColor4f(0.0, 0.0, 0.0, 0.2)
		glBegin(GL_QUADS)
		glVertex2f(x0, y0)
		glVertex2f(x0, y1)
		glVertex2f(x1, y1)
		glVertex2f(x1, y0)
		glEnd()
		glColor3f(0.0, 0.0, 0.0)
		glBegin(GL_LINE_LOOP)
		glVertex2f(x0, y0)
		glVertex2f(x0, y1)
		glVertex2f(x1, y1)
		glVertex2f(x1, y0)
		glEnd()

ForgeryTool.tools[ForgerySelectTool.toolID] = ForgerySelectTool
