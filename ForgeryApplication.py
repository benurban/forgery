# ForgeryApplication.py
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
	'ForgeryApplication',
	'sharedApplication',
)

if usePyObjC:
	
	from Foundation import *
	from AppKit import *
	from tracer import traced
	import objc
	
else:
	
	import os, sys
	import wx
	
	import ForgeryDocument

import ForgeryInspector, ForgeryPalette, ForgeryPreferences

class ForgeryApplication(NSObject if usePyObjC else wx.App):
	shapesDialogDirectory = None
	openDialogDirectory = None
	saveDialogDirectory = None
	
	if usePyObjC:
		application = objc.IBOutlet('application')
		preferences = objc.IBOutlet('preferences')
		palette = objc.IBOutlet('palette')
		inspector = objc.IBOutlet('inspector')
		progressWindow = objc.IBOutlet('progressWindow')
		
		@property
		def frontWindow(self):
			return self.application.mainWindow()
		@property
		def documents(self):
			return list(reversed(self.application.orderedDocuments()))
	else:
		documents = None
		@property
		def preferences(self):
			return ForgeryPreferences.sharedPreferences()
		@property
		def palette(self):
			return ForgeryPalette.sharedPalette()
		@property
		def inspector(self):
			return ForgeryInspector.sharedInspector()
	
	@property
	def frontDocument(self):
		return self.documents[-1] if self.documents else None
	
	# Shared
	
	_sharedApplication = None
	@classmethod
	def sharedApplication(Class):
		if not Class._sharedApplication:
			if usePyObjC:
				if not NSApplication.sharedApplication().delegate():
					NSApplication.sharedApplication().setDelegate_(Class.alloc().init())
				Class._sharedApplication = NSApplication.sharedApplication().delegate()
			else:
				Class._sharedApplication = Class(False)
		return Class._sharedApplication
	
	@traced
	def init(self):
		self = super(ForgeryApplication, self).init()
		if self and not ForgeryApplication._sharedApplication:
			ForgeryApplication._sharedApplication = self
		return self
	
	@traced
	def togglePalette(self):
		self.palette.isVisible = not self.palette.isVisible
		self.palette.updateVisibility()
	
	@traced
	def toggleInspector(self):
		self.inspector.isVisible = not self.inspector.isVisible
		self.inspector.updateVisibility()
	
	if usePyObjC:
		
		@objc.IBAction
		@traced
		def togglePalette_(self, sender):
			return self.togglePalette()
		
		@objc.IBAction
		@traced
		def toggleInspector_(self, sender):
			return self.toggleInspector()
		
	else:
		
		def OnInit(self):
			self.documents = []
			self.SetExitOnFrameDelete(False)
			wx.InitAllImageHandlers()
			
			self.shapesDialogDirectory = os.getcwd() # FIXME: 
			self.openDialogDirectory = os.path.dirname(__file__) # FIXME: 
			self.saveDialogDirectory = os.path.dirname(__file__) # FIXME: 
			
			return True
		
		def OnTogglePalette(self, event):
			return self.togglePalette()
		
		def OnToggleInspector(self, event):
			return self.toggleInspector()
		
		def MacOpenFile(self, path):
			self.CreateDocument(path)
		
		def CreateDocument(self, path = None):
			document = ForgeryDocument.ForgeryDocument(path)
			document.Bind(wx.EVT_ACTIVATE, errorWrap(self.OnDocumentActivated))
			self.SetTopWindow(document)
			document.Show() # this also activates the document
			return document
		
		def ShapesDialog(self):
			dialog = wx.FileDialog(
				self.frontDocument,
				defaultDir = self.shapesDialogDirectory,
				style = wx.OPEN | wx.FILE_MUST_EXIST,
				wildcard = "AlephOne Shapes File (*.shpA)|*.shpA|All Files (*.*)|*.*",
			)
			try:
				response = dialog.ShowModal()
				self.shapesDialogDirectory = dialog.GetDirectory()
				path = dialog.GetPath()
			finally:
				dialog.Destroy()
			if response == wx.ID_OK:
				self.shapesDialogDirectory = os.path.dirname(path)
				result = path
			else:
				result = None
			return result
		
		def OpenDialog(self):
			dialog = wx.FileDialog(
				self.frontDocument,
				defaultDir = self.openDialogDirectory,
				style = wx.OPEN | wx.FILE_MUST_EXIST | wx.MULTIPLE,
				wildcard = "Forgery XML Map (*.sceB)|*.sceB|All Files (*.*)|*.*",
			)
			try:
				response = dialog.ShowModal()
				self.openDialogDirectory = dialog.GetDirectory()
				paths = dialog.GetPaths()
			finally:
				dialog.Destroy()
			if response == ID.OK:
				self.openDialogDirectory = os.path.dirname(paths[0])
				result = paths
			else:
				result = []
			return result
		
		def SaveDialog(self, document):
			if document.path:
				directory = os.path.dirname(document.path)
			else:
				directory = self.saveDialogDirectory
			if document.path:
				filename = os.path.basename(document.path)
			else:
				filename = document.title + '.sceB'
			dialog = wx.FileDialog(
				document,
				style = wx.SAVE,
				defaultDir = directory,
				defaultFile = filename,
				wildcard = "Forgery XML Map (*.sceB)|*.sceB",
			)
			try:
				response = dialog.ShowModal()
				self.saveDialogDirectory = dialog.GetDirectory()
				path = dialog.GetPath()
			finally:
				dialog.Destroy()
			if response == ID.OK:
				# FIXME: Confirm replacement if necessary
				self.saveDialogDirectory = os.path.dirname(path)
				result = path
			else:
				result = None
			return result
		
		def OnNewDocument(self, event):
			self.CreateDocument()
		
		def OnOpenDocument(self, event):
			for path in self.OpenDialog():
				for document in self.documents:
					if document.path == path:
						document.Raise()
						self.SetTopWindow(document)
						break
				else:
					self.CreateDocument(path)
		
		def OnCloseDocument(self, event):
			return self.frontDocument.Close()
		
		def OnQuit(self, event):
			while self.documents:
				if not self.frontDocument.Close(): # the close has been vetoed
					return False
			else:
				self.palette.Close(True)
				self.inspector.Close(True)
				self.ExitMainLoop()
				return True
		
		def OnDocumentActivated(self, event):
			if event.GetActive():
				self.documents.append(self.documents.pop(self.documents.index(event.GetEventObject())))
				event.GetEventObject().documentActivated()
			else:
				event.GetEventObject().documentDeactivated()
			event.Skip()

def sharedApplication():
	return ForgeryApplication.sharedApplication()
