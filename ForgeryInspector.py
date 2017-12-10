# ForgeryInspector.py
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
	'ForgeryInspector',
	'sharedInspector',
)

import ForgeryApplication, ForgeryElements, ForgeryPreferences

if usePyObjC:
	
	from Foundation import *
	from AppKit import *
	
else:
	
	import wx, wx.grid
	import os

from tracer import traced

class ForgeryInspector(NSWindowController if usePyObjC else wx.MiniFrame):
	_sharedInspector = None
	
	@property
	@traced
	def app(self):
		return ForgeryApplication.sharedApplication()
	@property
	@traced
	def document(self):
		return self.app.frontDocument
	@property
	@traced
	def preferences(self):
		return self.document.preferences if self.document else self.app.preferences
	
	isDocked = property(
		fget = lambda self: getattr(self.preferences, 'inspectorIsDocked'),
		fset = lambda self, value: setattr(self.preferences, 'inspectorIsDocked', value),
	)
	position = property(
		fget = traced(lambda self: getattr(self.preferences, 'inspectorPosition')),
		fset = traced(lambda self, value: setattr(self.preferences, 'inspectorPosition', value)),
	)
	isVisible = property(
		fget = lambda self: getattr(self.preferences, 'inspectorIsVisible'),
		fset = lambda self, value: setattr(self.preferences, 'inspectorIsVisible', value),
	)
	
	@property
	def data(self):
		return self.document.data
	@property
	def mode(self):
		return self.document.currentMode
	@property
	def tool(self):
		return self.mode.currentTool if hasattr(self.mode, 'currentTool') else None
	@property
	def selection(self):
		return self.tool.selection if hasattr(self.tool, 'selection') else None
	@property
	def selectedElement(self):
		return tuple(self.selection)[0] # sets cannot be indexed
	
	@property
	def vertex(self):
		return {
			'xField': self.vertexXField,
			'yField': self.vertexYField,
		}
	
	@property
	def line(self):
		return {
			'vertex0Field': self.lineVertex0Field,
			'vertex1Field': self.lineVertex1Field,
			'blocksPlayersCheckbox': self.lineBlocksPlayersCheckbox,
			'blocksAlliesCheckbox': self.lineBlocksAlliesCheckbox,
			'blocksEnemiesCheckbox': self.lineBlocksEnemiesCheckbox,
			'blocksTeamsCheckbox': self.lineBlocksTeamsCheckbox,
			'blocksTeamsPropertiesButton': self.lineBlocksTeamsPropertiesButton,
			'mapVisibilityRadioGroup': self.lineMapVisibilityRadioGroup,
			'mapVisibilityPropertiesButton': self.lineMapVisibilityPropertiesButton,
			'side': (
				{
					'polygonField': self.lineSide0PolygonField,
					'bottom': {
						'dxSlider': self.lineSide0BottomDXSlider,
						'dySlider': self.lineSide0BottomDYSlider,
						'textureWell': self.lineSide0BottomTextureWell,
						'landscapeCheckbox': self.lineSide0BottomLandscapeCheckbox,
						'effectMenu': self.lineSide0BottomEffectMenu,
						'effectPropertiesButton': self.lineSide0BottomEffectPropertiesButton,
						'lightField': self.lineSide0BottomLightField,
						'actionsButton': self.lineSide0BottomActionsButton,
					},
					'middle': {
						'dxSlider': self.lineSide0MiddleDXSlider,
						'dySlider': self.lineSide0MiddleDYSlider,
						'textureWell': self.lineSide0MiddleTextureWell,
						'landscapeCheckbox': self.lineSide0MiddleLandscapeCheckbox,
						'effectMenu': self.lineSide0MiddleEffectMenu,
						'effectPropertiesButton': self.lineSide0MiddleEffectPropertiesButton,
						'lightField': self.lineSide0MiddleLightField,
						'actionsButton': self.lineSide0MiddleActionsButton,
					},
					'top': {
						'dxSlider': self.lineSide0TopDXSlider,
						'dySlider': self.lineSide0TopDYSlider,
						'textureWell': self.lineSide0TopTextureWell,
						'landscapeCheckbox': self.lineSide0TopLandscapeCheckbox,
						'effectMenu': self.lineSide0TopEffectMenu,
						'effectPropertiesButton': self.lineSide0TopEffectPropertiesButton,
						'lightField': self.lineSide0TopLightField,
						'actionsButton': self.lineSide0TopActionsButton,
					},
				}, {
					'polygonField': self.lineSide1PolygonField,
					'bottom': {
						'dxSlider': self.lineSide1BottomDXSlider,
						'dySlider': self.lineSide1BottomDYSlider,
						'textureWell': self.lineSide1BottomTextureWell,
						'landscapeCheckbox': self.lineSide1BottomLandscapeCheckbox,
						'effectMenu': self.lineSide1BottomEffectMenu,
						'effectPropertiesButton': self.lineSide1BottomEffectPropertiesButton,
						'lightField': self.lineSide1BottomLightField,
						'actionsButton': self.lineSide1BottomActionsButton,
					},
					'middle': {
						'dxSlider': self.lineSide1MiddleDXSlider,
						'dySlider': self.lineSide1MiddleDYSlider,
						'textureWell': self.lineSide1MiddleTextureWell,
						'landscapeCheckbox': self.lineSide1MiddleLandscapeCheckbox,
						'effectMenu': self.lineSide1MiddleEffectMenu,
						'effectPropertiesButton': self.lineSide1MiddleEffectPropertiesButton,
						'lightField': self.lineSide1MiddleLightField,
						'actionsButton': self.lineSide1MiddleActionsButton,
					},
					'top': {
						'dxSlider': self.lineSide1TopDXSlider,
						'dySlider': self.lineSide1TopDYSlider,
						'textureWell': self.lineSide1TopTextureWell,
						'landscapeCheckbox': self.lineSide1TopLandscapeCheckbox,
						'effectMenu': self.lineSide1TopEffectMenu,
						'effectPropertiesButton': self.lineSide1TopEffectPropertiesButton,
						'lightField': self.lineSide1TopLightField,
						'actionsButton': self.lineSide1TopActionsButton,
					},
				},
			),
		}
	
	@property
	def polygon(self):
		return {
			'table': self.polygonTable,
			'layer': {
				'menu': self.polygonLayerMenu,
				'offsetField': self.polygonLayerOffsetField,
				'offsetUnitsField': self.polygonLayerOffsetUnitsField,
			},
			'actionsButton': self.polygonActionsButton,
			'floor': {
				'heightField': self.polygonFloorHeightField,
				'heightStepper': self.polygonFloorHeightStepper,
				'offsetField': self.polygonFloorOffsetField,
				'offsetStepper': self.polygonFloorOffsetStepper,
				'dxSlider': self.polygonFloorDXSlider,
				'dySlider': self.polygonFloorDYSlider,
				'textureWell': self.polygonFloorTextureWell,
				'landscapeCheckbox': self.polygonFloorLandscapeCheckbox,
				'effectMenu': self.polygonFloorEffectMenu,
				'effectPropertiesButton': self.polygonFloorEffectPropertiesButton,
				'lightField': self.polygonFloorLightField,
				'actionsButton': self.polygonFloorActionsButton,
			},
			'ceiling': {
				'heightField': self.polygonCeilingHeightField,
				'heightStepper': self.polygonCeilingHeightStepper,
				'offsetField': self.polygonCeilingOffsetField,
				'offsetStepper': self.polygonCeilingOffsetStepper,
				'dxSlider': self.polygonCeilingDXSlider,
				'dySlider': self.polygonCeilingDYSlider,
				'textureWell': self.polygonCeilingTextureWell,
				'landscapeCheckbox': self.polygonCeilingLandscapeCheckbox,
				'effectMenu': self.polygonCeilingEffectMenu,
				'effectPropertiesButton': self.polygonCeilingEffectPropertiesButton,
				'lightField': self.polygonCeilingLightField,
				'actionsButton': self.polygonCeilingActionsButton,
			},
		}
	
	_sharedInspector = None
	@classmethod
	def sharedInspector(Class):
		if not Class._sharedInspector:
			if usePyObjC:
				Class._sharedInspector = Class.alloc().init()
			else:
				Class._sharedInspector = Class()
		return Class._sharedInspector
	
	@traced
	def setAttribute(self, prefix, suffix, value):
		return setattr(self, prefix + suffix, value)
	
	@traced
	def getPath(self, path):
		current = getattr(self, path[0])
		for entry in path[1:]:
			current = current[entry]
		return current
	
	@traced
	def refresh(self):
		self.document.view.refresh()
	
	if usePyObjC:
		@traced
		def getFrame(self):
			frame = self.window().frame()
			bottom = frame.origin.y
			left = frame.origin.x
			top = bottom + frame.size.height
			right = left + frame.size.width
			return (left, top, right, bottom)
	else:
		@traced
		def getFrame(self):
			frame = self.GetScreenRect()
			left = frame.GetLeft()
			top = frame.GetTop()
			right = frame.GetRight()
			bottom = frame.GetBottom()
			return (left, top, right, bottom)
	
	@traced
	def updatePosition(self):
		if self.isDocked:
			try:
				itsLeft, itsTop, itsRight, itsBottom = self.document.getFrame()
			except AttributeError:
				pass
			else:
				myLeft, myTop, myRight, myBottom = self.getFrame()
				self.moveTo((itsRight + 10, myTop + itsBottom - myBottom))
		else:
			self.moveTo(self.position)
	
	@traced
	def updateVisibility(self):
		if self.isVisible and self.app.documents:
			self.show()
		else:
			self.hide()
	
	@traced
	def toggleText(self):
		if self.isVisible:
			return u"Hide Inspector" if usePyObjC else u"Hide &Inspector"
		else:
			return u"Show Inspector" if usePyObjC else u"Show &Inspector"
	
	@traced
	def setTitle(self, title):
		if usePyObjC:
			self.window().setTitle_(title)
		else:
			self.SetTitle(title)
	
	@traced
	def show(self):
		if usePyObjC:
			self.showWindow_(self)
		else:
			self.Show()
	
	@traced
	def hide(self):
		if usePyObjC:
			self.window().close()
		else:
			self.Hide()
	
	@traced
	def moveTo(self, (x, y)):
		if usePyObjC:
			self.window().setFrameTopLeftPoint_((x, y))
		else:
			self.MoveXY(x, y)
	
	@traced
	def moved(self):
		myLeft, myTop, myRight, myBottom = self.getFrame()
		itsLeft, itsTop, itsRight, itsBottom = self.document.getFrame()
		if -20 < myLeft - (itsRight + 10) < 20 and -20 < myBottom - itsBottom < 20:
			self.isDocked = True
			self.position = None
		else:
			self.isDocked = False
			self.position = (myLeft, myTop)
		self.updatePosition()
	
	def texturesUpdated(self):
		self.update()
	
	@traced
	def update(self):
		if not self.selection:
			self.setTitle(u"Inspector")
			if usePyObjC:
				self.idField.setStringValue_('')
				self.idField.setEnabled_(False)
				self.tabView.selectTabViewItemAtIndex_(0)
			else:
				self.idField.ChangeValue('')
				self.idField.Disable()
				self.tabView.SetActivePage(ID.NO_SELECTION)
		elif len(self.selection) >= 2:
			self.setTitle(u"Inspector")
			if usePyObjC:
				self.idField.setStringValue_('')
				self.idField.setEnabled_(False)
				self.tabView.selectTabViewItemAtIndex_(1)
			else:
				self.idField.ChangeValue('')
				self.idField.Disable()
				self.tabView.SetActivePage(ID.MULTIPLE_SELECTION)
		else:
			selection = self.selectedElement
			if usePyObjC:
				self.idField.setStringValue_(str(selection.elementID))
				self.idField.setEnabled_(True)
			else:
				self.idField.ChangeValue(str(selection.elementID))
				self.idField.Enable()
			if isinstance(selection, ForgeryElements.ForgeryVertex):
				self.setTitle(u"Vertex Inspector")
				self.updateVertex(selection, self.vertex)
				if usePyObjC:
					self.tabView.selectTabViewItemAtIndex_(2)
				else:
					self.tabView.SetActivePage(ID.VERTEX)
			elif isinstance(selection, ForgeryElements.ForgeryLine):
				self.setTitle(u"Line Inspector")
				self.updateLine(selection, self.line)
				if usePyObjC:
					self.tabView.selectTabViewItemAtIndex_(3)
				else:
					self.tabView.SetActivePage(ID.LINE)
			elif isinstance(selection, ForgeryElements.ForgeryPolygon):
				self.setTitle(u"Polygon Inspector")
				self.updatePolygon(selection, self.polygon)
				if usePyObjC:
					self.tabView.selectTabViewItemAtIndex_(4)
				else:
					self.tabView.SetActivePage(ID.POLYGON)
			#elif isinstance(selection, ForgeryElements.ForgeryObject):
			#	self.setTitle(u"Object Inspector")
			#	if usePyObjC:
			#		self.tabView.selectTabViewItemAtIndex_(5)
			#	else:
			#		self.tabView.SetActivePage(ID.OBJECT)
			#elif isinstance(selection, ForgeryElements.ForgerySound):
			#	self.setTitle(u"Sound Inspector")
			#	if usePyObjC:
			#		self.tabView.selectTabViewItemAtIndex_(6)
			#	else:
			#		self.tabView.SetActivePage(ID.SOUND)
		
		self.updatePosition()
	
	@traced
	def updateVertex(self, vertex, vertexUI):
		if usePyObjC:
			vertexUI['xField'].setDoubleValue_(vertex.x)
			vertexUI['yField'].setDoubleValue_(vertex.y)
		else:
			vertexUI['xField'].ChangeValue(str(vertex.x))
			vertexUI['yField'].ChangeValue(str(vertex.y))
	
	@traced
	def updateLine(self, line, lineUI):
		if usePyObjC:
			lineUI['vertex0Field'].setStringValue_(unicode(line.vertex0.elementID))
			lineUI['vertex1Field'].setStringValue_(unicode(line.vertex1.elementID))
			# FIXME: NSButton lineBlocksPlayersCheckbox
			# FIXME: NSButton lineBlocksAlliesCheckbox
			# FIXME: NSButton lineBlocksEnemiesCheckbox
			# FIXME: NSButton lineBlocksTeamsCheckbox
			# FIXME: NSButton lineBlocksTeamsPropertiesButton
			# FIXME: NSMatrix lineMapVisibilityRadioGroup
			# FIXME: NSButton lineMapVisibilityPropertiesButton
		else:
			lineUI['vertex0Field'].ChangeValue(unicode(line.vertex0.elementID))
			lineUI['vertex1Field'].ChangeValue(unicode(line.vertex1.elementID))
			# FIXME: wx.Checkbox lineBlocksPlayersCheckbox
			# FIXME: wx.Checkbox lineBlocksAlliesCheckbox
			# FIXME: wx.Checkbox lineBlocksEnemiesCheckbox
			# FIXME: wx.Checkbox lineBlocksTeamsCheckbox
			# FIXME: ? lineBlocksTeamsPropertiesButton
			# FIXME: ? lineMapVisibilityRadioGroup
			# FIXME: ? lineMapVisibilityPropertiesButton
		for index, sideUI in enumerate(lineUI['side']):
			self.updateSide(line, getattr(line, 'side' + str(index)), index, sideUI)
	
	@traced
	def updatePolygon(self, polygon, polygonUI):
		polygon.findSides()
		if usePyObjC:
			# FIXME: Ranges?
			polygonUI['floor']['heightField'].setDoubleValue_(polygon.floorHeight)
			polygonUI['floor']['heightStepper'].setDoubleValue_(polygon.floorHeight)
			polygonUI['floor']['offsetField'].setDoubleValue_(polygon.floorOffset)
			polygonUI['floor']['offsetStepper'].setDoubleValue_(polygon.floorOffset)
			polygonUI['ceiling']['heightField'].setDoubleValue_(polygon.ceilingHeight)
			polygonUI['ceiling']['heightStepper'].setDoubleValue_(polygon.ceilingHeight)
			polygonUI['ceiling']['offsetField'].setDoubleValue_(polygon.ceilingOffset)
			polygonUI['ceiling']['offsetStepper'].setDoubleValue_(polygon.ceilingOffset)
		else:
			# FIXME: Steppers?
			polygonUI['floor']['heightField'].SetRange(-2147483648, int(polygon.ceilingHeight))
			polygonUI['floor']['heightField'].SetValue(int(polygon.floorHeight))
			polygonUI['floor']['offsetField'].SetRange(-2147483648, int(polygon.ceilingOffset))
			polygonUI['floor']['offsetField'].SetValue(int(polygon.floorOffset))
			polygonUI['ceiling']['heightField'].SetRange(int(polygon.floorHeight), 2147483647)
			polygonUI['ceiling']['heightField'].SetValue(int(polygon.ceilingHeight))
			polygonUI['ceiling']['offsetField'].SetRange(int(polygon.floorOffset), 2147483647)
			polygonUI['ceiling']['offsetField'].SetValue(int(polygon.ceilingOffset))
		self.updatePolygonTable(polygon, polygonUI['table'])
		self.updateLayer(polygon.layer, polygonUI['layer'])
		self.updateSurface(polygon.floor, polygonUI['floor'])
		self.updateSurface(polygon.ceiling, polygonUI['ceiling'])
	
	@traced
	def updatePolygonTable(self, polygon, tableUI):
		table = [(getattr(line, 'vertex' + str(side)), line) for line, side in zip(polygon, polygon.sides)] # we're assuming that findSides() has already been called
		if not usePyObjC:
			tableRows = len(table)
			tableUI.BeginBatch()
			uiRows = tableUI.GetNumberRows()
			if uiRows > tableRows:
				tableUI.DeleteRows(tableRows, uiRows - tableRows)
			elif uiRows < tableRows:
				tableUI.InsertRows(uiRows, tableRows - uiRows)
			for row, (vertex, line) in enumerate(table):
				if vertex:
					tableUI.SetCellValue(row, 0, unicode(vertex.elementID))
				else: # this should never happen
					tableUI.SetCellValue(row, 0, u"")
				if line:
					tableUI.SetCellValue(row, 1, unicode(line.elementID))
				else: # this should never happen
					tableUI.SetCellValue(row, 1, u"")
			tableUI.EndBatch()
	
	@traced
	def updateLayer(self, layer, layerUI):
		layers = [unicode(elementID) for elementID in self.data.layers]
		layers.sort()
		if usePyObjC:
			while layerUI['menu'].menu().numberOfItems():
				layerUI['menu'].menu().removeItemAtIndex_(0)
			for elementID in layers:
				layerUI['menu'].menu().addItemWithTitle_action_keyEquivalent_(elementID, None, '')
			layerUI['menu'].selectItemWithTitle_(unicode(layer.elementID))
			layerUI['offsetField'].setDoubleValue_(float(layer.offset) / float(WU))
			# FIXME: layerUI['offsetUnitsField']
		else:
			layerUI['menu'].Clear()
			layerUI['menu'].AppendItems(layers)
			layerUI['menu'].SetStringSelection(unicode(layer.elementID))
			layerUI['offsetField'].SetLabel(u"%1.2f" % (float(layer.offset) / float(WU), ))
			layerUI['offsetUnitsField'].SetLabel(u"WU")
	
	@traced
	def updateSide(self, line, side, index, sideUI):
		if side:
			polygon = self.data.polygonForSide(line, index)
			try:
				polygon = unicode(polygon.elementID)
			except AttributeError: # this will happen for invalid lines
				polygon = u""
			if usePyObjC:
				#sideUI['polygonField'].setEnabled_(True)
				sideUI['polygonField'].setStringValue_(polygon)
			else:
				sideUI['polygonField'].ChangeValue(polygon)
			self.updateSurface(side.lowerSurface, sideUI['bottom'])
			self.updateSurface(side.middleSurface, sideUI['middle'])
			self.updateSurface(side.upperSurface, sideUI['top'])
		else:
			if usePyObjC:
				#sideUI['polygonField'].setEnabled_(False)
				sideUI['polygonField'].setStringValue_(u"")
			else:
				sideUI['polygonField'].ChangeValue(u"")
			self.updateSurface(None, sideUI['bottom'])
			self.updateSurface(None, sideUI['middle'])
			self.updateSurface(None, sideUI['top'])
	
	@traced
	def updateSurface(self, surface, surfaceUI):
		if surface:
			if usePyObjC:
				surfaceUI['dxSlider'].setEnabled_(True)
				surfaceUI['dxSlider'].setDoubleValue_(surface.dx)
				surfaceUI['dySlider'].setEnabled_(True)
				surfaceUI['dySlider'].setDoubleValue_(surface.dy)
				surfaceUI['textureWell'].setEnabled_(True)
				surfaceUI['textureWell'].setImage_(surface.image)
				surfaceUI['landscapeCheckbox'].setEnabled_(True)
				if 'landscape' in surface.effects:
					surfaceUI['landscapeCheckbox'].setState_(True)
				else:
					surfaceUI['landscapeCheckbox'].setState_(False)
				surfaceUI['effectMenu'].setEnabled_(True)
				if 'pulsate' in surface.effects:
					surfaceUI['effectMenu'].selectItemWithTag_(ID.EFFECT_PULSATE)
					surfaceUI['effectPropertiesButton'].setEnabled_(True)
				elif 'wobble' in surface.effects:
					surfaceUI['effectMenu'].selectItemWithTag_(ID.EFFECT_WOBBLE)
					surfaceUI['effectPropertiesButton'].setEnabled_(True)
				elif 'slide' in surface.effects:
					surfaceUI['effectMenu'].selectItemWithTag_(ID.EFFECT_SLIDE)
					surfaceUI['effectPropertiesButton'].setEnabled_(True)
				elif 'wander' in surface.effects:
					surfaceUI['effectMenu'].selectItemWithTag_(ID.EFFECT_WANDER)
					surfaceUI['effectPropertiesButton'].setEnabled_(True)
				else:
					surfaceUI['effectMenu'].selectItemWithTag_(ID.EFFECT_NORMAL)
					surfaceUI['effectPropertiesButton'].setEnabled_(False)
				surfaceUI['lightField'].setEnabled_(True)
				# FIXME: NSTokenField surfaceUI['lightField']
				surfaceUI['actionsButton'].setEnabled_(True)
				# FIXME: Check Events panel and highlight button appropriately
				surfaceUI['actionsButton'].setState_(False)
				# FIXME: Update Events panel
			else:
				surfaceUI['dxSlider'].Enable()
				surfaceUI['dxSlider'].SetValue(int(surface.dx))
				surfaceUI['dySlider'].Enable()
				surfaceUI['dySlider'].SetValue(int(surface.dy))
				surfaceUI['textureWell'].Enable()
				surfaceUI['textureWell'].SetBitmapLabel(surface.image)
				surfaceUI['landscapeCheckbox'].Enable()
				if 'landscape' in surface.effects:
					surfaceUI['landscapeCheckbox'].SetValue(True)
				else:
					surfaceUI['landscapeCheckbox'].SetValue(False)
				surfaceUI['effectMenu'].Enable()
				if 'pulsate' in surface.effects:
					surfaceUI['effectMenu'].SetSelection(1)
					surfaceUI['effectPropertiesButton'].Enable()
				elif 'wobble' in surface.effects:
					surfaceUI['effectMenu'].SetSelection(2)
					surfaceUI['effectPropertiesButton'].Enable()
				elif 'slide' in surface.effects:
					surfaceUI['effectMenu'].SetSelection(3)
					surfaceUI['effectPropertiesButton'].Enable()
				elif 'wander' in surface.effects:
					surfaceUI['effectMenu'].SetSelection(4)
					surfaceUI['effectPropertiesButton'].Enable()
				else:
					surfaceUI['effectMenu'].SetSelection(0)
					surfaceUI['effectPropertiesButton'].Disable()
				surfaceUI['lightField'].Enable()
				# FIXME: wx.TextCtrl surfaceUI['lightField']
				surfaceUI['actionsButton'].Enable()
				# FIXME: Check Events panel and highlight button appropriately
				surfaceUI['actionsButton'].SetValue(False)
				# FIXME: Update Events panel
		else:
			if usePyObjC:
				surfaceUI['dxSlider'].setEnabled_(False)
				surfaceUI['dxSlider'].setDoubleValue_(0.0)
				surfaceUI['dySlider'].setEnabled_(False)
				surfaceUI['dySlider'].setDoubleValue_(0.0)
				surfaceUI['textureWell'].setEnabled_(False)
				surfaceUI['textureWell'].setImage_(None)
				surfaceUI['landscapeCheckbox'].setEnabled_(False)
				surfaceUI['effectMenu'].setEnabled_(False)
				surfaceUI['effectMenu'].selectItemWithTag_(ID.EFFECT_NORMAL)
				surfaceUI['effectPropertiesButton'].setEnabled_(False)
				surfaceUI['lightField'].setEnabled_(False)
				surfaceUI['lightField'].setStringValue_(u"")
				surfaceUI['actionsButton'].setEnabled_(False)
				surfaceUI['actionsButton'].setState_(False)
				# FIXME: Detach Events panel if attached to this actions button
				# FIXME: Update Events panel
			else:
				surfaceUI['dxSlider'].Disable()
				surfaceUI['dxSlider'].SetValue(0)
				surfaceUI['dySlider'].Disable()
				surfaceUI['dySlider'].SetValue(0)
				surfaceUI['textureWell'].Disable()
				surfaceUI['textureWell'].SetBitmapLabel(wx.EmptyBitmap(128, 128))
				surfaceUI['landscapeCheckbox'].Disable()
				surfaceUI['landscapeCheckbox'].SetValue(False)
				surfaceUI['effectMenu'].Disable()
				surfaceUI['effectMenu'].SetSelection(0)
				surfaceUI['effectPropertiesButton'].Disable()
				surfaceUI['lightField'].Disable()
				surfaceUI['lightField'].ChangeValue("")
				surfaceUI['actionsButton'].Disable()
				surfaceUI['actionsButton'].SetValue(False)
				# FIXME: Detach Events panel if attached to this actions button
				# FIXME: Update Events panel
	
	@traced
	def openUndoGroup(self, name = None):
		return self.document.openUndoGroup(name)
	
	@traced
	def closeUndoGroup(self, name = None):
		return self.document.closeUndoGroup(name)
	
	@traced
	def findSurfaceForUI(self, sender, uiName):
		if sender is self.line['side'][0]['bottom'][uiName]:
			return self.selectedElement.side0.lowerSurface
		elif sender is self.line['side'][0]['middle'][uiName]:
			return self.selectedElement.side0.middleSurface
		elif sender is self.line['side'][0]['top'][uiName]:
			return self.selectedElement.side0.upperSurface
		elif sender is self.line['side'][1]['bottom'][uiName]:
			return self.selectedElement.side1.lowerSurface
		elif sender is self.line['side'][1]['middle'][uiName]:
			return self.selectedElement.side1.middleSurface
		elif sender is self.line['side'][1]['top'][uiName]:
			return self.selectedElement.side1.upperSurface
		elif sender is self.polygon['ceiling'][uiName]:
			return self.selectedElement.ceiling
		elif sender is self.polygon['floor'][uiName]:
			return self.selectedElement.floor
		else:
			return None
	
	@traced
	def idChanged(self, value):
		selection = self.selectedElement
		oldID = selection.elementID
		category = selection.category
		if value and value != oldID:
			if value in self.data[category]:
				# FIXME: beep
				self.update()
			else:
				self.openUndoGroup(u"Change ID")
				self.data.changeID(selection, value)
				self.closeUndoGroup()
		else:
			self.update()
		self.refresh()
	
	@traced
	def lineSolidChanged(self, value):
		# FIXME: lineSolidChnged
		print "%s.lineSolidChanged(%r)" % (self, value)
	
	@traced
	def lineTransparentChanged(self, value):
		# FIXME: lineTransparentChanged
		print "%s.lineTransparentChanged(%r)" % (self, value)
	
	@traced
	def polygonCeilingHeightChanged(self, value):
		# FIXME: The undo group should not start and end here
		polygon = self.selectedElement
		self.openUndoGroup(u"Change Ceiling Height")
		self.data.setPolygonOffset(polygon, 'ceiling', value - polygon.layer.offset)
		self.closeUndoGroup()
		self.update()
	
	@traced
	def polygonCeilingOffsetChanged(self, value):
		# FIXME: The undo group should not start and end here
		polygon = self.selectedElement
		self.openUndoGroup(u"Change Ceiling Offset")
		self.data.setPolygonOffset(polygon, 'ceiling', value)
		self.closeUndoGroup()
		self.update()
	
	@traced
	def polygonFloorHeightChanged(self, value):
		# FIXME: The undo group should not start and end here
		polygon = self.selectedElement
		self.openUndoGroup(u"Change Floor Height")
		self.data.setPolygonOffset(polygon, 'floor', value - polygon.layer.offset)
		self.closeUndoGroup()
		self.update()
	
	@traced
	def polygonFloorOffsetChanged(self, value):
		# FIXME: The undo group should not start and end here
		polygon = self.selectedElement
		self.openUndoGroup(u"Change Floor Offset")
		self.data.setPolygonOffset(polygon, 'floor', value)
		self.closeUndoGroup()
		self.update()
	
	@traced
	def polygonLayerChanged(self, value):
		polygon = self.selectedElement
		layer = self.data.layers[value]
		self.openUndoGroup(u"Change Layer")
		self.data.setPolygonLayer(polygon, layer)
		self.closeUndoGroup()
		self.update()
	
	@traced
	def surfaceActionPropertiesClicked(self, surface, action):
		# FIXME: surfaceActionPropertiesClicked
		print "%s.surfaceActionPropertiesClicked(%s, %r)" % (self, surface, action)
	
	@traced
	def surfaceActionToggled(self, surface, action, value):
		if value:
			self.openUndoGroup(u"Add Action")
			self.data.addSurfaceActionKind(surface, action)
		else:
			self.openUndoGroup(u"Remove Action")
			self.data.delSurfaceActionKind(surface, action)
		self.closeUndoGroup()
		self.update()
	
	@traced
	def surfaceDXChanged(self, surface, value):
		# FIXME: The undo group should not start and end here
		self.openUndoGroup(u"Move Texture")
		self.data.setSurfaceOffset(surface, (value, surface.dy))
		self.closeUndoGroup()
		self.update()
		self.refresh()
	
	@traced
	def surfaceDYChanged(self, surface, value):
		# FIXME: The undo group should not start and end here
		self.openUndoGroup(u"Move Texture")
		self.data.setSurfaceOffset(surface, (surface.dx, value))
		self.closeUndoGroup()
		self.update()
		self.refresh()
	
	@traced
	def surfaceEffectChanged(self, surface, effect):
		self.openUndoGroup(u"Change Effect")
		for key in surface.effects.keys():
			if key in ('pulsate', 'wobble', 'slide', 'wander'):
				self.data.delSurfaceEffect(surface, key)
		if effect == 'pulsate':
			properties = {}
		elif effect == 'wobble':
			properties = {}
		elif effect == 'slide':
			properties = {}
		elif effect == 'wander':
			properties = {}
		if effect in ('pulsate', 'wobble', 'slide', 'wander'):
			self.data.addSurfaceEffect(surface, effect, properties)
		self.closeUndoGroup()
		self.update()
	
	@traced
	def surfaceEffectPropertiesClicked(self, surface, effect):
		# FIXME: surfaceEffectPropertiesClicked
		print "%s.surfaceEffectPropertiesClicked(%s, %r)" % (self, surface, effect)
	
	@traced
	def surfaceLandscapeChanged(self, surface, value):
		self.openUndoGroup(u"Toggle Landscape Mode")
		if value:
			self.data.addSurfaceEffect(surface, 'landscape', {})
		else:
			self.data.removeSurfaceEffect(surface, 'landscape')
		self.closeUndoGroup()
		self.update()
	
	@traced
	def surfaceLightChanged(self, surface, value):
		# FIXME: surfaceLightChanged
		print "%s.surfaceLightChanged(%s, %r)" % (self, surface, value)
	
	@traced
	def vertexXChanged(self, value):
		vertex = self.selectedElement
		self.openUndoGroup(u"Move Vertex '%s'" % (vertex.elementID, ))
		self.data.moveVertex(vertex, (value - vertex.x, 0.0))
		self.closeUndoGroup()
		self.refresh()
	
	@traced
	def vertexYChanged(self, value):
		vertex = self.selectedElement
		self.openUndoGroup(u"Move Vertex '%s'" % (vertex.elementID, ))
		self.data.moveVertex(vertex, (0.0, value - vertex.y))
		self.closeUndoGroup()
		self.refresh()
	
	if usePyObjC:
		
		idField = objc.IBOutlet()
		tabView = objc.IBOutlet()
		vertexXField = objc.IBOutlet()
		vertexYField = objc.IBOutlet()
		lineVertex0Field = objc.IBOutlet()
		lineVertex1Field = objc.IBOutlet()
		lineBlocksPlayersCheckbox = objc.IBOutlet()
		lineBlocksAlliesCheckbox = objc.IBOutlet()
		lineBlocksEnemiesCheckbox = objc.IBOutlet()
		lineBlocksTeamsCheckbox = objc.IBOutlet()
		lineBlocksTeamsPropertiesButton = objc.IBOutlet()
		lineMapVisibilityRadioGroup = objc.IBOutlet()
		lineMapVisibilityPropertiesButton = objc.IBOutlet()
		lineSide0PolygonField = objc.IBOutlet()
		lineSide0BottomDXSlider = objc.IBOutlet()
		lineSide0BottomDYSlider = objc.IBOutlet()
		lineSide0BottomTextureWell = objc.IBOutlet()
		lineSide0BottomLandscapeCheckbox = objc.IBOutlet()
		lineSide0BottomEffectMenu = objc.IBOutlet()
		lineSide0BottomEffectPropertiesButton = objc.IBOutlet()
		lineSide0BottomLightField = objc.IBOutlet()
		lineSide0BottomActionsButton = objc.IBOutlet()
		lineSide0MiddleDXSlider = objc.IBOutlet()
		lineSide0MiddleDYSlider = objc.IBOutlet()
		lineSide0MiddleTextureWell = objc.IBOutlet()
		lineSide0MiddleLandscapeCheckbox = objc.IBOutlet()
		lineSide0MiddleEffectMenu = objc.IBOutlet()
		lineSide0MiddleEffectPropertiesButton = objc.IBOutlet()
		lineSide0MiddleLightField = objc.IBOutlet()
		lineSide0MiddleActionsButton = objc.IBOutlet()
		lineSide0TopDXSlider = objc.IBOutlet()
		lineSide0TopDYSlider = objc.IBOutlet()
		lineSide0TopTextureWell = objc.IBOutlet()
		lineSide0TopLandscapeCheckbox = objc.IBOutlet()
		lineSide0TopEffectMenu = objc.IBOutlet()
		lineSide0TopEffectPropertiesButton = objc.IBOutlet()
		lineSide0TopLightField = objc.IBOutlet()
		lineSide0TopActionsButton = objc.IBOutlet()
		lineSide1PolygonField = objc.IBOutlet()
		lineSide1BottomDXSlider = objc.IBOutlet()
		lineSide1BottomDYSlider = objc.IBOutlet()
		lineSide1BottomTextureWell = objc.IBOutlet()
		lineSide1BottomLandscapeCheckbox = objc.IBOutlet()
		lineSide1BottomEffectMenu = objc.IBOutlet()
		lineSide1BottomEffectPropertiesButton = objc.IBOutlet()
		lineSide1BottomLightField = objc.IBOutlet()
		lineSide1BottomActionsButton = objc.IBOutlet()
		lineSide1MiddleDXSlider = objc.IBOutlet()
		lineSide1MiddleDYSlider = objc.IBOutlet()
		lineSide1MiddleTextureWell = objc.IBOutlet()
		lineSide1MiddleLandscapeCheckbox = objc.IBOutlet()
		lineSide1MiddleEffectMenu = objc.IBOutlet()
		lineSide1MiddleEffectPropertiesButton = objc.IBOutlet()
		lineSide1MiddleLightField = objc.IBOutlet()
		lineSide1MiddleActionsButton = objc.IBOutlet()
		lineSide1TopDXSlider = objc.IBOutlet()
		lineSide1TopDYSlider = objc.IBOutlet()
		lineSide1TopTextureWell = objc.IBOutlet()
		lineSide1TopLandscapeCheckbox = objc.IBOutlet()
		lineSide1TopEffectMenu = objc.IBOutlet()
		lineSide1TopEffectPropertiesButton = objc.IBOutlet()
		lineSide1TopLightField = objc.IBOutlet()
		lineSide1TopActionsButton = objc.IBOutlet()
		polygonTable = objc.IBOutlet()
		polygonLayerMenu = objc.IBOutlet()
		polygonLayerOffsetField = objc.IBOutlet()
		polygonLayerOffsetUnitsField = objc.IBOutlet()
		polygonActionsButton = objc.IBOutlet()
		polygonFloorHeightField = objc.IBOutlet()
		polygonFloorHeightStepper = objc.IBOutlet()
		polygonFloorOffsetField = objc.IBOutlet()
		polygonFloorOffsetStepper = objc.IBOutlet()
		polygonFloorDXSlider = objc.IBOutlet()
		polygonFloorDYSlider = objc.IBOutlet()
		polygonFloorTextureWell = objc.IBOutlet()
		polygonFloorLandscapeCheckbox = objc.IBOutlet()
		polygonFloorEffectMenu = objc.IBOutlet()
		polygonFloorEffectPropertiesButton = objc.IBOutlet()
		polygonFloorLightField = objc.IBOutlet()
		polygonFloorActionsButton = objc.IBOutlet()
		polygonCeilingHeightField = objc.IBOutlet()
		polygonCeilingHeightStepper = objc.IBOutlet()
		polygonCeilingOffsetField = objc.IBOutlet()
		polygonCeilingOffsetStepper = objc.IBOutlet()
		polygonCeilingDXSlider = objc.IBOutlet()
		polygonCeilingDYSlider = objc.IBOutlet()
		polygonCeilingTextureWell = objc.IBOutlet()
		polygonCeilingLandscapeCheckbox = objc.IBOutlet()
		polygonCeilingEffectMenu = objc.IBOutlet()
		polygonCeilingEffectPropertiesButton = objc.IBOutlet()
		polygonCeilingLightField = objc.IBOutlet()
		polygonCeilingActionsButton = objc.IBOutlet()
		
		@traced
		def init(self):
			#self = super(ForgeryInspector, self).initWithWindowNibName_(u'ForgeryInspector')
			self = super(ForgeryInspector, self).init()
			if self:
				if not ForgeryInspector._sharedInspector:
					ForgeryInspector._sharedInspector = self
			return self
		
		@traced
		def awakeFromNib(self):
			self.window().setBecomesKeyOnlyIfNeeded_(True)
		
		@traced
		def windowDidMove_(self, notification):
			self.moved()
		
		@objc.IBAction
		@traced
		def idChanged_(self, sender):
			self.idChanged(sender.stringValue())
		
		@objc.IBAction
		@traced
		def lineSolidChanged_(self, sender):
			self.lineSolidChanged(sender.intValue())
		
		@objc.IBAction
		@traced
		def lineTransparentChanged_(self, sender):
			self.lineTransparentChanged(sender.intValue())
		
		@objc.IBAction
		@traced
		def polygonCeilingHeightChanged_(self, sender):
			self.polygonCeilingHeightChanged(sender.doubleValue())
		
		@objc.IBAction
		@traced
		def polygonCeilingOffsetChanged_(self, sender):
			self.polygonCeilingOffsetChanged(sender.doubleValue())
		
		@objc.IBAction
		@traced
		def polygonFloorHeightChanged_(self, sender):
			self.polygonFloorHeightChanged(sender.doubleValue())
		
		@objc.IBAction
		@traced
		def polygonFloorOffsetChanged_(self, sender):
			self.polygonFloorOffsetChanged(sender.doubleValue())
		
		@objc.IBAction
		@traced
		def polygonLayerChanged_(self, sender):
			self.polygonLayerChanged(sender.titleOfSelectedItem())
		
		@objc.IBAction
		@traced
		def surfaceActionPropertiesClicked_(self, sender):
			if sender.tag() == ID.ACTION_SWITCH:
				surface = self.findSurfaceForUI(sender, 'switchPropertiesButton')
				action = 'switch'
			elif sender.tag() == ID.ACTION_TERMINAL:
				surface = self.findSurfaceForUI(sender, 'terminalPropertiesButton')
				action = 'terminal'
			elif sender.tag() == ID.ACTION_RECHARGER:
				surface = self.findSurfaceForUI(sender, 'rechargerPropertiesButton')
				action = 'recharger'
			self.surfaceActionPropertiesClicked(surface, action)
		
		@objc.IBAction
		@traced
		def surfaceActionToggled_(self, sender):
			if sender.tag() == ID.ACTION_SWITCH:
				surface = self.findSurfaceForUI(sender, 'switchCheckbox')
				action = 'switch'
			elif sender.tag() == ID.ACTION_PATTERN_BUFFER:
				surface = self.findSurfaceForUI(sender, 'patternBufferCheckbox')
				action = 'pattern buffer'
			elif sender.tag() == ID.ACTION_TERMINAL:
				surface = self.findSurfaceForUI(sender, 'terminalCheckbox')
				action = 'terminal'
			elif sender.tag() == ID.ACTION_RECHARGER:
				surface = self.findSurfaceForUI(sender, 'rechargerCheckbox')
				action = 'recharger'
			self.surfaceActionToggled(surface, action, sender.state())
		
		@objc.IBAction
		@traced
		def surfaceDXChanged_(self, sender):
			surface = self.findSurfaceForUI(sender, 'dxSlider')
			self.surfaceDXChanged(surface, sender.doubleValue())
		
		@objc.IBAction
		@traced
		def surfaceDYChanged_(self, sender):
			surface = self.findSurfaceForUI(sender, 'dySlider')
			self.surfaceDYChanged(surface, sender.doubleValue())
		
		@objc.IBAction
		@traced
		def surfaceEffectChanged_(self, sender):
			surface = self.findSurfaceForUI(sender, 'effectMenu')
			if sender.selectedItem().tag() == ID.EFFECT_PULSATE:
				effect = 'pulsate'
			elif sender.selectedItem().tag() == ID.EFFECT_WOBBLE:
				effect = 'wobble'
			elif sender.selectedItem().tag() == ID.EFFECT_SLIDE:
				effect = 'slide'
			elif sender.selectedItem().tag() == ID.EFFECT_WANDER:
				effect = 'wander'
			elif sender.selectedItem().tag() == ID.EFFECT_NORMAL:
				effect = None
			self.surfaceEffectChanged(surface, effect)
		
		@objc.IBAction
		@traced
		def surfaceEffectPropertiesClicked_(self, sender):
			surface = self.findSurfaceForUI(sender, 'effectPropertiesButton')
			# FIXME
			effect = None
			self.surfaceEffectPropertiesClicked(surface, effect)
		
		@objc.IBAction
		@traced
		def surfaceLandscapeChanged_(self, sender):
			surface = self.findSurfaceForUI(sender, 'landscapeCheckbox')
			self.surfaceLandscapeChanged(surface, sender.state())
		
		@objc.IBAction
		@traced
		def surfaceLightChanged_(self, sender):
			surface = self.findSurfaceForUI(sender, 'lightField')
			self.surfaceLightChanged(surface, sender.stringValue())
		
		@objc.IBAction
		@traced
		def vertexXChanged_(self, sender):
			self.vertexXChanged(sender.doubleValue())
		
		@objc.IBAction
		@traced
		def vertexYChanged_(self, sender):
			self.vertexYChanged(sender.doubleValue())
		
	else:
		
		sizer = property(
			fget = lambda self: self.GetSizer(),
			fset = lambda self, value: self.SetSizer(value),
		)
		idField = None
		tabView = None
		vertexXField = None
		vertexYField = None
		lineVertex0Field = None
		lineVertex1Field = None
		lineBlocksPlayersCheckbox = None
		lineBlocksAlliesCheckbox = None
		lineBlocksEnemiesCheckbox = None
		lineBlocksTeamsCheckbox = None
		lineBlocksTeamsPropertiesButton = None
		lineMapVisibilityRadioGroup = None
		lineMapVisibilityPropertiesButton = None
		lineSide0PolygonField = None
		lineSide0BottomDXSlider = None
		lineSide0BottomDYSlider = None
		lineSide0BottomTextureWell = None
		lineSide0BottomLandscapeCheckbox = None
		lineSide0BottomEffectMenu = None
		lineSide0BottomEffectPropertiesButton = None
		lineSide0BottomLightField = None
		lineSide0BottomActionsButton = None
		lineSide0MiddleDXSlider = None
		lineSide0MiddleDYSlider = None
		lineSide0MiddleTextureWell = None
		lineSide0MiddleLandscapeCheckbox = None
		lineSide0MiddleEffectMenu = None
		lineSide0MiddleEffectPropertiesButton = None
		lineSide0MiddleLightField = None
		lineSide0MiddleActionsButton = None
		lineSide0TopDXSlider = None
		lineSide0TopDYSlider = None
		lineSide0TopTextureWell = None
		lineSide0TopLandscapeCheckbox = None
		lineSide0TopEffectMenu = None
		lineSide0TopEffectPropertiesButton = None
		lineSide0TopLightField = None
		lineSide0TopActionsButton = None
		lineSide1PolygonField = None
		lineSide1BottomDXSlider = None
		lineSide1BottomDYSlider = None
		lineSide1BottomTextureWell = None
		lineSide1BottomLandscapeCheckbox = None
		lineSide1BottomEffectMenu = None
		lineSide1BottomEffectPropertiesButton = None
		lineSide1BottomLightField = None
		lineSide1BottomActionsButton = None
		lineSide1MiddleDXSlider = None
		lineSide1MiddleDYSlider = None
		lineSide1MiddleTextureWell = None
		lineSide1MiddleLandscapeCheckbox = None
		lineSide1MiddleEffectMenu = None
		lineSide1MiddleEffectPropertiesButton = None
		lineSide1MiddleLightField = None
		lineSide1MiddleActionsButton = None
		lineSide1TopDXSlider = None
		lineSide1TopDYSlider = None
		lineSide1TopTextureWell = None
		lineSide1TopLandscapeCheckbox = None
		lineSide1TopEffectMenu = None
		lineSide1TopEffectPropertiesButton = None
		lineSide1TopLightField = None
		lineSide1TopActionsButton = None
		polygonTable = None
		polygonLayerMenu = None
		polygonLayerOffsetField = None
		polygonLayerOffsetUnitsField = None
		polygonActionsButton = None
		polygonFloorHeightField = None
		polygonFloorHeightStepper = None
		polygonFloorOffsetField = None
		polygonFloorOffsetStepper = None
		polygonFloorDXSlider = None
		polygonFloorDYSlider = None
		polygonFloorTextureWell = None
		polygonFloorLandscapeCheckbox = None
		polygonFloorEffectMenu = None
		polygonFloorEffectPropertiesButton = None
		polygonFloorLightField = None
		polygonFloorActionsButton = None
		polygonCeilingHeightField = None
		polygonCeilingHeightStepper = None
		polygonCeilingOffsetField = None
		polygonCeilingOffsetStepper = None
		polygonCeilingDXSlider = None
		polygonCeilingDYSlider = None
		polygonCeilingTextureWell = None
		polygonCeilingLandscapeCheckbox = None
		polygonCeilingEffectMenu = None
		polygonCeilingEffectPropertiesButton = None
		polygonCeilingLightField = None
		polygonCeilingActionsButton = None
		
		def __init__(self):
			super(ForgeryInspector, self).__init__(
				None,
				style = wx.STAY_ON_TOP | wx.CAPTION | wx.CLOSE_BOX,
			)
			self.Bind(wx.EVT_CLOSE, errorWrap(self.OnClose))
			self.Bind(wx.EVT_MOVE, errorWrap(self.OnMoved))
			self.BuildUI()
			self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
		
		def BuildUI(self):
			self.idField = createTextCtrl(self, self.OnIDChanged)
			self.tabView = TablessNotebook()
			self.tabView[ID.NO_SELECTION] = self.BuildNoSelectionUI()
			self.tabView[ID.MULTIPLE_SELECTION] = self.BuildMultipleSelectionUI()
			self.tabView[ID.VERTEX] = self.BuildVertexUI()
			self.tabView[ID.LINE] = self.BuildLineUI()
			self.tabView[ID.POLYGON] = self.BuildPolygonUI()
			self.tabView[ID.OBJECT] = self.BuildObjectUI()
			self.tabView[ID.SOUND] = self.BuildSoundUI()
			# The numbers come from Apple's HIG
			self.sizer = buildSizers(
				wx.VERTICAL,
				10,
				(
					10,
					(
						(
							None,
							createRightAlignedStaticText(self, "ID:"),
							8,
							self.idField,
							None,
						),
						8,
						self.tabView,
					),
					10,
				),
				12,
			)
			self.sizer.Layout()
			self.sizer.Fit(self)
			self.update()
		
		def BuildNoSelectionUI(self):
			result = wx.Panel(self, -1)
			sizer = createCenteredText(
				result,
				u"Nothing Selected",
			)
			result.SetSizer(sizer)
			sizer.Layout()
			sizer.Fit(result)
			return result
		
		def BuildMultipleSelectionUI(self):
			result = wx.Panel(self, -1)
			sizer = createCenteredText(
				result,
				u"Multiple Objects Selected",
			)
			result.SetSizer(sizer)
			sizer.Layout()
			sizer.Fit(result)
			return result
		
		def BuildVertexUI(self):
			result = wx.Panel(self, -1)
			self.vertexXField = createTextCtrl(
				result,
				self.OnVertexXChanged,
			)
			self.vertexYField = createTextCtrl(
				result,
				self.OnVertexYChanged,
			)
			vertexUI = self.vertex
			sizer = buildNonuniformGrid(
				2,
				createRightAlignedStaticText(result, u"X:"),
				vertexUI['xField'],
				createRightAlignedStaticText(result, u"Y:"),
				vertexUI['yField'],
			)
			result.SetSizer(sizer)
			sizer.Layout()
			sizer.Fit(result)
			return result
		
		def BuildLineUI(self):
			result = wx.Panel(self, -1)
			self.lineVertex0Field = createTextCtrl(result)
			self.lineVertex1Field = createTextCtrl(result)
			self.lineSolidCheckbox = createCheckbox(
				result,
				u"Solid",
				self.OnLineSolidChanged,
			)
			self.lineTransparentCheckbox = createCheckbox(
				result,
				u"Transparent",
				self.OnLineTransparentChanged,
			)
			notebook = wx.Notebook(result, -1, style = wx.BK_TOP)
			notebook.AddPage(
				self.BuildSideUI(
					notebook,
					'lineSide0',
					('line', 'side', 0),
				),
				u"First Side",
			)
			notebook.AddPage(
				self.BuildSideUI(
					notebook,
					'lineSide1',
					('line', 'side', 1),
				),
				u"Second Side",
			)
			lineUI = self.line
			lineUI['vertex0Field'].Disable()
			lineUI['vertex1Field'].Disable()
			sizer = buildSizers(
				wx.VERTICAL,
				buildNonuniformGrid(
					2,
					createRightAlignedStaticText(result, u"First Vertex:"),
					lineUI['vertex0Field'],
					createRightAlignedStaticText(result, u"Second Vertex:"),
					lineUI['vertex1Field'],
					None,
					lineUI['solidCheckbox'],
					None,
					lineUI['transparentCheckbox'],
				),
				notebook,
			)
			result.SetSizer(sizer)
			sizer.Layout()
			sizer.Fit(result)
			return result
		
		def BuildPolygonUI(self):
			result = wx.Panel(self, -1)
			self.polygonTable = createPolygonTable(
				result,
				# self.OnPolygonTableDoubleClicked,
			)
			self.polygonLayerMenu = createPopupMenu(
				result,
				(),
				self.OnPolygonLayerChanged,
			)
			self.polygonLayerOffsetField = createStaticText(result, u"0.00", 0)
			self.polygonLayerOffsetUnitsField = createStaticText(result, u"WU", 0)
			notebook = wx.Notebook(result, -1, style = wx.BK_TOP)
			notebook.AddPage(
				self.BuildSurfaceUI(
					notebook,
					'polygonFloor',
					('polygon', 'floor'),
				),
				u"Floor",
			)
			notebook.AddPage(
				self.BuildSurfaceUI(
					notebook,
					'polygonCeiling',
					('polygon', 'ceiling'),
				),
				u"Ceiling",
			)
			polygonUI = self.polygon
			layerUI = polygonUI['layer']
			sizer = buildSizers(
				wx.VERTICAL,
				polygonUI['table'],
				8,
				(
					layerUI['menu'],
					8,
					layerUI['offsetField'],
					8,
					layerUI['offsetUnitsField'],
				),
				notebook,
			)
			result.SetSizer(sizer)
			sizer.Layout()
			sizer.Fit(result)
			return result
		
		def BuildObjectUI(self):
			# FIXME
			return None
		
		def BuildSoundUI(self):
			# FIXME
			return None
		
		def BuildSideUI(self, parent, prefix, path):
			result = wx.Panel(parent, -1)
			self.setAttribute(prefix, 'PolygonField', createTextCtrl(result))
			self.getPath(path)['polygonField'].Disable()
			notebook = wx.Notebook(result, -1, style = wx.BK_LEFT)
			notebook.AddPage(
				self.BuildSurfaceUI(
					notebook,
					prefix + 'Top',
					path + ('top', ),
				),
				u"Top",
			)
			notebook.AddPage(
				self.BuildSurfaceUI(
					notebook,
					prefix + 'Middle',
					path + ('middle', ),
				),
				u"Middle",
			)
			notebook.AddPage(
				self.BuildSurfaceUI(
					notebook,
					prefix + 'Bottom',
					path + ('bottom', ),
				),
				u"Bottom",
			)
			sideUI = self.getPath(path)
			sizer = buildSizers(
				wx.HORIZONTAL,
				8,
				(
					8,
					(
						createRightAlignedStaticText(result, u"Polygon:"),
						8,
						sideUI['polygonField'],
					),
					8,
					notebook,
					8,
				),
				8,
			)
			result.SetSizer(sizer)
			sizer.Layout()
			sizer.Fit(result)
			return result
		
		def BuildSurfaceUI(self, parent, prefix, path):
			result = wx.Panel(parent, -1)
			if prefix.startswith('polygon'):
				self.setAttribute(prefix, 'HeightField', createSpinCtrl(
					result,
					getattr(self, 'On' + capitalize(prefix) + 'HeightChanged'),
				))
				self.setAttribute(prefix, 'OffsetField', createSpinCtrl(
					result,
					getattr(self, 'On' + capitalize(prefix) + 'OffsetChanged'),
				))
			self.setAttribute(prefix, 'DXSlider', createSlider(
				result,
				0, 127, 9,
				wx.SL_HORIZONTAL | wx.SL_BOTTOM | wx.SL_AUTOTICKS,
				self.OnSurfaceDXChanged,
			))
			self.setAttribute(prefix, 'DYSlider', createSlider(
				result,
				0, 127, 9,
				wx.SL_VERTICAL | wx.SL_LEFT | wx.SL_AUTOTICKS,
				self.OnSurfaceDYChanged,
			))
			self.setAttribute(prefix, 'EffectMenu', createPopupMenu(
				result,
				(
					u"Normal",
					u"Pulsate",
					u"Slide",
					u"Wander",
					u"Wobble",
				),
				self.OnSurfaceEffectChanged,
			))
			self.setAttribute(prefix, 'EffectPropertiesButton', createPropertiesButton(
				result,
				self.OnSurfaceEffectPropertiesClicked,
			))
			self.setAttribute(prefix, 'LandscapeCheckbox', createCheckbox(
				result,
				u"Landscape",
				self.OnSurfaceLandscapeChanged,
			))
			self.setAttribute(prefix, 'LightField', createTextCtrl(
				result,
				self.OnSurfaceLightChanged,
			))
			self.setAttribute(prefix, 'PatternBufferCheckbox', createCheckbox(
				result,
				u"Pattern Buffer",
				self.OnSurfaceActionToggled,
			))
			self.setAttribute(prefix, 'RechargerCheckbox', createCheckbox(
				result,
				u"Recharger",
				self.OnSurfaceActionToggled,
			))
			self.setAttribute(prefix, 'RechargerPropertiesButton', createPropertiesButton(
				result,
				self.OnSurfaceActionPropertiesClicked,
			))
			self.setAttribute(prefix, 'SwitchCheckbox', createCheckbox(
				result,
				u"Switch",
				self.OnSurfaceActionToggled,
			))
			self.setAttribute(prefix, 'SwitchPropertiesButton', createPropertiesButton(
				result,
				self.OnSurfaceActionPropertiesClicked,
			))
			self.setAttribute(prefix, 'TerminalCheckbox', createCheckbox(
				result,
				u"Terminal",
				self.OnSurfaceActionToggled,
			))
			self.setAttribute(prefix, 'TerminalPropertiesButton', createPropertiesButton(
				result,
				self.OnSurfaceActionPropertiesClicked,
			))
			self.setAttribute(prefix, 'TextureWell', createTextureWell(
				result,
				ForgeryElements.ForgerySurface(None, None, ForgeryElements.ForgeryTexture('')).image, # this will be replaced when update() is called
				# self.OnSurfaceTextureChanged,
			))
			surfaceUI = self.getPath(path)
			sizers = [
				20,
				[
					20,
					buildNonuniformGrid(
						3,
						
						surfaceUI['dySlider'],
						surfaceUI['textureWell'],
						None,
						
						None,
						surfaceUI['dxSlider'],
						None,
						
						None,
						surfaceUI['landscapeCheckbox'],
						None,
						
						createRightAlignedStaticText(result, u"Effect:"),
						surfaceUI['effectMenu'],
						surfaceUI['effectPropertiesButton'],
						
						createRightAlignedStaticText(result, u"Light:"),
						surfaceUI['lightField'],
						None,
					),
					buildNonuniformGrid(
						5,
						
						surfaceUI['switchCheckbox'],
						surfaceUI['switchPropertiesButton'],
						None,
						surfaceUI['patternBufferCheckbox'],
						None,
						
						surfaceUI['terminalCheckbox'],
						surfaceUI['terminalPropertiesButton'],
						None,
						surfaceUI['rechargerCheckbox'],
						surfaceUI['rechargerPropertiesButton'],
					),
					20,
				],
				20,
			]
			if path[0] == 'polygon':
				sizers[1].insert(1, (
					createRightAlignedStaticText(result, u"Height:"),
					8,
					surfaceUI['heightField'],
					None,
					createRightAlignedStaticText(result, u"Offset:"),
					8,
					surfaceUI['offsetField'],
				))
			sizer = buildSizers(
				wx.HORIZONTAL,
				*sizers
			)
			result.SetSizer(sizer)
			sizer.Layout()
			sizer.Fit(result)
			return result
		
		def OnIDChanged(self, event):
			self.idChanged(event.GetEventObject().GetValue())
		
		def OnLineSolidChanged(self, event):
			self.lineSolidChanged(event.GetEventObject().GetValue())
		
		def OnLineTransparentChanged(self, event):
			self.lineTransparentChanged(event.GetEventObject().GetValue())
		
		def OnPolygonCeilingHeightChanged(self, event):
			self.polygonCeilingHeightChanged(event.GetEventObject().GetValue())
		
		def OnPolygonCeilingOffsetChanged(self, event):
			self.polygonCeilingOffsetChanged(event.GetEventObject().GetValue())
		
		def OnPolygonFloorHeightChanged(self, event):
			self.polygonFloorHeightChanged(event.GetEventObject().GetValue())
		
		def OnPolygonFloorOffsetChanged(self, event):
			self.polygonFloorOffsetChanged(event.GetEventObject().GetValue())
		
		def OnPolygonLayerChanged(self, event):
			self.polygonLayerChanged(event.GetEventObject().GetStringSelection())
		
		def OnSurfaceActionPropertiesClicked(self, event):
			print "%s.OnSurfaceActionPropertiesClicked(%s)" % (self, event)
			#if sender.tag() == ID.ACTION_SWITCH:
			#	surface = self.findSurfaceForUI(sender, 'switchPropertiesButton')
			#	action = 'switch'
			#elif sender.tag() == ID.ACTION_TERMINAL:
			#	surface = self.findSurfaceForUI(sender, 'terminalPropertiesButton')
			#	action = 'terminal'
			#elif sender.tag() == ID.ACTION_RECHARGER:
			#	surface = self.findSurfaceForUI(sender, 'rechargerPropertiesButton')
			#	action = 'recharger'
			#self.surfaceActionPropertiesClicked(surface, action)
		
		def OnSurfaceActionToggled(self, event):
			print "%s.OnSurfaceActionToggled(%s)" % (self, event)
			#if sender.tag() == ID.ACTION_SWITCH:
			#	surface = self.findSurfaceForUI(sender, 'switchCheckbox')
			#	action = 'switch'
			#elif sender.tag() == ID.ACTION_PATTERN_BUFFER:
			#	surface = self.findSurfaceForUI(sender, 'patternBufferCheckbox')
			#	action = 'pattern buffer'
			#elif sender.tag() == ID.ACTION_TERMINAL:
			#	surface = self.findSurfaceForUI(sender, 'terminalCheckbox')
			#	action = 'terminal'
			#elif sender.tag() == ID.ACTION_RECHARGER:
			#	surface = self.findSurfaceForUI(sender, 'rechargerCheckbox')
			#	action = 'recharger'
			#self.surfaceActionToggled(surface, action, sender.state())
		
		def OnSurfaceDXChanged(self, event):
			surface = self.findSurfaceForUI(event.GetEventObject(), 'dxSlider')
			self.surfaceDXChanged(surface, event.GetEventObject().GetValue())
		
		def OnSurfaceDYChanged(self, event):
			surface = self.findSurfaceForUI(event.GetEventObject(), 'dySlider')
			self.surfaceDYChanged(surface, event.GetEventObject().GetValue())
		
		def OnSurfaceEffectChanged(self, event):
			print "%s.OnSurfaceEffectChanged(%s)" % (self, event)
			surface = self.findSurfaceForUI(event.GetEventObject(), 'effectMenu')
			#if sender.selectedItem().tag() == ID.EFFECT_PULSATE:
			#	effect = 'pulsate'
			#elif sender.selectedItem().tag() == ID.EFFECT_WOBBLE:
			#	effect = 'wobble'
			#elif sender.selectedItem().tag() == ID.EFFECT_SLIDE:
			#	effect = 'slide'
			#elif sender.selectedItem().tag() == ID.EFFECT_WANDER:
			#	effect = 'wander'
			#elif sender.selectedItem().tag() == ID.EFFECT_NORMAL:
			#	effect = None
			#self.surfaceEffectChanged(surface, effect)
		
		def OnSurfaceEffectPropertiesClicked(self, event):
			print "%s.OnSurfaceEffectPropertiesClicked(%s)" % (self, event)
			surface = self.findSurfaceForUI(event.GetEventObject(), 'effectPropertiesButton')
			# FIXME
			effect = None
			self.surfaceEffectPropertiesClicked(surface, effect)
		
		def OnSurfaceLandscapeChanged(self, event):
			surface = self.findSurfaceForUI(event.GetEventObject(), 'landscapeCheckbox')
			self.surfaceLandscapeChanged(surface, event.GetEventObject().GetValue())
		
		def OnSurfaceLightChanged(self, event):
			surface = self.findSurfaceForUI(event.GetEventObject(), 'lightField')
			self.surfaceLightChanged(surface, event.GetEventObject().GetValue())
		
		def OnVertexXChanged(self, event):
			try:
				value = float(event.GetEventObject().GetValue())
			except ValueError:
				# FIXME: beep
				self.update()
			else:
				self.vertexXChanged(value)
		
		def OnVertexYChanged(self, event):
			try:
				value = float(event.GetEventObject().GetValue())
			except ValueError:
				# FIXME: beep
				self.update()
			else:
				self.vertexYChanged(value)
		
		def OnClose(self, event):
			if event.CanVeto() and self.IsShown():
				self.hide()
				event.Veto()
			else:
				self.Destroy()
		
		def OnMoved(self, event):
			self.moved()

