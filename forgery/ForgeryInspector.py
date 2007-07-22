# ForgeryInspector.py
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
	'ForgeryInspector',
	'sharedInspector',
)

import ForgeryApplication, ForgeryElements, ForgeryPreferences

if usePyObjC:
	
	from PyObjCTools import NibClassBuilder
	from Foundation import *
	from AppKit import *
	
	Superclass = NibClassBuilder.AutoBaseClass
	
else:
	
	import wx
	import os
	
	Superclass = wx.MiniFrame

class ForgeryInspector(Superclass):
	_sharedInspector = None
	
	app = property(fget = lambda self: ForgeryApplication.sharedApplication())
	document = property(fget = lambda self: self.app.frontDocument)
	preferences = property(fget = lambda self: self.document and self.document.preferences or self.app.preferences)
	
	isDocked = property(
		fget = lambda self: getattr(self.preferences, 'inspectorIsDocked'),
		fset = lambda self, value: setattr(self.preferences, 'inspectorIsDocked', value),
	)
	position = property(
		fget = lambda self: getattr(self.preferences, 'inspectorPosition'),
		fset = lambda self, value: setattr(self.preferences, 'inspectorPosition', value),
	)
	isVisible = property(
		fget = lambda self: getattr(self.preferences, 'inspectorIsVisible'),
		fset = lambda self, value: setattr(self.preferences, 'inspectorIsVisible', value),
	)
	
	data = property(fget = lambda self: self.document and self.document.data)
	mode = property(fget = lambda self: self.document and self.document.currentMode)
	tool = property(fget = lambda self: self.mode and getattr(self.mode, 'currentTool', None))
	selection = property(fget = lambda self: self.tool and getattr(self.tool, 'selection', ()))
	selectedElement = property(fget = lambda self: tuple(self.selection)[0]) # sets cannot be indexed
	
	vertex = property(fget = lambda self: {
		'xField': self.vertexXField,
		'yField': self.vertexYField,
	})
	
	line = property(fget = lambda self: {
		'vertex0Field': self.lineVertex0Field,
		'vertex1Field': self.lineVertex1Field,
		'solidCheckbox': self.lineSolidCheckbox,
		'transparentCheckbox': self.lineTransparentCheckbox,
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
					'switchCheckbox': self.lineSide0BottomSwitchCheckbox,
					'switchPropertiesButton': self.lineSide0BottomSwitchPropertiesButton,
					'patternBufferCheckbox': self.lineSide0BottomPatternBufferCheckbox,
					'terminalCheckbox': self.lineSide0BottomTerminalCheckbox,
					'terminalPropertiesButton': self.lineSide0BottomTerminalPropertiesButton,
					'rechargerCheckbox': self.lineSide0BottomRechargerCheckbox,
					'rechargerPropertiesButton': self.lineSide0BottomRechargerPropertiesButton,
				},
				'middle': {
					'dxSlider': self.lineSide0MiddleDXSlider,
					'dySlider': self.lineSide0MiddleDYSlider,
					'textureWell': self.lineSide0MiddleTextureWell,
					'landscapeCheckbox': self.lineSide0MiddleLandscapeCheckbox,
					'effectMenu': self.lineSide0MiddleEffectMenu,
					'effectPropertiesButton': self.lineSide0MiddleEffectPropertiesButton,
					'lightField': self.lineSide0MiddleLightField,
					'switchCheckbox': self.lineSide0MiddleSwitchCheckbox,
					'switchPropertiesButton': self.lineSide0MiddleSwitchPropertiesButton,
					'patternBufferCheckbox': self.lineSide0MiddlePatternBufferCheckbox,
					'terminalCheckbox': self.lineSide0MiddleTerminalCheckbox,
					'terminalPropertiesButton': self.lineSide0MiddleTerminalPropertiesButton,
					'rechargerCheckbox': self.lineSide0MiddleRechargerCheckbox,
					'rechargerPropertiesButton': self.lineSide0MiddleRechargerPropertiesButton,
				},
				'top': {
					'dxSlider': self.lineSide0TopDXSlider,
					'dySlider': self.lineSide0TopDYSlider,
					'textureWell': self.lineSide0TopTextureWell,
					'landscapeCheckbox': self.lineSide0TopLandscapeCheckbox,
					'effectMenu': self.lineSide0TopEffectMenu,
					'effectPropertiesButton': self.lineSide0TopEffectPropertiesButton,
					'lightField': self.lineSide0TopLightField,
					'switchCheckbox': self.lineSide0TopSwitchCheckbox,
					'switchPropertiesButton': self.lineSide0TopSwitchPropertiesButton,
					'patternBufferCheckbox': self.lineSide0TopPatternBufferCheckbox,
					'terminalCheckbox': self.lineSide0TopTerminalCheckbox,
					'terminalPropertiesButton': self.lineSide0TopTerminalPropertiesButton,
					'rechargerCheckbox': self.lineSide0TopRechargerCheckbox,
					'rechargerPropertiesButton': self.lineSide0TopRechargerPropertiesButton,
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
					'switchCheckbox': self.lineSide1BottomSwitchCheckbox,
					'switchPropertiesButton': self.lineSide1BottomSwitchPropertiesButton,
					'patternBufferCheckbox': self.lineSide1BottomPatternBufferCheckbox,
					'terminalCheckbox': self.lineSide1BottomTerminalCheckbox,
					'terminalPropertiesButton': self.lineSide1BottomTerminalPropertiesButton,
					'rechargerCheckbox': self.lineSide1BottomRechargerCheckbox,
					'rechargerPropertiesButton': self.lineSide1BottomRechargerPropertiesButton,
				},
				'middle': {
					'dxSlider': self.lineSide1MiddleDXSlider,
					'dySlider': self.lineSide1MiddleDYSlider,
					'textureWell': self.lineSide1MiddleTextureWell,
					'landscapeCheckbox': self.lineSide1MiddleLandscapeCheckbox,
					'effectMenu': self.lineSide1MiddleEffectMenu,
					'effectPropertiesButton': self.lineSide1MiddleEffectPropertiesButton,
					'lightField': self.lineSide1MiddleLightField,
					'switchCheckbox': self.lineSide1MiddleSwitchCheckbox,
					'switchPropertiesButton': self.lineSide1MiddleSwitchPropertiesButton,
					'patternBufferCheckbox': self.lineSide1MiddlePatternBufferCheckbox,
					'terminalCheckbox': self.lineSide1MiddleTerminalCheckbox,
					'terminalPropertiesButton': self.lineSide1MiddleTerminalPropertiesButton,
					'rechargerCheckbox': self.lineSide1MiddleRechargerCheckbox,
					'rechargerPropertiesButton': self.lineSide1MiddleRechargerPropertiesButton,
				},
				'top': {
					'dxSlider': self.lineSide1TopDXSlider,
					'dySlider': self.lineSide1TopDYSlider,
					'textureWell': self.lineSide1TopTextureWell,
					'landscapeCheckbox': self.lineSide1TopLandscapeCheckbox,
					'effectMenu': self.lineSide1TopEffectMenu,
					'effectPropertiesButton': self.lineSide1TopEffectPropertiesButton,
					'lightField': self.lineSide1TopLightField,
					'switchCheckbox': self.lineSide1TopSwitchCheckbox,
					'switchPropertiesButton': self.lineSide1TopSwitchPropertiesButton,
					'patternBufferCheckbox': self.lineSide1TopPatternBufferCheckbox,
					'terminalCheckbox': self.lineSide1TopTerminalCheckbox,
					'terminalPropertiesButton': self.lineSide1TopTerminalPropertiesButton,
					'rechargerCheckbox': self.lineSide1TopRechargerCheckbox,
					'rechargerPropertiesButton': self.lineSide1TopRechargerPropertiesButton,
				},
			},
		),
	})
	
	polygon = property(fget = lambda self: {
		'table': self.polygonTable,
		'layer': {
			'menu': self.polygonLayerMenu,
			'offsetField': self.polygonLayerOffsetField,
			'offsetUnitsField': self.polygonLayerOffsetUnitsField,
		},
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
			'switchCheckbox': self.polygonFloorSwitchCheckbox,
			'switchPropertiesButton': self.polygonFloorSwitchPropertiesButton,
			'patternBufferCheckbox': self.polygonFloorPatternBufferCheckbox,
			'terminalCheckbox': self.polygonFloorTerminalCheckbox,
			'terminalPropertiesButton': self.polygonFloorTerminalPropertiesButton,
			'rechargerCheckbox': self.polygonFloorRechargerCheckbox,
			'rechargerPropertiesButton': self.polygonFloorRechargerPropertiesButton,
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
			'switchCheckbox': self.polygonCeilingSwitchCheckbox,
			'switchPropertiesButton': self.polygonCeilingSwitchPropertiesButton,
			'patternBufferCheckbox': self.polygonCeilingPatternBufferCheckbox,
			'terminalCheckbox': self.polygonCeilingTerminalCheckbox,
			'terminalPropertiesButton': self.polygonCeilingTerminalPropertiesButton,
			'rechargerCheckbox': self.polygonCeilingRechargerCheckbox,
			'rechargerPropertiesButton': self.polygonCeilingRechargerPropertiesButton,
		},
	})
	
	@classmethod
	def sharedInspector(cls):
		if not cls._sharedInspector:
			if usePyObjC:
				cls._sharedInspector = cls.alloc().init()
			else:
				cls._sharedInspector = cls()
		return cls._sharedInspector
	
	def setAttribute(self, prefix, suffix, value):
		return setattr(self, prefix + suffix, value)
	
	def getPath(self, path):
		current = getattr(self, path[0])
		for entry in path[1:]:
			current = current[entry]
		return current
	
	def refresh(self):
		self.document.view.refresh()
	
	def getFrame(self):
		if usePyObjC:
			frame = self.window().frame()
			bottom = frame.origin.y
			left = frame.origin.x
			top = bottom + frame.size.height
			right = left + frame.size.width
		else:
			try:
				frame = self.GetScreenRect()
			except AttributeError: # wx 2.6 does this
				frame = self.GetRect()
			left = frame.GetLeft()
			top = frame.GetTop()
			right = frame.GetRight()
			bottom = frame.GetBottom()
		return (left, top, right, bottom)
	
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
	
	def updateVisibility(self):
		if self.isVisible and self.app.documents:
			self.show()
		else:
			self.hide()
	
	def toggleText(self):
		if self.isVisible:
			return usePyObjC and u"Hide Inspector" or u"Hide &Inspector"
		else:
			return usePyObjC and u"Show Inspector" or u"Show &Inspector"
	
	def setTitle(self, title):
		if usePyObjC:
			self.window().setTitle_(title)
		else:
			self.SetTitle(title)
	
	def show(self):
		if usePyObjC:
			self.showWindow_(self)
		else:
			self.Show()
	
	def hide(self):
		if usePyObjC:
			self.window().close()
		else:
			self.Hide()
	
	def moveTo(self, (x, y)):
		if usePyObjC:
			self.window().setFrameTopLeftPoint_((x, y))
		else:
			self.MoveXY(x, y)
	
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
	
	def update(self):
		if not self.selection:
			self.setTitle(u"Inspector")
			if usePyObjC:
				self.idField.setStringValue_("")
				self.idField.setEnabled_(False)
				self.tabView.selectTabViewItemAtIndex_(0)
			else:
				try:
					self.idField.ChangeValue("")
				except AttributeError: # wx 2.6 does this
					self.idField.SetValue("")
				self.idField.SetEditable(False)
				self.tabView.SetActivePage(ID.NO_SELECTION)
		elif len(self.selection) >= 2:
			self.setTitle(u"Inspector")
			if usePyObjC:
				self.idField.setStringValue_("")
				self.idField.setEnabled_(False)
				self.tabView.selectTabViewItemAtIndex_(1)
			else:
				try:
					self.idField.ChangeValue("")
				except AttributeError: # wx 2.6 does this
					self.idField.SetValue("")
				self.idField.SetEditable(False)
				self.tabView.SetActivePage(ID.MULTIPLE_SELECTION)
		else:
			selection = self.selectedElement
			if usePyObjC:
				self.idField.setStringValue_(str(selection.elementID))
				self.idField.setEnabled_(True)
			else:
				try:
					self.idField.ChangeValue(str(selection.elementID))
				except AttributeError: # wx 2.6 does this
					self.idField.SetValue(str(selection.elementID))
				self.idField.SetEditable(True)
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
	
	def updateVertex(self, vertex, vertexUI):
		if usePyObjC:
			vertexUI['xField'].setDoubleValue_(vertex.x)
			vertexUI['yField'].setDoubleValue_(vertex.y)
		else:
			try:
				vertexUI['xField'].ChangeValue(str(vertex.x))
				vertexUI['yField'].ChangeValue(str(vertex.y))
			except AttributeError: # wx 2.6 does this
				vertexUI['xField'].SetValue(str(vertex.x))
				vertexUI['yField'].SetValue(str(vertex.y))
	
	def updateLine(self, line, lineUI):
		if usePyObjC:
			lineUI['vertex0Field'].setEditable_(False) # can't set this in the NIB for some reason
			lineUI['vertex0Field'].setStringValue_(unicode(line.vertex0.elementID))
			lineUI['vertex1Field'].setEditable_(False) # can't set this in the NIB for some reason
			lineUI['vertex1Field'].setStringValue_(unicode(line.vertex1.elementID))
			#NSButton lineSolidCheckbox
			#NSButton lineTransparentCheckbox
		else:
			try:
				lineUI['vertex0Field'].ChangeValue(unicode(line.vertex0.elementID))
				lineUI['vertex1Field'].ChangeValue(unicode(line.vertex1.elementID))
			except AttributeError: # wx 2.6 does this
				lineUI['vertex0Field'].SetValue(unicode(line.vertex0.elementID))
				lineUI['vertex1Field'].SetValue(unicode(line.vertex1.elementID))
			#wx.Checkbox lineSolidCheckbox
			#wx.Checkbox lineTransparentCheckbox
		for index, sideUI in enumerate(lineUI['side']):
			self.updateSide(line, getattr(line, 'side' + str(index)), index, sideUI)
	
	def updatePolygon(self, polygon, polygonUI):
		if usePyObjC:
			self.updateLayer(polygon.layer, polygonUI['layer'])
			polygonUI['floor']['heightField'].setDoubleValue_(polygon.floorHeight)
			polygonUI['floor']['heightStepper'].setDoubleValue_(polygon.floorHeight)
			polygonUI['floor']['offsetField'].setDoubleValue_(polygon.floorOffset)
			polygonUI['floor']['offsetStepper'].setDoubleValue_(polygon.floorOffset)
			polygonUI['ceiling']['heightField'].setDoubleValue_(polygon.ceilingHeight)
			polygonUI['ceiling']['heightStepper'].setDoubleValue_(polygon.ceilingHeight)
			polygonUI['ceiling']['offsetField'].setDoubleValue_(polygon.ceilingOffset)
			polygonUI['ceiling']['offsetStepper'].setDoubleValue_(polygon.ceilingOffset)
			self.updateSurface(polygon.floor, polygonUI['floor'])
			self.updateSurface(polygon.ceiling, polygonUI['ceiling'])
	
	def updateLayer(self, layer, layerUI):
		if usePyObjC:
			# FIXME: populate layerUI['menu']
			layerUI['menu'].setStringValue_(unicode(layer.elementID))
			layerUI['offsetField'].setDoubleValue_(layer.offset)
			# FIXME: layerUI['offsetUnitsField']
	
	def updateSide(self, line, side, index, sideUI):
		if side:
			if usePyObjC:
				sideUI['polygonField'].setEditable_(False) # can't set this in the NIB for some reason
				sideUI['polygonField'].setEnabled_(True)
				sideUI['polygonField'].setStringValue_(unicode(self.data.polygonForSide(line, index).elementID))
			else:
				try:
					sideUI['polygonField'].ChangeValue(unicode(self.data.polygonForSide(line, index).elementID))
				except AttributeError: # wx 2.6 does this
					sideUI['polygonField'].SetValue(unicode(self.data.polygonForSide(line, index).elementID))
			self.updateSurface(side.lowerSurface, sideUI['bottom'])
			self.updateSurface(side.middleSurface, sideUI['middle'])
			self.updateSurface(side.upperSurface, sideUI['top'])
		else:
			if usePyObjC:
				sideUI['polygonField'].setEditable_(False) # can't set this in the NIB for some reason
				sideUI['polygonField'].setEnabled_(False)
				sideUI['polygonField'].setStringValue_(u"")
			else:
				try:
					sideUI['polygonField'].ChangeValue(u"")
				except AttributeError: # wx 2.6 does this
					sideUI['polygonField'].SetValue(u"")
			self.updateSurface(None, sideUI['bottom'])
			self.updateSurface(None, sideUI['middle'])
			self.updateSurface(None, sideUI['top'])
	
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
				#NSTokenField surfaceUI['lightField']
				surfaceUI['switchCheckbox'].setEnabled_(True)
				if 'switch' in surface.actions:
					surfaceUI['switchCheckbox'].setState_(True)
				else:
					surfaceUI['switchCheckbox'].setState_(False)
				surfaceUI['switchPropertiesButton'].setEnabled_(True)
				surfaceUI['patternBufferCheckbox'].setEnabled_(True)
				if 'pattern buffer' in surface.actions:
					surfaceUI['patternBufferCheckbox'].setState_(True)
				else:
					surfaceUI['patternBufferCheckbox'].setState_(False)
				surfaceUI['terminalCheckbox'].setEnabled_(True)
				if 'terminal' in surface.actions:
					surfaceUI['terminalCheckbox'].setState_(True)
				else:
					surfaceUI['terminalCheckbox'].setState_(False)
				surfaceUI['terminalPropertiesButton'].setEnabled_(True)
				surfaceUI['rechargerCheckbox'].setEnabled_(True)
				if 'recharger' in surface.actions:
					surfaceUI['rechargerCheckbox'].setState_(True)
				else:
					surfaceUI['rechargerCheckbox'].setState_(False)
				surfaceUI['rechargerPropertiesButton'].setEnabled_(True)
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
					surfaceUI['effectMenu'].SetSelection(2)
					surfaceUI['effectPropertiesButton'].Enable()
				elif 'wobble' in surface.effects:
					surfaceUI['effectMenu'].SetSelection(3)
					surfaceUI['effectPropertiesButton'].Enable()
				elif 'slide' in surface.effects:
					surfaceUI['effectMenu'].SetSelection(4)
					surfaceUI['effectPropertiesButton'].Enable()
				elif 'wander' in surface.effects:
					surfaceUI['effectMenu'].SetSelection(5)
					surfaceUI['effectPropertiesButton'].Enable()
				else:
					surfaceUI['effectMenu'].SetSelection(0)
					surfaceUI['effectPropertiesButton'].Disable()
				surfaceUI['lightField'].Enable()
				#wx.TextCtrl surfaceUI['lightField']
				surfaceUI['switchCheckbox'].Enable()
				if 'switch' in surface.actions:
					surfaceUI['switchCheckbox'].SetValue(True)
				else:
					surfaceUI['switchCheckbox'].SetValue(False)
				surfaceUI['switchPropertiesButton'].Enable()
				surfaceUI['patternBufferCheckbox'].Enable()
				if 'pattern buffer' in surface.actions:
					surfaceUI['patternBufferCheckbox'].SetValue(True)
				else:
					surfaceUI['patternBufferCheckbox'].SetValue(False)
				surfaceUI['terminalCheckbox'].Enable()
				if 'terminal' in surface.actions:
					surfaceUI['terminalCheckbox'].SetValue(True)
				else:
					surfaceUI['terminalCheckbox'].SetValue(False)
				surfaceUI['terminalPropertiesButton'].Enable()
				surfaceUI['rechargerCheckbox'].Enable()
				if 'recharger' in surface.actions:
					surfaceUI['rechargerCheckbox'].SetValue(True)
				else:
					surfaceUI['rechargerCheckbox'].SetValue(False)
				surfaceUI['rechargerPropertiesButton'].Enable()
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
				surfaceUI['switchCheckbox'].setEnabled_(False)
				surfaceUI['switchCheckbox'].setState_(False)
				surfaceUI['switchPropertiesButton'].setEnabled_(False)
				surfaceUI['patternBufferCheckbox'].setEnabled_(False)
				surfaceUI['patternBufferCheckbox'].setState_(False)
				surfaceUI['terminalCheckbox'].setEnabled_(False)
				surfaceUI['terminalCheckbox'].setState_(False)
				surfaceUI['terminalPropertiesButton'].setEnabled_(False)
				surfaceUI['rechargerCheckbox'].setEnabled_(False)
				surfaceUI['rechargerCheckbox'].setState_(False)
				surfaceUI['rechargerPropertiesButton'].setEnabled_(False)
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
				try:
					surfaceUI['lightField'].ChangeValue("")
				except AttributeError: # wx 2.6 does this
					surfaceUI['lightField'].SetValue("")
				surfaceUI['switchCheckbox'].Disable()
				surfaceUI['switchCheckbox'].SetValue(False)
				surfaceUI['switchPropertiesButton'].Disable()
				surfaceUI['patternBufferCheckbox'].Disable()
				surfaceUI['patternBufferCheckbox'].SetValue(False)
				surfaceUI['terminalCheckbox'].Disable()
				surfaceUI['terminalCheckbox'].SetValue(False)
				surfaceUI['terminalPropertiesButton'].Disable()
				surfaceUI['rechargerCheckbox'].Disable()
				surfaceUI['rechargerCheckbox'].SetValue(False)
				surfaceUI['rechargerPropertiesButton'].Disable()
	
	def openUndoGroup(self, name = None):
		return self.document.openUndoGroup(name)
	
	def closeUndoGroup(self, name = None):
		return self.document.closeUndoGroup(name)
	
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
		#else:
		#	self.update() # this causes infinite recursion in wx 2.6
		self.refresh()
	
	def lineSolidChanged(self, value):
		print "%s.lineSolidChanged(%s)" % (self, value)
	
	def lineTransparentChanged(self, value):
		print "%s.lineTransparentChanged(%s)" % (self, value)
	
	def surfaceDXChanged(self, surface, value):
		# FIXME: The undo group should not start and end here
		self.openUndoGroup(u"Move Texture")
		self.data.setSurfaceOffset(surface, (value, surface.dy))
		self.closeUndoGroup()
		self.update()
		self.refresh()
	
	def surfaceDYChanged(self, surface, value):
		# FIXME: The undo group should not start and end here
		self.openUndoGroup(u"Move Texture")
		self.data.setSurfaceOffset(surface, (surface.dx, value))
		self.closeUndoGroup()
		self.update()
		self.refresh()
	
	def surfaceLandscapeChanged(self, surface, value):
		self.openUndoGroup(u"Toggle Landscape Mode")
		if value:
			self.data.addSurfaceEffect(surface, 'landscape', {})
		else:
			self.data.removeSurfaceEffect(surface, 'landscape')
		self.closeUndoGroup()
		self.update()
	
	def surfaceLightChanged(self, surface, value):
		print "%s.surfaceLightChanged(%s, %s)" % (self, surface, value)
	
	def vertexXChanged(self, value):
		vertex = self.selectedElement
		self.openUndoGroup(u"Move Vertex '%s'" % (vertex.elementID, ))
		self.data.moveVertex(vertex, (value - vertex.x, 0.0))
		self.closeUndoGroup()
		self.refresh()
	
	def vertexYChanged(self, value):
		vertex = self.selectedElement
		self.openUndoGroup(u"Move Vertex '%s'" % (vertex.elementID, ))
		self.data.moveVertex(vertex, (0.0, value - vertex.y))
		self.closeUndoGroup()
		self.refresh()
	
	# PyObjC
	
	def init(self):
		self = super(ForgeryInspector, self).initWithWindowNibName_(u"ForgeryInspector")
		self.window().setBecomesKeyOnlyIfNeeded_(True)
		return self
	
	def windowDidMove_(self, notification):
		self.moved()
	
	def idChanged_(self, sender):
		self.idChanged(sender.stringValue())
	
	def lineSolidChanged_(self, sender):
		self.lineSolidChanged(sender.intValue())
	
	def lineTransparentChanged_(self, sender):
		self.lineTransparentChanged(sender.intValue())
	
	def polygonCeilingHeightChanged_(self, sender):
		print "[%s polygonCeilingHeightChanged:%s]" % (self, sender)
	
	def polygonCeilingOffsetChanged_(self, sender):
		print "[%s polygonCeilingOffsetChanged:%s]" % (self, sender)
	
	def polygonFloorHeightChanged_(self, sender):
		print "[%s polygonFloorHeightChanged:%s]" % (self, sender)
	
	def polygonFloorOffsetChanged_(self, sender):
		print "[%s polygonFloorOffsetChanged:%s]" % (self, sender)
	
	def polygonLayerChanged_(self, sender):
		print "[%s polygonLayerChanged:%s]" % (self, sender)
	
	def surfaceActionToggled_(self, sender):
		if sender.tag() == ID.ACTION_SWITCH:
			surface = self.findSurfaceForUI(sender, 'switchCheckbox')
			action = 'switch'
			properties = {}
		elif sender.tag() == ID.ACTION_PATTERN_BUFFER:
			surface = self.findSurfaceForUI(sender, 'patternBufferCheckbox')
			action = 'pattern buffer'
			properties = {}
		elif sender.tag() == ID.ACTION_TERMINAL:
			surface = self.findSurfaceForUI(sender, 'terminalCheckbox')
			action = 'terminal'
			properties = {}
		elif sender.tag() == ID.ACTION_RECHARGER:
			surface = self.findSurfaceForUI(sender, 'rechargerCheckbox')
			action = 'recharger'
			properties = {}
		if sender.state():
			self.openUndoGroup(u"Add Action")
			self.data.addSurfaceAction(surface, action, properties)
		else:
			self.openUndoGroup(u"Remove Action")
			self.data.removeSurfaceAction(surface, action)
		self.closeUndoGroup()
		self.update()
	
	def surfaceActionPropertiesClicked_(self, sender):
		print "[%s surfaceActionPropertiesClicked:%s]" % (self, sender)
	
	def surfaceDXChanged_(self, sender):
		surface = self.findSurfaceForUI(sender, 'dxSlider')
		self.surfaceDXChanged(surface, sender.doubleValue())
	
	def surfaceDYChanged_(self, sender):
		surface = self.findSurfaceForUI(sender, 'dySlider')
		self.surfaceDYChanged(surface, sender.doubleValue())
	
	def surfaceEffectChanged_(self, sender):
		surface = self.findSurfaceForUI(sender, 'effectMenu')
		self.openUndoGroup(u"Change Effect")
		for effect in surface.effects.keys():
			if effect in ('pulsate', 'wobble', 'slide', 'wander'):
				self.data.removeSurfaceEffect(surface, effect)
		if sender.selectedItem().tag() == ID.EFFECT_PULSATE:
			self.data.addSurfaceEffect(surface, 'pulsate', {})
		elif sender.selectedItem().tag() == ID.EFFECT_WOBBLE:
			self.data.addSurfaceEffect(surface, 'wobble', {})
		elif sender.selectedItem().tag() == ID.EFFECT_SLIDE:
			self.data.addSurfaceEffect(surface, 'slide', {})
		elif sender.selectedItem().tag() == ID.EFFECT_WANDER:
			self.data.addSurfaceEffect(surface, 'wander', {})
		self.closeUndoGroup()
		self.update()
	
	def surfaceEffectPropertiesClicked(self, sender):
		print "[%s surfaceEffectPropertiesClicked:%s]" % (self, sender)
	
	def surfaceLandscapeChanged_(self, sender):
		surface = self.findSurfaceForUI(sender, 'landscapeCheckbox')
		self.surfaceLandscapeChanged(surface, sender.state())
	
	def surfaceLightChanged_(self, sender):
		self.surfaceLightChanged(surface, sender.stringValue())
	
	def vertexXChanged_(self, sender):
		self.vertexXChanged(sender.doubleValue())
	
	def vertexYChanged_(self, sender):
		self.vertexYChanged(sender.doubleValue())
	
	# wxPython
	
	if not usePyObjC:
		
		sizer = property(
			fget = lambda self: self.GetSizer(),
			fset = lambda self, value: self.SetSizer(value),
		)
		tabView = None
		vertexXField = None
		vertexYField = None
		lineVertex0Field = None
		lineVertex1Field = None
		lineSolidCheckbox = None
		lineTransparentCheckbox = None
		lineSide0PolygonField = None
		lineSide0BottomDXSlider = None
		lineSide0BottomDYSlider = None
		lineSide0BottomTextureWell = None
		lineSide0BottomLandscapeCheckbox = None
		lineSide0BottomEffectMenu = None
		lineSide0BottomEffectPropertiesButton = None
		lineSide0BottomLightField = None
		lineSide0BottomSwitchCheckbox = None
		lineSide0BottomSwitchPropertiesButton = None
		lineSide0BottomPatternBufferCheckbox = None
		lineSide0BottomTerminalCheckbox = None
		lineSide0BottomTerminalPropertiesButton = None
		lineSide0BottomRechargerCheckbox = None
		lineSide0BottomRechargerPropertiesButton = None
		lineSide0MiddleDXSlider = None
		lineSide0MiddleDYSlider = None
		lineSide0MiddleTextureWell = None
		lineSide0MiddleLandscapeCheckbox = None
		lineSide0MiddleEffectMenu = None
		lineSide0MiddleEffectPropertiesButton = None
		lineSide0MiddleLightField = None
		lineSide0MiddleSwitchCheckbox = None
		lineSide0MiddleSwitchPropertiesButton = None
		lineSide0MiddlePatternBufferCheckbox = None
		lineSide0MiddleTerminalCheckbox = None
		lineSide0MiddleTerminalPropertiesButton = None
		lineSide0MiddleRechargerCheckbox = None
		lineSide0MiddleRechargerPropertiesButton = None
		lineSide0TopDXSlider = None
		lineSide0TopDYSlider = None
		lineSide0TopTextureWell = None
		lineSide0TopLandscapeCheckbox = None
		lineSide0TopEffectMenu = None
		lineSide0TopEffectPropertiesButton = None
		lineSide0TopLightField = None
		lineSide0TopSwitchCheckbox = None
		lineSide0TopSwitchPropertiesButton = None
		lineSide0TopPatternBufferCheckbox = None
		lineSide0TopTerminalCheckbox = None
		lineSide0TopTerminalPropertiesButton = None
		lineSide0TopRechargerCheckbox = None
		lineSide0TopRechargerPropertiesButton = None
		lineSide1PolygonField = None
		lineSide1BottomDXSlider = None
		lineSide1BottomDYSlider = None
		lineSide1BottomTextureWell = None
		lineSide1BottomLandscapeCheckbox = None
		lineSide1BottomEffectMenu = None
		lineSide1BottomEffectPropertiesButton = None
		lineSide1BottomLightField = None
		lineSide1BottomSwitchCheckbox = None
		lineSide1BottomSwitchPropertiesButton = None
		lineSide1BottomPatternBufferCheckbox = None
		lineSide1BottomTerminalCheckbox = None
		lineSide1BottomTerminalPropertiesButton = None
		lineSide1BottomRechargerCheckbox = None
		lineSide1BottomRechargerPropertiesButton = None
		lineSide1MiddleDXSlider = None
		lineSide1MiddleDYSlider = None
		lineSide1MiddleTextureWell = None
		lineSide1MiddleLandscapeCheckbox = None
		lineSide1MiddleEffectMenu = None
		lineSide1MiddleEffectPropertiesButton = None
		lineSide1MiddleLightField = None
		lineSide1MiddleSwitchCheckbox = None
		lineSide1MiddleSwitchPropertiesButton = None
		lineSide1MiddlePatternBufferCheckbox = None
		lineSide1MiddleTerminalCheckbox = None
		lineSide1MiddleTerminalPropertiesButton = None
		lineSide1MiddleRechargerCheckbox = None
		lineSide1MiddleRechargerPropertiesButton = None
		lineSide1TopDXSlider = None
		lineSide1TopDYSlider = None
		lineSide1TopTextureWell = None
		lineSide1TopLandscapeCheckbox = None
		lineSide1TopEffectMenu = None
		lineSide1TopEffectPropertiesButton = None
		lineSide1TopLightField = None
		lineSide1TopSwitchCheckbox = None
		lineSide1TopSwitchPropertiesButton = None
		lineSide1TopPatternBufferCheckbox = None
		lineSide1TopTerminalCheckbox = None
		lineSide1TopTerminalPropertiesButton = None
		lineSide1TopRechargerCheckbox = None
		lineSide1TopRechargerPropertiesButton = None
		polygonTable = None
		polygonLayerMenu = None
		polygonLayerOffsetField = None
		polygonLayerOffsetUnitsField = None
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
		polygonFloorSwitchCheckbox = None
		polygonFloorSwitchPropertiesButton = None
		polygonFloorPatternBufferCheckbox = None
		polygonFloorTerminalCheckbox = None
		polygonFloorTerminalPropertiesButton = None
		polygonFloorRechargerCheckbox = None
		polygonFloorRechargerPropertiesButton = None
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
		polygonCeilingSwitchCheckbox = None
		polygonCeilingSwitchPropertiesButton = None
		polygonCeilingPatternBufferCheckbox = None
		polygonCeilingTerminalCheckbox = None
		polygonCeilingTerminalPropertiesButton = None
		polygonCeilingRechargerCheckbox = None
		polygonCeilingRechargerPropertiesButton = None
		
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
		sizer = createCenteredText(result, "Nothing Selected")
		result.SetSizer(sizer)
		sizer.Layout()
		sizer.Fit(result)
		return result
	
	def BuildMultipleSelectionUI(self):
		result = wx.Panel(self, -1)
		sizer = createCenteredText(result, "Multiple Objects Selected")
		result.SetSizer(sizer)
		sizer.Layout()
		sizer.Fit(result)
		return result
	
	def BuildVertexUI(self):
		result = wx.Panel(self, -1)
		self.vertexXField = createTextCtrl(result, self.OnVertexXChanged)
		self.vertexYField = createTextCtrl(result, self.OnVertexYChanged)
		sizer = buildNonuniformGrid(
			2,
			createRightAlignedStaticText(result, "X:"),
			self.vertexXField,
			createRightAlignedStaticText(result, "Y:"),
			self.vertexYField,
		)
		result.SetSizer(sizer)
		sizer.Layout()
		sizer.Fit(result)
		return result
	
	def BuildLineUI(self):
		result = wx.Panel(self, -1)
		self.lineVertex0Field = createTextCtrl(result)
		self.line['vertex0Field'].Disable()
		self.lineVertex1Field = createTextCtrl(result)
		self.line['vertex1Field'].Disable()
		self.lineSolidCheckbox = createCheckbox(result, "Solid", self.OnLineSolidChanged)
		self.lineTransparentCheckbox = createCheckbox(result, "Transparent", self.OnLineTransparentChanged)
		notebook = wx.Notebook(result, -1, style = wx.BK_TOP)
		notebook.AddPage(
			self.BuildSideUI(
				notebook,
				'lineSide0',
				('line', 'side', 0),
			),
			"First Side",
		)
		notebook.AddPage(
			self.BuildSideUI(
				notebook,
				'lineSide1',
				('line', 'side', 1),
			),
			"Second Side",
		)
		sizer = buildSizers(
			wx.VERTICAL,
			buildNonuniformGrid(
				2,
				createRightAlignedStaticText(result, "First Vertex:"),
				self.line['vertex0Field'],
				createRightAlignedStaticText(result, "Second Vertex:"),
				self.line['vertex1Field'],
				None,
				self.line['solidCheckbox'],
				None,
				self.line['transparentCheckbox'],
			),
			notebook,
		)
		result.SetSizer(sizer)
		sizer.Layout()
		sizer.Fit(result)
		return result
	
	def BuildPolygonUI(self):
		# FIXME
		return None
	
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
			"Top",
		)
		notebook.AddPage(
			self.BuildSurfaceUI(
				notebook,
				prefix + 'Middle',
				path + ('middle', ),
			),
			"Middle",
		)
		notebook.AddPage(
			self.BuildSurfaceUI(
				notebook,
				prefix + 'Bottom',
				path + ('bottom', ),
			),
			"Bottom",
		)
		sizer = buildSizers(
			wx.HORIZONTAL,
			8,
			(
				8,
				(
					createRightAlignedStaticText(result, "Polygon:"),
					8,
					self.getPath(path)['polygonField'],
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
		self.setAttribute(prefix, 'EffectMenu', wx.Choice(
			result, -1,
			wx.DefaultPosition,
			wx.DefaultSize,
			(
				"Normal",
				"",
				"Pulsate",
				"Slide",
				"Wander",
				"Wobble",
			),
		))
		self.setAttribute(prefix, 'EffectPropertiesButton', createPropertiesButton(result))
		self.setAttribute(prefix, 'LandscapeCheckbox', createCheckbox(
			result,
			"Landscape",
			self.OnSurfaceLandscapeChanged,
		))
		self.setAttribute(prefix, 'LightField', createTextCtrl(
			result,
			self.OnSurfaceLightChanged,
		))
		self.setAttribute(prefix, 'PatternBufferCheckbox', createCheckbox(
			result,
			"Pattern Buffer",
		))
		self.setAttribute(prefix, 'RechargerCheckbox', createCheckbox(
			result,
			"Recharger",
		))
		self.setAttribute(prefix, 'RechargerPropertiesButton', createPropertiesButton(result))
		self.setAttribute(prefix, 'SwitchCheckbox', createCheckbox(
			result,
			"Switch",
		))
		self.setAttribute(prefix, 'SwitchPropertiesButton', createPropertiesButton(result))
		self.setAttribute(prefix, 'TerminalCheckbox', createCheckbox(
			result,
			"Terminal",
		))
		self.setAttribute(prefix, 'TerminalPropertiesButton', createPropertiesButton(result))
		self.setAttribute(prefix, 'TextureWell', createTextureWell(
			result,
			ForgeryElements.ForgerySurface(None, None, ForgeryElements.ForgeryTexture('')).image, # this will be replaced when update() is called
		))
		sizer = buildSizers(
			wx.HORIZONTAL,
			20,
			(
				20,
				buildNonuniformGrid(
					3,
					
					self.getPath(path)['dySlider'],
					self.getPath(path)['textureWell'],
					None,
					
					None,
					self.getPath(path)['dxSlider'],
					None,
					
					None,
					self.getPath(path)['landscapeCheckbox'],
					None,
					
					createRightAlignedStaticText(result, "Effect:"),
					self.getPath(path)['effectMenu'],
					self.getPath(path)['effectPropertiesButton'],
					
					createRightAlignedStaticText(result, "Light:"),
					self.getPath(path)['lightField'],
					None,
				),
				buildNonuniformGrid(
					5,
					
					self.getPath(path)['switchCheckbox'],
					self.getPath(path)['switchPropertiesButton'],
					None,
					self.getPath(path)['patternBufferCheckbox'],
					None,
					
					self.getPath(path)['terminalCheckbox'],
					self.getPath(path)['terminalPropertiesButton'],
					None,
					self.getPath(path)['rechargerCheckbox'],
					self.getPath(path)['rechargerPropertiesButton'],
				),
				20,
			),
			20,
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
	
	def OnSurfaceDXChanged(self, event):
		surface = self.findSurfaceForUI(event.GetEventObject(), 'dxSlider')
		self.surfaceDXChanged(surface, event.GetEventObject().GetValue())
	
	def OnSurfaceDYChanged(self, event):
		surface = self.findSurfaceForUI(event.GetEventObject(), 'dySlider')
		self.surfaceDYChanged(surface, event.GetEventObject().GetValue())
	
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
