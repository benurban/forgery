# ForgeryProgressWindow.py
# Forgery

# Copyright (c) 2011 by Ben Urban <benurban@users.sourceforge.net>.
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

if usePyObjC:
	from Foundation import *
	from AppKit import *
	import objc
else:
	import wx

from tracer import traced

class ForgeryProgressWindow(NSWindowController if usePyObjC else wx.Frame):
	label = objc.IBOutlet('label') if usePyObjC else None
	progressBar = objc.IBOutlet('progressBar') if usePyObjC else None
	cancelButton = objc.IBOutlet('cancelButton') if usePyObjC else None
	currentItemLabel = objc.IBOutlet('currentItemLabel') if usePyObjC else None
	progressLabel = objc.IBOutlet('progressLabel') if usePyObjC else None
	cancelAction = objc.ivar('cancelAction') if usePyObjC else None
	
	@traced
	def setup(self, title, label = u"", cancelAction = None):
		if usePyObjC:
			self.setupWithTitle_label_cancelAction_(title, label, cancelAction)
		else:
			pass # FIXME: wx
	
	@traced
	def setCancelAction(self, cancelAction):
		self.cancelAction = cancelAction
		if usePyObjC:
			self.cancelButton.setEnabled_(True if self.cancelAction else False)
		else:
			pass # FIXME: wx
	
	@traced
	def setProgressMaximum(self, maximum):
		if usePyObjC:
			self.progressBar.setIndeterminate_(False)
			self.progressBar.setMinValue_(0.0)
			self.progressBar.setDoubleValue_(0.0)
			self.progressBar.setMaxValue_(maximum)
			self.currentItemLabel.setStringValue_(u"")
			self.currentItemLabel.setHidden_(False)
			self.progressLabel.setStringValue_(u"")
			self.progressLabel.setHidden_(False)
		else:
			pass # FIXME: wx
	
	@traced
	def updateProgress(self, progress, currentItem, progressText):
		if usePyObjC:
			self.performSelectorOnMainThread_withObject_waitUntilDone_('doUpdateProgress:', (progressText, currentItem, progress), True)
		else:
			pass # FIXME: wx
	
	@traced
	def cleanUp(self):
		if usePyObjC:
			self.window().performSelectorOnMainThread_withObject_waitUntilDone_('orderOut:', self, True)
		else:
			pass # FIXME: wx
	
	if usePyObjC:
		@traced
		def init(self):
			self = super(ForgeryProgressWindow, self).init()
			return self
		
		@traced
		def setupWithTitle_label_cancelAction_(self, title, label, cancelAction):
			self.window().setTitle_(title)
			self.label.setStringValue_(label)
			self.progressBar.setIndeterminate_(True)
			self.progressBar.setMinValue_(0.0)
			self.progressBar.setDoubleValue_(0.0)
			self.progressBar.setMaxValue_(100.0)
			self.setCancelAction(cancelAction)
			self.currentItemLabel.setStringValue_(u"")
			self.currentItemLabel.setHidden_(True)
			self.progressLabel.setStringValue_(u"")
			self.progressLabel.setHidden_(True)
			self.window().makeKeyAndOrderFront_(self)
		
		@traced
		def updateProgress_currentItem_amount_(self, progressText, currentItem, progress):
			self.progressBar.setDoubleValue_(progress)
			self.currentItemLabel.setStringValue_(currentItem)
			self.progressLabel.setStringValue_(progressText)
		
		@traced
		def doUpdateProgress_(self, params):
			self.updateProgress_currentItem_amount_(*params)
		
		@objc.IBAction
		@traced
		def cancelClicked_(self, sender):
			self.cancelAction()