def sharedInspector():
	return ForgeryInspector.sharedInspector()

if not usePyObjC:
	
	def createStaticText(parent, label, style):
		result = wx.StaticText(
			parent, -1,
			label = label,
			style = style,
		)
		return result
	
	def addStaticText(sizer, parent, label, style):
		result = createStaticText(parent, label, style)
		sizer.Add(result)
		return result
	
	def createCenteredStaticText(parent, label):
		return createStaticText(parent, label, wx.ALIGN_CENTER)
	
	def addCenteredStaticText(sizer, parent, label):
		return addStaticText(sizer, parent, label, wx.ALIGN_CENTER)
	
	def createRightAlignedStaticText(parent, label):
		return createStaticText(parent, label, wx.ALIGN_RIGHT)
	
	def addRightAlignedStaticText(sizer, parent, label):
		return addStaticText(sizer, parent, label, wx.ALIGN_RIGHT)
	
	def createTextCtrl(parent, func = None):
		result = wx.TextCtrl(
			parent, -1,
			style = wx.TE_PROCESS_ENTER,
		)
		if func:
			result.Bind(wx.EVT_TEXT, errorWrap(func))
			result.Bind(wx.EVT_TEXT_ENTER, errorWrap(func))
		return result
	
	def addTextCtrl(sizer, parent, func = None):
		result = createTextCtrl(parent, func)
		sizer.Add(result)
		return result
	
	def createCenteredText(parent, text):
		return buildSizers(
			wx.VERTICAL,
			#None,
			createCenteredStaticText(parent, text),
			#None,
		)
	
	def createCheckbox(parent, label, func = None):
		result = wx.CheckBox(
			parent, -1,
			label,
		)
		if func:
			result.Bind(wx.EVT_CHECKBOX, errorWrap(func))
		return result
	
	def createSlider(parent, minValue, maxValue, ticks = None, style = 0, func = None):
		if style & wx.SL_VERTICAL:
			size = wx.Size(16, maxValue - minValue + 1)
			style |= wx.SL_INVERSE
		else:
			size = wx.Size(maxValue - minValue + 1, 16)
		result = wx.Slider(
			parent, -1,
			value = int((minValue + maxValue) / 2),
			minValue = minValue,
			maxValue = maxValue,
			size = size,
			style = style,
		)
		if ticks:
			tickFreq = (maxValue - minValue + 1) / (ticks - 1)
			result.SetTickFreq(int(tickFreq), 1)
		if func:
			result.Bind(wx.EVT_SCROLL, errorWrap(func))
		return result
	
	def createTextureWell(parent, bitmap, func = None):
		result = wx.BitmapButton(
			parent, -1,
			bitmap,
		)
		# FIXME: Clicking the button should bring up a texture selector
		if func:
			result.Bind(wx.EVT_BUTTON, errorWrap(func))
		return result
	
	def createPropertiesButton(parent, func = None):
		result = wx.BitmapButton(
			parent, -1,
			wx.Bitmap(os.path.join(resourcesDir, 'info.tiff')),
			style = wx.NO_BORDER,
		)
		if func:
			result.Bind(wx.EVT_BUTTON, errorWrap(func))
		return result
	
	def createPolygonTable(parent):
		result = wx.grid.Grid(parent, -1)
		result.CreateGrid(4, 2)
		result.BeginBatch()
		result.EnableEditing(False)
		result.SetColLabelValue(0, "Vertices")
		result.SetColLabelValue(1, "Lines")
		result.SetRowLabelSize(0)
		result.SetColLabelSize(15)
		result.EndBatch()
		return result
	
	def createPopupMenu(parent, items = (), func = None):
		result = wx.Choice(
			parent, -1,
			wx.DefaultPosition,
			wx.DefaultSize,
			items,
		)
		if func:
			result.Bind(wx.EVT_CHOICE, errorWrap(func))
		return result
	
	def createSpinCtrl(parent, func = None):
		result = wx.SpinCtrl(
			parent, -1,
		)
		if func:
			result.Bind(wx.EVT_SPINCTRL, errorWrap(func))
		return result
	
	class TablessNotebook(wx.PySizer):
		pages = None
		currentPage = None
		
		def __init__(self):
			self.pages = {}
			super(TablessNotebook, self).__init__()
		
		def CalcMin(self):
			w, h = 0, 0
			for page in self.itervalues():
				pageSize = page.GetMinSize()
				if pageSize == wx.DefaultSize:
					pageSize = page.GetSize()
				if pageSize.width > w:
					w = pageSize.width
				if pageSize.height > h:
					h = pageSize.height
			return wx.Size(w, h)
		
		def RecalcSizes(self):
			size = self.GetSize()
			position = self.GetPosition()
			for page in self.itervalues():
				page.SetSize(size)
				page.SetPosition(position)
		
		def ActivePage(self):
			return self.currentPage
		
		def SetActivePage(self, key):
			for page in self.itervalues():
				page.Hide()
			self.Clear()
			self[key].Show()
			self.Add(self[key])
		
		def __setitem__(self, key, value):
			if self.get(key) != value:
				try:
					del self[key]
				except KeyError:
					pass
				if value:
					self.pages.__setitem__(key, value)
			if len(self) == 1 or self.ActivePage() not in self:
				self.SetActivePage(self.keys()[0])
			elif not self:
				self.SetActivePage(None)
		
		def __getitem__(self, key):
			return self.pages.__getitem__(key)
		
		def __delitem__(self, key):
			self[key].Destroy()
			return self.pages.__delitem__(key)
		
		def __contains__(self, key):
			return self.pages.__contains__(key)
		
		def __iter__(self):
			return self.pages.__iter__()
		
		def __len__(self):
			return self.pages.__len__()
		
		def get(self, key, default = None):
			return self.pages.get(key, default)
		
		def iterkeys(self):
			return self.pages.iterkeys()
		
		def keys(self):
			return self.pages.keys()
		
		def itervalues(self):
			return self.pages.itervalues()
		
		def values(self):
			return self.pages.values()
		
		def iteritems(self):
			return self.pages.iteritems()
		
		def items(self):
			return self.pages.items()
	
	#class TablessNotebook(wx.BookCtrlBase):
	#	def Init(self):
	#		self.m_selection = wx.NOT_FOUND
	#	
	#	def SetSelection(self, n):
	#		return self.DoSetSelection(n, self.SetSelection_SendEvent)
	#	
	#	def ChangeSelection(self, n):
	#		return self.DoSetSelection(n)
	#	
	#	def GetControllerSize(self):
	#		return wx.Size()
	#	
	#	def HitTest(self, pt):
	#		pagePos = wx.NOT_FOUND
	#		flags = wx.BK_HITTEST_NOWHERE
	#		if self.GetPageRect().Contains(pt):
	#			flags |= wx.BK_HITTEST_ONPAGE
	#		return pagePos, flags
	#	
	#	def CalcSizeFromPage(self, sizePage):
	#		return sizePage
	#	
	#	def UpdateSelectedPage(self, newsel):
	#		self.m_selection = newsel
	#	
	#	def GetSelection(self):
	#		return self.m_selection
	#	
	#	def CreatePageChangingEvent(self):
	#		return wx.NotebookEvent(wx.EVT_COMMAND_NOTEBOOK_PAGE_CHANGING, self.m_windowId)
	#	
	#	def MakeChangedEvent(self, event):
	#		event.SetEventType(wx.EVT_COMMAND_NOTEBOOK_PAGE_CHANGED)
	#	
	#	def InsertPage(self, n, page, bSelect = False):
	#		if not super(TablessNotebook, self).InsertPage(n, page, wx.EmptyString, bSelect, -1):
	#			return False
	#		if int(n) <= self.m_selection:
	#			self.m_selection += 1
	#		selNew = -1
	#		if bSelect:
	#			selNew = n
	#		elif self.m_selection == -1:
	#			selNew = 0
	#		if selNew != self.m_selection:
	#			page.Hide()
	#		if selNew != -1:
	#			self.SetSelection(selNew)
	#		if self.GetPageCount() == 1:
	#			sz = wx.SizeEvent(self.GetSize(), self.GetId())
	#			self.GetEventHandler().ProcessEvent(sz)
	#		return True
	#	
	#	def DoRemovePage(self, page):
	#		page_count = self.GetPageCount()
	#		win = super(TablessNotebook, self).DoRemovePage(page)
	#		if win:
	#			if self.m_selection >= int(page):
	#				sel = self.m_selection - 1
	#				if page_count == 1:
	#					sel = wx.NOT_FOUND
	#				elif page_count == 2 or sel == -1:
	#					sel = 0
	#				if self.m_selection == int(page):
	#					self.m_selection = wx.NOT_FOUND
	#				else:
	#					self.m_selection -= 1
	#				if sel != wx.NOT_FOUND and sel != m_selection:
	#					self.SetSelection(sel)
	#			if self.GetPageCount() == 0:
	#				sz = wx.SizeEvent(self.GetSize(), self.GetId())
	#				self.GetEventHandler().ProcessEvent(sz)
	#		return win
	#	
	#	def DeleteAllPages(self):
	#		if not super(TablessNotebook, self).DeleteAllPages():
	#			return False
	#		self.m_selection = -1
	#		sz = wx.SizeEvent(self.GetSize(), self.GetId())
	#		self.GetEventHandler().ProcessEvent(sz)
	#		return True
