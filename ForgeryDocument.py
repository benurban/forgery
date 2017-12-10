# ForgeryDocument.py
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
	'ForgeryDocument',
)

import ForgeryAlert, ForgeryApplication, ForgeryElements, ForgeryInspector, ForgeryMap, ForgeryMode, ForgeryPalette, ForgeryPreferences, ForgeryUndoManager

if usePyObjC:
	
	from Foundation import *
	from AppKit import *
	from tracer import traced
	import objc
	
else:
	
	import os, sys
	import wx
	
	import ForgeryMenuBar, ForgeryView
	
class ForgeryDocument(NSDocument if usePyObjC else wx.Frame):
	mode = ID.DRAW_MODE
	modes = None
	
	@property
	def currentMode(self):
		return self.modes[self.mode]
	
	@property
	def undoer(self):
		return self.data.undoManager
	# undoManager is reserved for NSDocument
	
	@property
	def app(self):
		return ForgeryApplication.sharedApplication()
	
	snapToGrid = property(
		fget = lambda self: getattr(self.preferences, 'snapToGrid'),
		fset = lambda self, value: setattr(self.preferences, 'snapToGrid', value),
	)
	
	if usePyObjC:
		
		ceilingTextureMode = objc.IBOutlet('ceilingTextureMode')
		#currentMode = objc.IBOutlet('currentMode')
		data = objc.ivar('data')
		drawMode = objc.IBOutlet('drawMode')
		floorTextureMode = objc.IBOutlet('floorTextureMode')
		#path = objc.IBOutlet('path')
		preferences = objc.ivar('preferences')
		statusBar = objc.IBOutlet('statusBar')
		view = objc.IBOutlet('view')
		#window = objc.IBOutlet('window')
		
	else:
		
		path = None
		data = None
		preferences = None
		view = None
		_title = None
		
		menuBar = property(
			fget = lambda self: self.GetMenuBar(),
			fset = lambda self, value: self.SetMenuBar(value),
			fdel = lambda self: self.SetMenuBar(None),
		)
		statusBar = property(
			fget = lambda self: self.GetStatusBar(),
			fset = lambda self, value: self.SetStatusBar(value),
			fdel = lambda self: self.SetStatusBar(None),
		)
		sizer = property(
			fget = lambda self: self.GetSizer(),
			fset = lambda self, value: self.SetSizer(value),
			fdel = lambda self: self.SetSizer(None),
		)
		title = property(
			fget = lambda self: self.__GetTitle(),
			fset = lambda self, value: self.__SetTitle(value),
			fdel = lambda self: self.__SetTitle(""),
		)
	
	# Shared
	
	@traced
	def loadMap(self, path):
		if not self.data:
			if usePyObjC:
				self.data = ForgeryMap.ForgeryMap.alloc().init()
			else:
				self.data = ForgeryMap.ForgeryMap()
		if path:
			with open(path, 'r') as f:
				self.data.readFromXMLFile(f)
		else:
			self.data.flush()
	
	@traced
	def saveMap(self, path):
		with open(path, 'w') as f:
			self.data.writeToXMLFile(f)
	
	@traced
	def openUndoGroup(self, name = None):
		self.undoer.openUndoGroup(name)
	
	@traced
	def closeUndoGroup(self, name = None):
		self.undoer.closeUndoGroup(name)
	
	@traced
	def isDirty(self):
		return self.undoer.isDirty()
	
	@traced
	def canSave(self):
		return self.isDirty()
	
	@traced
	def canUndo(self):
		return self.undoer.canUndo()
	
	@traced
	def canRedo(self):
		return self.undoer.canRedo()
	
	@traced
	def undoText(self):
		text = self.undoer.undoText()
		if text:
			text = u"Undo %s" % (text, )
		else:
			text = u"Can't Undo"
		if not usePyObjC:
			text += u"	CTRL-Z"
		return text
	
	@traced
	def redoText(self):
		text = self.undoer.redoText()
		if text:
			text = u"Redo %s" % (text, )
		else:
			text = u"Can't Redo"
		if not usePyObjC:
			text += u"	CTRL-SHIFT-Z"
		return text
	
	@traced
	def importShapes(self, shapes):
		if shapes:
			self.data.importTextures(shapes)
			[mode.texturesUpdated() for mode in self.modes.itervalues()]
			ForgeryInspector.sharedInspector().texturesUpdated()
	
	@traced
	def undo(self):
		self.undoer.undo()
		self.view.refresh()
		self.view.adjustScrollbars()
		ForgeryInspector.sharedInspector().update()
	
	@traced
	def redo(self):
		self.undoer.redo()
		self.view.refresh()
		self.view.adjustScrollbars()
		ForgeryInspector.sharedInspector().update()
	
	@traced
	def cutSelection(self):
		self.currentMode.cutSelection()
	
	@traced
	def copySelection(self):
		self.currentMode.copySelection()
	
	@traced
	def paste(self):
		self.currentMode.paste()
	
	@traced
	def deleteSelection(self):
		self.currentMode.deleteSelection()
	
	@traced
	def duplicateSelection(self):
		self.currentMode.duplicateSelection()
	
	@traced
	def selectAll(self):
		self.currentMode.selectAll()
	
	@traced
	def selectNone(self):
		self.currentMode.selectNone()
	
	@traced
	def toggleGrid(self):
		self.snapToGrid = not self.snapToGrid
	
	@traced
	def changeMode(self, modeID):
		if modeID != self.mode:
			self.currentMode.deactivate()
			self.mode = modeID
			self.currentMode.activate()
	
	@traced
	def changeTool(self, toolID):
		self.changeMode(ID.DRAW_MODE) # just in case
		self.currentMode.changeTool(toolID)
	
	@traced
	def clearUndoStates(self):
		self.undoer.flush()
	
	@traced
	def updateMenuItem(self, itemID, check, setText):
		dispatchTable = {
			ID.UNDO:                   (None, self.undoText),
			ID.REDO:                   (None, self.redoText),
			ID.TOGGLE_PALETTE:         (None, ForgeryPalette.sharedPalette().toggleText),
			ID.TOGGLE_INSPECTOR:       (None, ForgeryInspector.sharedInspector().toggleText),
			ID.TOGGLE_GRID:            (lambda: self.snapToGrid, None),
		}
		result = self.validateUI(itemID)
		if result is not None:
			checkedFunc, textFunc = dispatchTable.get(itemID, (None, None))
			if checkedFunc:
				check(checkedFunc())
			if textFunc:
				setText(textFunc())
			self.currentMode.updateMenuItem(itemID, check, setText)
		return result
	
	@traced
	def validateUI(self, itemID):
		dispatchTable = {
			ID.NEW:                    True,
			ID.OPEN:                   True,
			ID.CLOSE:                  True,
			ID.SAVE:                   self.canSave,
			ID.SAVEAS:                 True,
			ID.REVERT:                 self.isDirty,
			ID.IMPORT_SHAPES:          True,
			ID.EXIT:                   True,
			ID.UNDO:                   self.canUndo,
			ID.REDO:                   self.canRedo,
			ID.CUT:                    False,
			ID.COPY:                   False,
			ID.PASTE:                  False,
			ID.DELETE:                 False,
			ID.DUPLICATE:              False,
			ID.SELECTALL:              False,
			ID.SELECTNONE:             False,
			ID.PREFERENCES:            False,
			ID.TOGGLE_PALETTE:         True,
			ID.TOGGLE_INSPECTOR:       True,
			ID.TOGGLE_GRID:            True,
		}
		result = self.currentMode.validateUI(itemID)
		if result is None:
			result = dispatchTable.get(itemID, None)
			if callable(result):
				result = result()
		return result
	
	@traced
	def documentActivated(self):
		palette = ForgeryPalette.sharedPalette()
		inspector = ForgeryInspector.sharedInspector()
		self.currentMode.documentActivated()
		inspector.updatePosition()
		inspector.updateVisibility()
		#if usePyObjC and inspector.isDocked: # this fails in multiple ways
		#	self.window.addChildWindow_ordered_(inspector.window(), NSWindowAbove)
		palette.updatePosition()
		palette.updateVisibility()
		#if usePyObjC and palette.isDocked: # this fails in multiple ways
		#	self.window.addChildWindow_ordered_(palette.window(), NSWindowAbove)
	
	@traced
	def documentDeactivated(self):
		#if usePyObjC: # this fails in multiple ways
		#	palette = ForgeryPalette.sharedPalette()
		#	inspector = ForgeryInspector.sharedInspector()
		#	if palette.isDocked:
		#		self.window.removeChildWindow_(palette.window())
		#	if inspector.isDocked:
		#		self.window.removeChildWindow_(inspector.window())
		self.currentMode.documentDeactivated()
	
	@traced
	def sized(self):
		ForgeryPalette.sharedPalette().updatePosition()
		ForgeryInspector.sharedInspector().updatePosition()
	
	@traced
	def moved(self):
		ForgeryPalette.sharedPalette().updatePosition()
		ForgeryInspector.sharedInspector().updatePosition()
	
	if usePyObjC:
		def getFrame(self):
			frame = self.window.frame()
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
	
	if usePyObjC: # PyObjC
		
		@traced
		def init(self):
			self = super(ForgeryDocument, self).init()
			if self:
				self.setHasUndoManager_(False)
				self.data = ForgeryMap.ForgeryMap.alloc().init()
				self.preferences = ForgeryPreferences.sharedPreferences().createDocument(self.data)
			return self
		
		@traced
		def windowNibName(self):
			return u'ForgeryDocument'
		
		@traced
		def windowControllerDidLoadNib_(self, controller):
			super(ForgeryDocument, self).windowControllerDidLoadNib_(controller)
			self.window = controller.window()
			modes = (self.drawMode, self.floorTextureMode, self.ceilingTextureMode)
			self.modes = dict((mode.modeID, mode) for mode in modes)
			self.currentMode.activate()
			#self.preferences.update(ForgeryPreferences.sharedPreferences())
			ForgeryInspector.sharedInspector().updatePosition()
			ForgeryInspector.sharedInspector().updateVisibility()
			ForgeryPalette.sharedPalette().updatePosition()
			ForgeryPalette.sharedPalette().updateVisibility()
		
		@objc.IBAction
		@traced
		def importShapes_(self, sender):
			panel = NSOpenPanel.openPanel()
			panel.setAllowsMultipleSelection_(False)
			result = panel.runModalForDirectory_file_types_('/Applications/AlephOne', None, ['shpA', NSFileTypeForHFSTypeCode('shpA')]) #NSHomeDirectory()
			if result == NSOKButton:
				self.importShapes(panel.filenames()[0])
		
		@objc.IBAction
		@traced
		def undo_(self, sender):
			self.undo()
		
		@objc.IBAction
		@traced
		def reallyUndo_(self, sender):
			self.undo()
		
		@objc.IBAction
		@traced
		def redo_(self, sender):
			self.redo()
		
		@objc.IBAction
		@traced
		def reallyRedo_(self, sender):
			self.redo()
		
		@objc.IBAction
		@traced
		def dumpUndoState_(self, sender): # not used
			print self.undoer.undoStack
			print self.undoer.redoStack
		
		@objc.IBAction
		@traced
		def cut_(self, sender):
			self.cutSelection()
		
		@objc.IBAction
		@traced
		def copy_(self, sender):
			self.copySelection()
		
		@objc.IBAction
		@traced
		def paste_(self, sender):
			self.paste()
		
		@objc.IBAction
		@traced
		def delete_(self, sender):
			self.deleteSelection()
		
		@objc.IBAction
		@traced
		def duplicate_(self, sender):
			self.duplicateSelection()
		
		@objc.IBAction
		@traced
		def selectAll_(self, sender):
			self.selectAll()
		
		@objc.IBAction
		@traced
		def selectNone_(self, sender):
			self.selectNone()
		
		@objc.IBAction
		@traced
		def changeMode_(self, sender):
			self.changeMode(sender.tag())
		
		@objc.IBAction
		@traced
		def changeTool_(self, sender):
			self.changeTool(sender.tag())
		
		@objc.IBAction
		@traced
		def toggleGrid_(self, sender):
			self.toggleGrid()
		
		@traced
		def validateMenuItem_(self, item):
			result = self.updateMenuItem(
				item.tag(),
				item.setState_,
				item.setTitle_,
			)
			if result is None:
				return super(ForgeryDocument, self).validateMenuItem_(item)
			else:
				return result
		
		@traced
		def validateUserInterfaceItem_(self, item):
			result = self.validateUI(item.tag())
			if result is None:
				return super(ForgeryDocument, self).validateUserInterfaceItem_(item)
			else:
				return result
		
		@traced
		def windowDidBecomeMain_(self, notification):
			self.documentActivated()
		
		@traced
		def windowWillResignMain_(self, notification): # this seems to be undocumented
			self.documentDeactivated()
			return super(ForgeryDocument, self).windowWillResignMain_(notification)
		
		@traced
		def windowWillClose_(self, notification):
			if len(self.app.documents) < 2:
				ForgeryInspector.sharedInspector().hide()
				ForgeryPalette.sharedPalette().hide()
		
		@traced
		def windowDidResize_(self, notification):
			self.sized()
		
		@traced
		def windowDidMove_(self, notification):
			self.moved()
		
		@traced
		def readFromFile_ofType_(self, path, typ):
			self.loadMap(path)
			self.preferences.update(self.data['preferences'])
			return True
		
		@traced
		def writeToFile_ofType_(self, path, typ):
			self.saveMap(path)
			return True
		
		@traced
		def dataOfType_error_(self, typeName, outError):
			return None, NSError.errorWithDomain_code_userInfo_(NSOSStatusErrorDomain, -4, None) # -4 is unimpErr from CarbonCore
		
		@traced
		def readFromData_ofType_error_(self, data, typeName, outError):
			return objc.NO, NSError.errorWithDomain_code_userInfo_(NSOSStatusErrorDomain, -4, None) # -4 is unimpErr from CarbonCore
		
	else: # wxPython
		
		def __init__(self, path = None, title = None):
			super(ForgeryDocument, self).__init__(
				None,
				style = wx.DEFAULT_FRAME_STYLE,
			)
			self.path = path
			if path:
				self.title = os.path.basename(path)
			elif title:
				self.title = title
			else:
				self.title = u"untitled"
			
			self.data = ForgeryMap.ForgeryMap()
			self.loadMap(self.path)
			#self.preferences = ForgeryPreferences.sharedPreferences()
			self.preferences = ForgeryPreferences.sharedPreferences().createDocument(self.data['preferences'])
			
			self.app.documents.append(self)
			
			self.menuBar = self.SetupMenuBar()
			self.statusBar = self.SetupStatusBar()
			self.sizer = wx.BoxSizer(wx.VERTICAL)
			
			self.view = ForgeryView.ForgeryView(self, -1)
			self.sizer.Add(self.view, 1, wx.EXPAND, 0)
			
			# wx does not let me set the actual size; only the minimum size
			self.sizer.SetMinSize(self.preferences.windowSize)
			self.sizer.Fit(self)
			self.sizer.SetMinSize(wx.DefaultSize)
			
			self.Layout()
			
			if self.preferences.windowPosition:
				self.Move(self.preferences.windowPosition)
			
			self.Bind(wx.EVT_UPDATE_UI, errorWrap(self.OnUpdateUI))
			self.Bind(wx.EVT_MOVE, errorWrap(self.OnMoved))
			self.Bind(wx.EVT_SIZE, errorWrap(self.OnSized))
			self.Bind(wx.EVT_CLOSE, errorWrap(self.OnClose))
			
			self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
			
			self.modes = ForgeryMode.modes.copy()
			for modeID, mode in self.modes.iteritems():
				self.modes[modeID] = mode(self)
			
			self.currentMode.activate()
		
		def SetupMenuBar(self):
			result = wx.MenuBar()
			ForgeryMenuBar.CreateMenu(self, ForgeryMenuBar.menus, result)
			result.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
			return result
			
		def SetupStatusBar(self):
			result = self.CreateStatusBar(1, 0, ID.STATUS_BAR)
			result.Bind(wx.EVT_UPDATE_UI, errorWrap(self.OnUpdateStatusBar))
			result.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
			return result
		
		def __GetTitle(self): # no clue why GetTitle takes so long
			return self._title
		
		def __SetTitle(self, value):
			self.SetTitle(value)
			self._title = value
		
		def OnSaveDocument(self, event):
			if self.path:
				self.saveMap(self.path)
				return True
			else:
				return self.OnSaveDocumentAs(event)
		
		def OnSaveDocumentAs(self, event):
			path = self.app.SaveDialog(self)
			if path:
				self.path = path
				self.SetTitle(os.path.basename(self.path))
				self.OnSaveDocument(event)
				return True
			else:
				return False
		
		def OnRevertDocument(self, event):
			if self.ConfirmRevertDialog() == ID.YES:
				self.loadMap(self.path)
				self.view.refresh()
		
		def OnClose(self, event):
			try:
				if event.CanVeto() and self.isDirty():
					result = self.ConfirmCloseDialog()
					if result == ID.SAVE:
						if self.OnSaveDocument(event):
							self.CloseDocument()
						else:
							event.Veto() # save was cancelled
					elif result == ID.NO:
						self.CloseDocument()
					else: # result == ID.CANCEL
						event.Veto()
				else:
					self.CloseDocument()
			except:
				event.Veto()
				raise
		
		def OnImportShapes(self, event):
			self.importShapes(self.app.ShapesDialog())
		
		def OnUndo(self, event):
			self.undo()
		
		def OnRedo(self, event):
			self.redo()
		
		def DispatchCommand(self, event):
			if not self.currentMode.doMenu(event.GetID()):
				event.Skip()
		
		def OnCut(self, event):
			self.cutSelection()
		
		def OnCopy(self, event):
			self.copySelection()
		
		def OnPaste(self, event):
			self.paste()
		
		def OnDelete(self, event):
			self.deleteSelection()
		
		def OnDuplicate(self, event):
			self.duplicateSelection()
		
		def OnSelectAll(self, event):
			self.selectAll()
		
		def OnSelectNone(self, event):
			self.selectNone()
		
		def OnChangeMode(self, event):
			return self.changeMode(event.GetId())
		
		def OnToggleGrid(self, event):
			self.toggleGrid()
		
		def OnUpdateUI(self, event):
			enabled = self.updateMenuItem(
				event.GetId(),
				event.Check,
				event.SetText,
			)
			if enabled is None:
				event.Skip()
			else:
				event.Enable(enabled)
		
		def OnSized(self, event):
			self.sized()
			event.Skip()
		
		def OnMoved(self, event):
			self.moved()
			event.Skip()
		
		def OnUpdateStatusBar(self, event):
			self.SetStatusText(self.currentMode.getStatusText())
		
		def CloseDocument(self):
			self.currentMode.documentClosed()
			del self.app.documents[self.app.documents.index(self)]
			if not self.app.documents:
				self.app.OnQuit(None)
			self.Destroy()
		
		def ConfirmRevertDialog(self):
			return ForgeryAlert.runApplicationModalAlert(
				u"Are you sure you want to revert to the previously saved version of \"%s\"?" % (self.title, ),
				u"You will lose all of the changes you made since you last saved the document.",
				(ID.CANCEL, ID_YES),
			)
		
		def ConfirmCloseDialog(self):
			return ForgeryAlert.runApplicationModalAlert(
				u"The document \"%s\" has not been saved" % (self.title, ),
				u"Your changes will be lost if you close the document\nwithout saving.",
				(ID.SAVE, ID.DONTSAVE, ID.CANCEL),
			)
