# ForgeryTool.py
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
	'ForgeryTool',
	'tools',
)

import ForgeryCursor
from tracer import traced

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
	
	@property
	def preferences(self):
		return self.document.preferences
	@property
	def snapToGrid(self):
		return self.preferences.snapToGrid
	@property
	def gridSpacing(self):
		return self.preferences.gridSpacing
	@property
	def view(self):
		return self.document.view
	@property
	def viewDelegate(self):
		return self.view.delegate
	@property
	def realGridSpacing(self):
		return self.viewDelegate.realGridSpacing
	@property
	def toolData(self):
		return self.viewDelegate._toolData
	@property
	def mouse0(self):
		return self.view.mouse0
	@property
	def mouse1(self):
		return self.view.mouse1
	@property
	def data(self):
		return self.document.data
	@property
	def zoomFactor(self):
		return self.view.zoomFactor
	@property
	def center(self):
		return self.view.center
	@property
	def player(self):
		return self.view.player
	
	def __init__(self, document):
		super(ForgeryTool, self).__init__()
		self.document = document
		if usePyObjC:
			self.icon = NSImage.imageNamed_(self.iconFileName)
		else:
			self.icon = wx.Bitmap(os.path.join(resourcesDir, self.iconFileName))
	
	@traced
	def refresh(self):
		return self.view.refresh()
	
	@traced
	def openUndoGroup(self, name = None):
		return self.document.openUndoGroup(name)
	
	@traced
	def closeUndoGroup(self, name = None):
		return self.document.closeUndoGroup(name)
	
	@traced
	def addDrawHook(self, hook):
		return self.viewDelegate.addDrawHook(hook)
	
	@traced
	def removeDrawHook(self, hook):
		return self.viewDelegate.removeDrawHook(hook)
	
	@traced
	def adjustScrollbars(self):
		return self.view.adjustScrollbars()
	
	@traced
	def activate(self):
		self.setCursor(self.cursor)
	
	@traced
	def deactivate(self):
		self.setCursor(None)
	
	@traced
	def setCursor(self, cursor):
		self.view.setCursor(cursor)
	
	@traced
	def validateUI(self, itemID):
		return None
	
	@traced
	def getStatusText(self):
		return u""
	
	@traced
	def cutSelection(self):
		pass
	
	@traced
	def copySelection(self):
		pass
	
	@traced
	def paste(self):
		pass
	
	@traced
	def deleteSelection(self):
		pass
	
	@traced
	def duplicateSelection(self):
		pass
	
	@traced
	def selectAll(self):
		pass
	
	@traced
	def selectNone(self):
		pass
	
	@traced
	def doubleClick(self):
		pass
	
	@traced
	def mouseUp(self, modifiers):
		print "mouseUp at (%s, %s)" % tuple(self.mouse1)
	
	@traced
	def mouseDown(self, modifiers):
		print "mouseDown at (%s, %s)" % tuple(self.mouse1)
	
	def mouseDragged(self, modifiers):
		print "mouseDragged from (%s, %s) to (%s, %s)" % (tuple(self.mouse0) + tuple(self.mouse1))
	
	@traced
	def commandDown(self):
		pass
	
	@traced
	def commandUp(self):
		pass
	
	@traced
	def optionDown(self):
		pass
	
	@traced
	def optionUp(self):
		pass
	
	@traced
	def shiftDown(self):
		pass
	
	@traced
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
