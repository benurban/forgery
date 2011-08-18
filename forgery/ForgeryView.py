#!/usr/bin/env python

# ForgeryView.py
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
	'ForgeryView',
)

import ForgeryCursor, ForgeryPoint

from OpenGL.GL import *
from OpenGL.GLU import *

from tracer import traced

if usePyObjC:
	
	from Foundation import *
	from AppKit import *
	
	def display(name, value):
		return
		if isinstance(value, ForgeryPoint.ForgeryPoint):
			print "%15s %6s(%7s, %7s)" % (name, value.coordinates, '%.1f' % value.x, '%.1f' % value.y)
		else:
			print "%15s %s" % (name, value)
	
else:
	
	import wx
	import wx.glcanvas

class ForgeryView(NSOpenGLView if usePyObjC else wx.glcanvas.GLCanvas):
	if usePyObjC:
		document = objc.IBOutlet()
		statusBar = objc.IBOutlet()
	else:
		document = None
	zoomFactor = 16.0
	center = None
	player = None
	mouse0 = None
	mouse1 = None
	cursor = None
	
	scrollMin = None
	scrollMax = None
	clipSize = None
	
	if usePyObjC:
		@property
		def clipMin(self):
			return self.center - ForgeryPoint.ForgeryPoint((self.clipSize - (1, 1)).asObject / 2.0)
		@property
		def clipMax(self):
			return self.center + ForgeryPoint.ForgeryPoint((self.clipSize - (1, 1)).asObject / 2.0)
		@property
		def scrollSize(self):
			return ForgeryPoint.ForgerySize((self.scrollMax - self.scrollMin).asObject)
	else:
		@property
		def clipMin(self):
			return self.center - ForgeryPoint.ForgeryPoint((self.clipSize - (1, 1)).asObject / 2.0).scale((1.0, -1.0))
		@property
		def clipMax(self):
			return self.center + ForgeryPoint.ForgeryPoint((self.clipSize - (1, 1)).asObject / 2.0).scale((1.0, -1.0))
		@property
		def scrollSize(self):
			return ForgeryPoint.ForgerySize((self.scrollMax - self.scrollMin).asObject).scale((1.0, -1.0))
	@property
	def extraSize(self):
		"Amount of extra space added to each end of the scroll bars to facilitate unlimited scrolling"
		return self.clipSize.asView
	
	@property
	def currentMode(self):
		return self.document.currentMode
	@property
	def delegate(self):
		return self.currentMode.viewDelegate
	@property
	def currentTool(self):
		return self.currentMode.currentTool
	@property
	def data(self):
		return self.document.data
	@property
	def preferences(self):
		return self.document.preferences
	@property
	def backgroundColor(self):
		return self.preferences.backgroundColor
	if usePyObjC:
		@property
		def sizeInPixels(self):
			return ForgeryPoint.ForgerySize('view', self, self.frame().size)
	else:
		@property
		def sizeInPixels(self):
			return ForgeryPoint.ForgerySize('clip', self, self.GetClientSize())
	
	if usePyObjC:
		@property
		def scrollView(self):
			return self.enclosingScrollView()
	
	# Shared
	
	def refresh(self):
		if usePyObjC:
			self.setNeedsDisplay_(True)
		else:
			self.Refresh()
	
	@traced
	def texturesUpdated(self):
		if self.delegate:
			self.delegate.texturesUpdated()
	
	@traced
	def doInit(self):
		if not self.center:
			self.center = ForgeryPoint.ForgeryPoint('object', self, 0.0, 0.0)
		if not self.player:
			self.player = ForgeryPoint.ForgeryPoint('object', self, 0.0, 0.0)
		if usePyObjC:
			self.clipSize = self.sizeInPixels.asView
		else: # sizeInPixels is (-16, -16)
			self.clipSize = ForgeryPoint.ForgerySize('view', self, 0.0, 0.0)
		self.scrollMin = self.clipMin
		self.scrollMax = self.clipMax
		#if usePyObjC:
		#	self.scaleUnitSquareToSize_((1.0 / self.zoomFactor, 1.0 / self.zoomFactor))
		#	self.setBoundsOrigin_(self.center - ((self.clipSize.asObject - ForgeryPoint.ForgerySize('view', self, 1, 1)) / 2.0))
		self.adjustScrollbars()
	
	def adjustScroll_(self, proposedVisibleRect):
		#print '[%r adjustScroll:%r]' % (self, proposedVisibleRect)
		display('documentVisibleRect', self.scrollView.documentVisibleRect())
		origin = ForgeryPoint.ForgeryPoint('view', self, proposedVisibleRect.origin)
		size = ForgeryPoint.ForgerySize('view', self, proposedVisibleRect.size)
		delta = origin.asView - self.extraSize.asView - ForgeryPoint.ForgerySize(self.center).asView
		center = self.center.asView - self.scrollMin.asView + delta.asView
		#origin = ForgeryPoint.ForgeryPoint('view', self, proposedVisibleRect.origin) - self.extraSize.asView
		#delta = origin - ForgeryPoint.ForgerySize(self.center).asView
		#size = ForgeryPoint.ForgerySize('view', self, proposedVisibleRect.size)
		#origin = ForgeryPoint.ForgeryPoint('object', self, proposedVisibleRect.origin)
		#size = ForgeryPoint.ForgerySize('object', self, proposedVisibleRect.size)
		#center = origin + (size - ForgeryPoint.ForgerySize('view', self, 1, 1)) / 2.0
		display('zoomFactor', self.zoomFactor)
		display('center', self.center)
		display('clipSize', self.clipSize)
		display('scrollMin', self.scrollMin)
		display('scrollMax', self.scrollMax)
		display('delta', delta)
		display('origin', origin)
		display('size', size)
		display('center', center)
		#print 'center', center.asView
		#print 'center', center.asObject
		#print
		#self.pan(self.center - center)
		#self._documentVisibleOrigin = proposedVisibleRect.origin - ForgeryPoint.ForgerySize(self.center).asView # this is a very ugly hack
		self._scrollDelta = delta
		self.center = center.asObject
		self.adjustScrollbars()
		self.refresh()
		return proposedVisibleRect
	
	# FIXME: handle window sizing in Cocoa
	def adjustScrollbars(self):
		try:
			elements = self.data.vertices.values()
		except AttributeError: # data might be None
			elements = []
		coords = [(element.x, element.y) for element in elements]
		# include the top-right and bottom-left corners of the clip area
		# in the list of coordinates for consideration
		coords.append(self.clipMin.asObject)
		coords.append(self.clipMax.asObject)
		xCoords = [x for x, y in coords]
		yCoords = [y for x, y in coords]
		if usePyObjC:
			self.scrollMin = ForgeryPoint.ForgeryPoint('object', self, min(xCoords), min(yCoords))
			self.scrollMax = ForgeryPoint.ForgeryPoint('object', self, max(xCoords), max(yCoords))
			#print '[%r adjustScrollbars]' % (self, )
			display('zoomFactor', self.zoomFactor)
			display('center', self.center)
			display('clipSize', self.clipSize)
			display('scrollMin', self.scrollMin)
			display('scrollMax', self.scrollMax)
			#print 'scrollMin', self.scrollMin
			#print 'scrollMin', self.scrollMin.asView
			#print 'scrollMax', self.scrollMax
			#print 'scrollMax', self.scrollMax.asView
			#print
			scrollPos = self.clipMin.asView + self.extraSize.asView
			clipFrameOrigin = self.scrollMin.asView - scrollPos.asView
			clipFrameSize = self.extraSize.asView + self.scrollSize.asView + self.extraSize.asView
			frame = self.frame()
			display('scrollPos', scrollPos)
			display('clipFrameOrigin', clipFrameOrigin)
			display('clipFrameSize', clipFrameSize)
			#print
			display('frame', frame)
			#print 'frame', frame
			#print
			documentVisibleOrigin = ForgeryPoint.ForgeryPoint('view', self, self.scrollView.documentVisibleRect().origin)
			try: # this is a very ugly hack
				documentVisibleOrigin += ForgeryPoint.ForgerySize(self.center).asView - self._scrollDelta
				#documentVisibleOrigin = self._documentVisibleOrigin
			except AttributeError:
				pass
				#documentVisibleOrigin = self.scrollView.documentVisibleRect().origin
			else:
				display('scrollDelta', self._scrollDelta)
				#del self._documentVisibleOrigin
				del self._scrollDelta
			display('documentVisibleOrigin', documentVisibleOrigin)
			#print 'documentVisibleOrigin', documentVisibleOrigin
			#print
			#if tuple(frame.origin) != tuple(clipFrameOrigin) or tuple(frame.size) != tuple(clipFrameSize):
			#	self.setFrame_(NSRect(
			#		clipFrameOrigin,
			#		clipFrameSize,
			#	))
			#print self.scrollView.contentView().bounds()
			#self.scrollPoint_(self.clipMin.asView)
			#self.scrollPoint_(clipMin.asObject)
			#print 'scrollPos', scrollPos
			#if tuple(documentVisibleOrigin) != tuple(scrollPos):
			#	self.scrollPoint_(scrollPos)
			#self.scrollRectToVisible_(NSRect(self.clipMin, self.clipSize))
			#self.scrollView.contentView().scrollToPoint_(self.clipMin.asView)
			#self.refresh()
			#print self.scrollView.contentView().bounds()
			#print tuple(self.scrollMin.asView), tuple(self.scrollMax.asView), tuple(self.scrollSize.asView), tuple(self.clipMin.asView), tuple(self.clipMax.asView), tuple(self.clipSize.asView)
		else:
			self.scrollMin = ForgeryPoint.ForgeryPoint('object', self, min(xCoords), max(yCoords))
			self.scrollMax = ForgeryPoint.ForgeryPoint('object', self, max(xCoords), min(yCoords))
			scrollSize = self.scrollSize.asView
			scrollPos = self.clipMin.asView - self.scrollMin.asView
			scrollSize = self.extraSize + scrollSize + self.extraSize
			scrollPos = ForgeryPoint.ForgeryPoint(self.extraSize + scrollPos)
			#print se;f.extraSize
			#print scrollPos
			#print scrollSize
			#print
			self.SetScrollbar(
				wx.HORIZONTAL,
				int(scrollPos.x),
				int(self.clipSize.asView.x),
				int(scrollSize.x),
			)
			self.SetScrollbar(
				wx.VERTICAL,
				int(scrollPos.y),
				int(self.clipSize.asView.y),
				int(scrollSize.y),
			)
			self.refresh()
	
	@traced
	def zoom(self, factor):
		self.zoomFactor /= factor
		#if usePyObjC:
		#	self.scaleUnitSquareToSize_((factor, factor))
		self.adjustScrollbars()
		self.refresh()
	
	def pan(self, (dx, dy)):
		self.center -= ForgeryPoint.ForgeryPoint('object', self, dx, dy)
		#if usePyObjC:
		#	self.setBoundsOrigin_((-dx, -dy))
		self.adjustScrollbars()
		self.refresh()
	
	def draw(self):
		width, height = self.clipSize.asView
		glViewport(0, 0, int(width - 1), int(height - 1))
		
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		if self.delegate:
			self.delegate.draw()
		else:
			glClearColor(self.backgroundColor[0], self.backgroundColor[1], self.backgroundColor[2], 1.0)
			glClear(GL_COLOR_BUFFER_BIT)
		
		if usePyObjC:
			glFinish()
		else:
			self.SwapBuffers()
	
	@traced
	def setCursor(self, cursor):
		if usePyObjC:
			self.cursor = cursor
			self.window().invalidateCursorRectsForView_(self)
		else:
			self.SetCursor(cursor or ForgeryCursor.arrow)
	
	# PyObjC
	
	@traced
	def awakeFromNib(self):
		self.doInit()
	
	@traced
	def acceptFirstResponder(self):
		return True
	
	def drawRect_(self, aRect):
		self.draw()
	
	@traced
	def mouseEvent_method_(self, event, method):
		pos1 = ForgeryPoint.ForgeryPoint('window', self, event.locationInWindow())
		delta = ForgeryPoint.ForgeryPoint('window', self, event.deltaX(), -event.deltaY()) # not sure why deltaY needs negation
		pos0 = pos1 - delta
		self.mouse1 = pos1.asObject
		self.mouse0 = pos0.asObject
		#print (self.mouse0, self.mouse1)
		modifiers = event.modifierFlags()
		method((
			bool(modifiers & NSCommandKeyMask),
			bool(modifiers & NSAlternateKeyMask),
			bool(modifiers & NSShiftKeyMask),
		))
	
	@traced
	def mouseDown_(self, event):
		self.mouseEvent_method_(event, self.currentMode.mouseDown)
	
	@traced
	def mouseUp_(self, event):
		self.mouseEvent_method_(event, self.currentMode.mouseUp)
		pos = ForgeryPoint.ForgeryPoint('window', self, event.locationInWindow())
		#print pos
		#print pos.changeTo('clip')
		#print pos.changeTo('view')
		#print pos.changeTo('object')
	
	@traced
	def mouseDragged_(self, event):
		self.mouseEvent_method_(event, self.currentMode.mouseDragged)
		#self.autoscroll_(event)
	
	@traced
	def resetCursorRects(self):
		if self.cursor:
			self.addCursorRect_cursor_(self.visibleRect(), self.cursor)
	
	# wxPython
	
	if not usePyObjC:
		
		def __init__(self, *posArgs, **kwdArgs):
			self.document = posArgs[0]
			kwdArgs['style'] = kwdArgs.get('style', 0) | wx.HSCROLL | wx.VSCROLL | wx.ALWAYS_SHOW_SB | wx.WANTS_CHARS
			super(ForgeryView, self).__init__(*posArgs, **kwdArgs)
			
			self.Bind(wx.EVT_KEY_DOWN, errorWrap(self.OnKeyDown))
			self.Bind(wx.EVT_KEY_UP, errorWrap(self.OnKeyUp))
			self.Bind(wx.EVT_ERASE_BACKGROUND, errorWrap(self.OnEraseBackground))
			self.Bind(wx.EVT_PAINT, errorWrap(self.OnRepaint))
			self.Bind(wx.EVT_LEFT_DOWN, errorWrap(self.OnMouseDown))
			self.Bind(wx.EVT_LEFT_UP, errorWrap(self.OnMouseUp))
			self.Bind(wx.EVT_MOTION, errorWrap(self.OnMouseMoved))
			self.Bind(wx.EVT_MOUSEWHEEL, errorWrap(self.OnMouseWheeled))
			self.Bind(wx.EVT_SCROLLWIN_TOP, errorWrap(self.OnScrolledToTop))
			self.Bind(wx.EVT_SCROLLWIN_BOTTOM, errorWrap(self.OnScrolledToBottom))
			self.Bind(wx.EVT_SCROLLWIN_LINEUP, errorWrap(self.OnScrolledLineUp))
			self.Bind(wx.EVT_SCROLLWIN_LINEDOWN, errorWrap(self.OnScrolledLineDown))
			self.Bind(wx.EVT_SCROLLWIN_PAGEUP, errorWrap(self.OnScrolledPageUp))
			self.Bind(wx.EVT_SCROLLWIN_PAGEDOWN, errorWrap(self.OnScrolledPageDown))
			self.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, errorWrap(self.OnScrolledThumbTrack))
			self.Bind(wx.EVT_SIZE, errorWrap(self.OnSized))
			self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
			self.doInit()
	
	def OnEraseBackground(self, event):
		pass # Do nothing, to avoid flashing in Windows.
	
	def OnRepaint(self, event):
		# put a DC on the stack, to be cleaned up when OnRepaint returns
		dc = wx.PaintDC(self)
		self.SetCurrent()
		self.draw()
	
	def OnMouseDown(self, event):
		self.mouse0 = self.mouse1
		self.mouse1 = ForgeryPoint.ForgeryPoint(
			'clip',
			self,
			event.GetPosition(),
		)
		self.CaptureMouse()
		self.currentMode.mouseDown((
			event.CmdDown(),
			event.AltDown(),
			event.ShiftDown(),
		))
	
	def OnMouseUp(self, event):
		self.mouse0 = self.mouse1
		self.mouse1 = ForgeryPoint.ForgeryPoint(
			'clip',
			self,
			event.GetPosition(),
		)
		if self.HasCapture():
			self.currentMode.mouseUp((
				event.CmdDown(),
				event.AltDown(),
				event.ShiftDown(),
			))
			self.ReleaseMouse()
		else:
			event.Skip()
	
	def OnMouseMoved(self, event):
		self.mouse0 = self.mouse1
		self.mouse1 = ForgeryPoint.ForgeryPoint(
			'clip',
			self,
			event.GetPosition(),
		)
		if event.Dragging() and event.LeftIsDown():
			self.OnMouseDragged(event)
	
	def OnMouseDragged(self, event):
		self.currentMode.mouseDragged((
			event.CmdDown(),
			event.AltDown(),
			event.ShiftDown(),
		))
	
	def OnMouseWheeled(self, event):
		try:
			axis = event.GetWheelAxis() # available in CVS on or around 2007-02-04
		except AttributeError:
			axis = wx.VERTICAL
		linesPerAction = event.GetLinesPerAction()
		wheelRotation = event.GetWheelRotation()
		wheelDelta = event.GetWheelDelta()
		delta = WU * linesPerAction * float(wheelRotation) / float(wheelDelta)
		if axis == wx.HORIZONTAL:
			self.center.x += delta
		elif axis == wx.VERTICAL:
			self.center.y += delta
		else: # axis is diagonal?
			raise ValueError, "%r is not %r or %r" % (axis, wx.HORIZONTAL, wx.VERTICAL)
		self.adjustScrollbars()
	
	def OnKeyDown(self, event):
		code = event.GetKeyCode()
		if code in (396, wx.WXK_CONTROL):
			self.OnCommandDown(event)
		elif code == wx.WXK_ALT:
			self.OnOptionDown(event)
		elif code == wx.WXK_SHIFT:
			self.OnShiftDown(event)
		event.Skip()
	
	def OnKeyUp(self, event):
		code = event.GetKeyCode()
		if code in (396, wx.WXK_CONTROL):
			self.OnCommandUp(event)
		elif code == wx.WXK_ALT:
			self.OnOptionUp(event)
		elif code == wx.WXK_SHIFT:
			self.OnShiftUp(event)
		event.Skip()
	
	def OnOptionDown(self, event):
		self.currentMode.optionDown()
		event.Skip()
	
	def OnOptionUp(self, event):
		self.currentMode.optionUp()
		event.Skip()
	
	def OnCommandDown(self, event):
		self.currentMode.commandDown()
		event.Skip()
	
	def OnCommandUp(self, event):
		self.currentMode.commandUp()
		event.Skip()
	
	def OnShiftDown(self, event):
		self.currentMode.shiftDown()
		event.Skip()
	
	def OnShiftUp(self, event):
		self.currentMode.shiftUp()
		event.Skip()
	
	def OnScrolledToTop(self, event):
		orientation = event.GetOrientation()
		zoomFactor = self.zoomFactor
		if orientation == wx.HORIZONTAL:
			coords = [v.x for v in self.data.vertices.itervalues()]
			sizeInPixels = self.sizeInPixels.x
			center = self.center.x
			# include the edges of the currently displayed
			# area in the list of coordinates for consideration
			coords.append(center - zoomFactor * sizeInPixels / 2)
			coords.append(center + zoomFactor * sizeInPixels / 2)
			self.center.x = min(coords) - zoomFactor * sizeInPixels / 2
		elif orientation == wx.VERTICAL:
			coords = [v.y for v in self.data.vertices.itervalues()]
			sizeInPixels = self.sizeInPixels.y
			center = self.center.y
			coords.append(center - zoomFactor * sizeInPixels / 2)
			coords.append(center + zoomFactor * sizeInPixels / 2)
			self.center.y = max(coords) + zoomFactor * sizeInPixels / 2
		else: # orientation is diagonal?
			event.Skip()
			return
		self.adjustScrollbars()
	
	def OnScrolledToBottom(self, event):
		orientation = event.GetOrientation()
		zoomFactor = self.zoomFactor
		if orientation == wx.HORIZONTAL:
			coords = [v.x for v in self.data.vertices.itervalues()]
			sizeInPixels = self.sizeInPixels.x
			center = self.center.x
			# include the edges of the currently displayed
			# area in the list of coordinates for consideration
			coords.append(center - zoomFactor * sizeInPixels / 2)
			coords.append(center + zoomFactor * sizeInPixels / 2)
			self.center.x = max(coords) + zoomFactor * sizeInPixels / 2
		elif orientation == wx.VERTICAL:
			coords = [v.y for v in self.data.vertices.itervalues()]
			sizeInPixels = self.sizeInPixels.y
			center = self.center.y
			# include the edges of the currently displayed
			# area in the list of coordinates for consideration
			coords.append(center - zoomFactor * sizeInPixels / 2)
			coords.append(center + zoomFactor * sizeInPixels / 2)
			self.center.y = min(coords) - zoomFactor * sizeInPixels / 2
		else: # orientation is diagonal?
			event.Skip()
			return
		self.adjustScrollbars()
	
	def OnScrolledLineUp(self, event):
		orientation = event.GetOrientation()
		if orientation == wx.HORIZONTAL:
			self.center.x -= WU
		elif orientation == wx.VERTICAL:
			self.center.y += WU
		else: # orientation is diagonal?
			event.Skip()
			return
		self.adjustScrollbars()
	
	def OnScrolledLineDown(self, event):
		orientation = event.GetOrientation()
		if orientation == wx.HORIZONTAL:
			self.center.x += WU
		elif orientation == wx.VERTICAL:
			self.center.y -= WU
		else: # orientation is diagonal?
			event.Skip()
			return
		self.adjustScrollbars()
	
	def OnScrolledPageUp(self, event):
		orientation = event.GetOrientation()
		if orientation == wx.HORIZONTAL:
			self.center.x -= self.sizeInPixels.x * self.zoomFactor
		elif orientation == wx.VERTICAL:
			self.center.y += self.sizeInPixels.y * self.zoomFactor
		else: # orientation is diagonal?
			event.Skip()
			return
		self.adjustScrollbars()
	
	def OnScrolledPageDown(self, event):
		orientation = event.GetOrientation()
		if orientation == wx.HORIZONTAL:
			self.center.x += self.sizeInPixels.x * self.zoomFactor
		elif orientation == wx.VERTICAL:
			self.center.y -= self.sizeInPixels.y * self.zoomFactor
		else: # orientation is diagonal?
			event.Skip()
			return
		self.adjustScrollbars()
	
	def OnScrolledThumbTrack(self, event):
		orientation = event.GetOrientation()
		currPosition = event.GetPosition()
		zoomFactor = self.zoomFactor
		if orientation == wx.HORIZONTAL:
			coords = [v.x for v in self.data.vertices.itervalues()]
			sizeInPixels = self.sizeInPixels.x
			center = self.center.x
			# include the edges of the currently displayed
			# area in the list of coordinates for consideration
			coords.append(center - zoomFactor * sizeInPixels / 2)
			coords.append(center + zoomFactor * sizeInPixels / 2)
			prevPosition = center - min(coords)
			self.center.x += currPosition * zoomFactor - prevPosition
		elif orientation == wx.VERTICAL:
			coords = [v.y for v in self.data.vertices.itervalues()]
			sizeInPixels = self.sizeInPixels.y
			center = self.center.y
			# include the edges of the currently displayed
			# area in the list of coordinates for consideration
			coords.append(center - zoomFactor * sizeInPixels / 2)
			coords.append(center + zoomFactor * sizeInPixels / 2)
			prevPosition = center - min(coords)
			currPosition = (max(coords) - min(coords)) / zoomFactor - currPosition
			self.center.y += currPosition * zoomFactor - prevPosition
		else: # orientation is diagonal?
			event.Skip()
			return
		self.adjustScrollbars()
	
	def OnSized(self, event):
		self.clipSize = self.sizeInPixels.asView
		self.adjustScrollbars()
		event.Skip()

if __name__ == '__main__':
	import Forgery
	Forgery.main()
