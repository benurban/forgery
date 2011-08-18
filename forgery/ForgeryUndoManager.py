# ForgeryUndoManager.py
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
	'ForgeryUndoManager',
)

if usePyObjC:
	
	from Foundation import *
	from AppKit import *
	import objc

class ForgeryUndoManager(NSObject if usePyObjC else object):
	undoStack = None
	redoStack = None
	isUndoing = False
	isRedoing = False
	
	@property
	def activeStack(self):
		if self.isUndoing:
			return self.redoStack
		else:
			return self.undoStack
	
	top = property(
		fget = lambda self: self.activeStack.__getitem__(-1),
		fset = lambda self, value: self.activeStack.__setitem__(-1, value),
		fdel = lambda self: self.activeStack.__delitem__(-1),
	)
	
	if usePyObjC:
		
		def init(self):
			self = super(ForgeryUndoManager, self).init()
			if self:
				self.flush()
			return self
		
	else:
		
		def __init__(self):
			super(ForgeryUndoManager, self).__init__()
			self.flush()
	
	def flush(self):
		self.undoStack = []
		self.redoStack = []
		self.isUndoing = False
		self.isRedoing = False
		if usePyObjC:
			import ForgeryApplication
			if ForgeryApplication.sharedApplication() and ForgeryApplication.sharedApplication().documents:
				try:
					ForgeryApplication.sharedApplication().frontDocument.updateChangeCount_(NSChangeCleared)
				except TypeError: # this happens when a document is being loaded, when no other documents are open (frontDocument is a generator)
					pass
	
	def undoGroupIsOpen(self):
		try:
			return self.top[0]
		except IndexError:
			return False
	
	def openUndoGroup(self, name = None):
		if self.undoGroupIsOpen():
			self.top[0] += 1
		else:
			if not name:
				name = u"Unspecified Action"
			self.activeStack.append([1, name, []])
		if not self.isUndoing and not self.isRedoing:
			self.redoStack = []
	
	def closeUndoGroup(self, name = None):
		self.top[0] -= 1
		if name:
			self.setUndoGroupName(name)
		if self.top[0] == 0:
			if self.top[2]:
				self.top = (0, self.top[1], tuple(self.top[2]))
				if usePyObjC:
					import ForgeryApplication
					try:
						ForgeryApplication.sharedApplication().frontDocument.updateChangeCount_(NSChangeDone)
					except AttributeError: # this happens when a document is being loaded from a file, when no other documents are open (frontDocument is a list)
						pass
			else: # no actions to undo
				del self.top
	
	def undoableAction(self, undofunc, params):
		self.top[2].append((undofunc, params))
	
	def setUndoGroupName(self, name):
		self.top[1] = name
	
	def undo(self):
		openCount, name, actions = self.undoStack[-1]
		self.isUndoing = True
		self.openUndoGroup(name)
		try:
			for undofunc, params in reversed(actions):
				undofunc(*params)
			if usePyObjC:
				import ForgeryApplication
				ForgeryApplication.sharedApplication().frontDocument.updateChangeCount_(NSChangeUndone)
			del self.undoStack[-1]
		finally:
			self.closeUndoGroup(name)
			self.isUndoing = False
	
	def redo(self):
		openCount, name, actions = self.redoStack[-1]
		self.isRedoing = True
		self.openUndoGroup(name)
		try:
			for undofunc, params in reversed(actions):
				undofunc(*params)
			if usePyObjC:
				import ForgeryApplication
				ForgeryApplication.sharedApplication().frontDocument.updateChangeCount_(NSChangeDone)
			del self.redoStack[-1]
		finally:
			self.closeUndoGroup(name)
			self.isRedoing = False
	
	def isDirty(self):
		# FIXME: check the saved status
		return self.canUndo()
	
	def canUndo(self):
		if self.undoStack:
			return True
		else:
			return False
	
	def canRedo(self):
		if self.redoStack:
			return True
		else:
			return False
	
	def undoText(self):
		try:
			return self.undoStack[-1][1]
		except IndexError:
			return None
	
	def redoText(self):
		try:
			return self.redoStack[-1][1]
		except IndexError:
			return None
