# ForgeryPalette.py
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
	'ForgeryPalette',
	'sharedPalette',
	'ForgeryPaletteDelegate',
)

import ForgeryApplication, ForgeryPreferences

if usePyObjC:
	
	from Foundation import *
	from AppKit import *
	import objc
	from tracer import traced
	
	class ForgeryPaletteWindow(NSPanel):
		
		def canBecomeKeyWindow(self):
			return False
		
		def canBecomeMainWindow(self):
			return False
	
else:
	
	import wx

class ForgeryPalette(NSWindowController if usePyObjC else wx.MiniFrame):
	delegate = objc.IBOutlet() if usePyObjC else None
	if usePyObjC:
		matrix = objc.IBOutlet()
		elementToTag = None
		tagToElement = None
	else:
		sizer = property(
			fget = lambda self: self.GetSizer(),
			fset = lambda self, value: self.SetSizer(value),
			fdel = lambda self: self.SetSizer(None),
		)
		buttons = None
	
	@property
	def app(self):
		return ForgeryApplication.sharedApplication()
	@property
	def mode(self):
		return self.delegate.mode
	@property
	def document(self):
		return self.mode.document
	@property
	@traced
	def preferences(self):
		return self.document.preferences if self.document else self.app.preferences
	@property
	def elements(self):
		return self.delegate.elements
	@property
	def icons(self):
		return self.delegate.icons
	@property
	def title(self):
		return self.delegate.title
	currentObject = property(
		fget = lambda self: getattr(self.delegate, 'currentObject'),
		fset = lambda self, value: setattr(self.delegate, 'currentObject', value),
	)
	isDocked = property(
		fget = lambda self: getattr(self.preferences, 'paletteIsDocked'),
		fset = lambda self, value: setattr(self.preferences, 'paletteIsDocked', value),
	)
	position = property(
		fget = lambda self: getattr(self.preferences, 'palettePosition'),
		fset = lambda self, value: setattr(self.preferences, 'palettePosition', value),
	)
	isVisible = property(
		fget = lambda self: getattr(self.preferences, 'paletteIsVisible'),
		fset = lambda self, value: setattr(self.preferences, 'paletteIsVisible', value),
	)
	
	# Shared
	
	_sharedPalette = None
	@classmethod
	def sharedPalette(Class):
		if not Class._sharedPalette:
			if usePyObjC:
				Class._sharedPalette = Class.alloc().init()
			else:
				Class._sharedPalette = Class()
		return Class._sharedPalette
	
	if usePyObjC:
		
		@traced
		def init(self):
			#self = super(ForgeryPalette, self).initWithWindowNibName_(u'ForgeryPalette')
			self = super(ForgeryPalette, self).init()
			if self and not ForgeryPalette._sharedPalette:
				ForgeryPalette._sharedPalette = self
			return self
		
		def getFrame(self):
			frame = self.window().frame()
			bottom = frame.origin.y
			left = frame.origin.x
			top = bottom + frame.size.height
			right = left + frame.size.width
			return (left, top, right, bottom)
		
	else:
		
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
				left, top, right, bottom = self.document.getFrame()
			except AttributeError: # document is None
				pass
			else:
				self.moveTo((right + 10, top))
		else:
			self.moveTo(self.position)
	
	@traced
	def updateVisibility(self):
		if self.isVisible and self.app.documents:
			self.show()
		else:
			self.hide()
	
	@traced
	def updateSelection(self):
		if usePyObjC:
			tag = self.elementToTag[self.currentObject]
			self.matrix.selectCellWithTag_(tag)
			self.matrix.cellWithTag_(tag).setState_(True)
		else:
			for button in self.buttons.itervalues():
				button.OnUpdate()
	
	@traced
	def toggleText(self):
		if self.isVisible:
			return u"Hide Palette" if usePyObjC else u"Hide &Palette"
		else:
			return u"Show Palette" if usePyObjC else u"Show &Palette"
	
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
		if -20 < myLeft - (itsRight + 10) < 20 and -20 < myTop - itsTop < 20:
			self.isDocked = True
			self.position = None
		else:
			self.isDocked = False
			self.position = (myLeft, myTop)
		self.updatePosition()
	
	@traced
	def update(self):
		self.delegate.setupElements()
		self.setTitle(self.title)
		rows = max([row for row, col in self.elements] + [0]) + 1
		cols = max([col for row, col in self.elements] + [0]) + 1
		
		if usePyObjC:
			
			self.elementToTag = {}
			self.tagToElement = {}
			
			self.matrix.renewRows_columns_(rows, cols)
			self.matrix.sizeToCells()
			self.matrix.setDoubleAction_('doubleClick:')
			self.matrix.setFrame_((
				(0, 0),
				(38 * cols, 38 * rows),
			))
			self.window().setContentSize_(self.matrix.frame().size)
			
			tag = 1
			for row in xrange(rows):
				for col in xrange(cols):
					cell = self.matrix.cellAtRow_column_(row, col)
					cell.setImage_(self.icons.get((row, col), None))
					cell.setBezelStyle_(NSShadowlessSquareBezelStyle)
					try:
						element = self.elements[(row, col)]
					except KeyError:
						cell.setEnabled_(False)
						cell.setTransparent_(True)
						cell.setTag_(0)
						cell.setState_(False)
					else:
						self.elementToTag[element] = tag
						self.tagToElement[tag] = element
						cell.setEnabled_(True)
						cell.setTransparent_(False)
						cell.setTag_(tag)
						cell.setState_(element == self.currentObject)
						tag += 1
			
		else:
			
			self.buttons = {}
			if self.sizer:
				self.sizer.Clear(True)
				self.sizer.SetRows(rows)
				self.sizer.SetCols(cols)
			else:
				self.sizer = wx.GridSizer(rows = rows, cols = cols, vgap = 0, hgap = 0)
			for row in xrange(rows):
				for col in xrange(cols):
					index = row * cols + col
					if (row, col) in self.elements:
						self.buttons[(row, col)] = ForgeryPaletteButton(self, self.elements[(row, col)], self.icons[(row, col)])
						#self.Bind(wx.EVT_BUTTON, errorWrap(self.buttons[(row, col)].clicked), self.buttons[(row, col)])
						self.sizer.Add(self.buttons[(row, col)])
					else:
						self.sizer.AddStretchSpacer()
			self.sizer.Layout()
			self.sizer.Fit(self)
			self.Fit()
			self.Refresh()
		
		self.updateSelection()
		self.updateVisibility()
		self.updatePosition()
	
	@traced
	def select(self, obj):
		if self.currentObject != obj:
			self.delegate.deactivate(self.currentObject)
			self.currentObject = obj
			self.delegate.activate(self.currentObject)
	
	@traced
	def doubleClick(self, obj):
		self.delegate.doubleClick(obj)
	
	if usePyObjC:
		
		@traced
		def windowDidMove_(self, notification):
			self.moved()
		
		@objc.IBAction
		@traced
		def select_(self, sender):
			self.select(self.tagToElement[sender.selectedCell().tag()])
		
		@objc.IBAction
		@traced
		def doubleClick_(self, sender):
			self.select_(sender)
			self.doubleClick(self.currentObject)
		
	else:
		
		def __init__(self):
			self.delegate = None
			self.buttons = {}
			super(ForgeryPalette, self).__init__(
				None,
				style = wx.STAY_ON_TOP | wx.CAPTION | wx.CLOSE_BOX,
			)
			self.Bind(wx.EVT_CLOSE, errorWrap(self.OnClose))
			self.Bind(wx.EVT_MOVE, errorWrap(self.OnMoved))
			self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
		
		def OnClose(self, event):
			if event.CanVeto() and self.IsShown():
				self.hide()
				event.Veto()
			else:
				self.Destroy()
		
		def OnMoved(self, event):
			self.moved()

