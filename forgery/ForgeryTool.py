# ForgeryTool.py
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
	'ForgeryTool',
	'tools',
)

import ForgeryCursor

if usePyObjC:
	from AppKit import *
else:
	import wx
	import os

class ForgeryTool(object):
	iconFileName = None
	icon = None
	cursor = ForgeryCursor.arrow
	toolID = None
	position = None
	document = None
	
	vertexSelectionRadius = 5
	
	preferences = property(fget = lambda self: self.document.preferences)
	snapToGrid = property(fget = lambda self: self.preferences.snapToGrid)
	gridSpacing = property(fget = lambda self: self.preferences.gridSpacing)
	view = property(fget = lambda self: self.document.view)
	viewDelegate = property(fget = lambda self: self.view.delegate)
	realGridSpacing = property(fget = lambda self: self.viewDelegate.realGridSpacing)
	toolData = property(fget = lambda self: self.viewDelegate._toolData)
	mouse0 = property(fget = lambda self: self.view.mouse0)
	mouse1 = property(fget = lambda self: self.view.mouse1)
	data = property(fget = lambda self: self.document.data)
	zoomFactor = property(fget = lambda self: self.view.zoomFactor)
	center = property(fget = lambda self: self.view.center)
	player = property(fget = lambda self: self.view.player)
	
	def __init__(self, document):
		super(ForgeryTool, self).__init__()
		self.document = document
		if usePyObjC:
			self.icon = NSImage.imageNamed_(self.iconFileName)
		else:
			self.icon = wx.Bitmap(os.path.join(resourcesDir, self.iconFileName))
	
	def refresh(self):
		return self.view.refresh()
	
	def openUndoGroup(self, name = None):
		return self.document.openUndoGroup(name)
	
	def closeUndoGroup(self, name = None):
		return self.document.closeUndoGroup(name)
	
	def addDrawHook(self, hook):
		return self.viewDelegate.addDrawHook(hook)
	
	def removeDrawHook(self, hook):
		return self.viewDelegate.removeDrawHook(hook)
	
	def adjustScrollbars(self):
		return self.view.adjustScrollbars()
	
	def activate(self):
		self.setCursor(self.cursor)
	
	def deactivate(self):
		self.setCursor(None)
	
	def setCursor(self, cursor):
		self.view.setCursor(cursor)
	
	def validateUI(self, itemID):
		return None
	
	def getStatusText(self):
		return ""
	
	def cutSelection(self):
		pass
	
	def copySelection(self):
		pass
	
	def paste(self):
		pass
	
	def deleteSelection(self):
		pass
	
	def duplicateSelection(self):
		pass
	
	def selectAll(self):
		pass
	
	def selectNone(self):
		pass
	
	def doubleClick(self):
		pass
	
	def mouseUp(self, modifiers):
		print "mouseUp at (%s, %s)" % tuple(self.mouse1)
	
	def mouseDown(self, modifiers):
		print "mouseDown at (%s, %s)" % tuple(self.mouse1)
	
	def mouseDragged(self, modifiers):
		print "mouseDragged from (%s, %s) to (%s, %s)" % (tuple(self.mouse0) + tuple(self.mouse1))
	
	def commandDown(self):
		pass
	
	def commandUp(self):
		pass
	
	def optionDown(self):
		pass
	
	def optionUp(self):
		pass
	
	def shiftDown(self):
		pass
	
	def shiftUp(self):
		pass

tools = {}

import ForgerySelectTool
import ForgeryLineTool
import ForgeryRegularPolygonTool
import ForgeryFillTool
import ForgeryPanTool
import ForgeryZoomTool
import ForgeryTextTool
import ForgeryObjectTool
