# ForgeryApplication.py
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
	'ForgeryApplication',
	'sharedApplication',
)

if usePyObjC:
	
	from PyObjCTools import NibClassBuilder
	from AppKit import *
	
	Superclass = NibClassBuilder.AutoBaseClass
	
else:
	
	import os, sys
	import wx
	
	import ForgeryDocument
	
	Superclass = wx.App

import ForgeryInspector, ForgeryPalette, ForgeryPreferences

class ForgeryApplication(Superclass):
	_sharedApplication = None
	
	shapesDialogDirectory = None
	openDialogDirectory = None
	saveDialogDirectory = None
	preferences = property(fget = lambda self: ForgeryPreferences.sharedPreferences())
	palette = property(fget = lambda self: ForgeryPalette.sharedPalette())
	inspector = property(fget = lambda self: ForgeryInspector.sharedInspector())
	
	if usePyObjC:
		frontWindow = property(fget = lambda self: self.application.mainWindow())
		documents = property(fget = lambda self: list(self.application.orderedDocuments())[::-1])
	else:
		documents = None
	
	frontDocument = property(fget = lambda self: self.documents and self.documents[-1])
	
	# Shared
	
	@classmethod
	def sharedApplication(cls):
		if not cls._sharedApplication:
			if usePyObjC:
				cls._sharedApplication = NSApplication.sharedApplication().delegate()
			else:
				cls._sharedApplication = cls(False)
		return cls._sharedApplication
	
	def togglePalette(self):
		self.palette.isVisible = not self.palette.isVisible
		self.palette.updateVisibility()
	
	def toggleInspector(self):
		self.inspector.isVisible = not self.inspector.isVisible
		self.inspector.updateVisibility()
	
	# PyObjC
	
	def togglePalette_(self, sender):
		return self.togglePalette()
	
	def toggleInspector_(self, sender):
		return self.toggleInspector()
	
	# wxPython
	
	def OnInit(self):
		self.documents = []
		self.SetExitOnFrameDelete(False)
		wx.InitAllImageHandlers()
		
		self.shapesDialogDirectory = os.getcwd()
		self.openDialogDirectory = os.path.dirname(__file__)
		self.saveDialogDirectory = os.path.dirname(__file__)
		
		return True
	
	def OnTogglePalette(self, event):
		return self.togglePalette()
	
	def OnToggleInspector(self, event):
		return self.toggleInspector()
	
	def MacOpenFile(self, path):
		self.CreateDocument(path)
	
	def CreateDocument(self, path = None):
		document = ForgeryDocument.ForgeryDocument(path)
		document.Bind(wx.EVT_ACTIVATE, self.OnDocumentActivated)
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