def sharedPalette():
	return ForgeryPalette.sharedPalette()

class ForgeryPaletteDelegate(NSObject if usePyObjC else object):
	mode = objc.IBOutlet('mode') if usePyObjC else None
	elements = None
	icons = None
	title = u""
	currentObject = None
	
	# Shared
	
	@traced
	def setupElements(self):
		self.elements = {}
		self.icons = {}
	
	def deactivate(self, obj):
		pass
	
	def activate(self, obj):
		pass
	
	def doubleClick(self, obj):
		pass
	
	if usePyObjC:
		
		def initWithMode_(self, mode):
			self = super(ForgeryPaletteDelegate, self).init()
			if self:
				self.mode = mode
			return self
	
	else:
		
		def __init__(self, mode):
			super(ForgeryPaletteDelegate, self).__init__()
			self.mode = mode

if not usePyObjC:
	
	import wx.lib.buttons
	
	class ForgeryPaletteButton(wx.lib.buttons.GenBitmapButton):
		owner = None
		obj = None
		pressed = False
		
		def __init__(self, owner, obj, icon, *posArgs, **kwdArgs):
			posArgs = (owner, ) + posArgs
			kwdArgs['bitmap'] = icon
			super(ForgeryPaletteButton, self).__init__(*posArgs, **kwdArgs)
			self.owner = owner
			self.obj = obj
			self.SetUseFocusIndicator(False)
			#self.Bind(wx.EVT_BUTTON, errorWrap(self.OnClick))
			#self.Bind(wx.EVT_TOGGLEBUTTON, errorWrap(self.OnClick))
			#self.Bind(wx.EVT_UPDATE_UI, errorWrap(self.OnUpdate))
			self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
			self.OnUpdate()
		
		#def Notify(self):
		#	self.OnClick(None)
		
		def OnClick(self, event):
			self.owner.select(self.obj)
			for sibling in self.owner.buttons.itervalues():
				if isinstance(sibling, ForgeryPaletteButton):
					sibling.OnUpdate()
		
		def OnUpdate(self, event = None):
			if self.obj == self.owner.currentObject:
				self.up = False
				self.Refresh()
			else:
				self.up = not self.pressed
				self.Refresh()
		
		def OnLeftDown(self, event):
			if not self.IsEnabled():
				return
			self.pressed = True
			self.up = False
			self.CaptureMouse()
			self.Refresh()
		
		def OnLeftUp(self, event):
			if not self.IsEnabled():
				return
			if self.HasCapture():
				self.ReleaseMouse()
				self.Refresh()
				if self.pressed:
					self.pressed = False
					self.up = True
					self.OnClick(event)
				else:
					self.OnUpdate()
		
		def OnMotion(self, event):
			if not self.IsEnabled():
				return
			if event.LeftIsDown() and self.HasCapture():
				x, y = event.GetPositionTuple()
				w, h = self.GetClientSizeTuple()
				if 0 <= x < w and 0 <= y < h:
					self.pressed = True
					self.up = False
					self.Refresh()
				else:
					self.pressed = False
					self.up = True
					self.Refresh()
