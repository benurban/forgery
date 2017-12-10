# ForgeryAlert.py
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
from tracer import traced

__all__ = (
	'runApplicationModalAlert',
	'runWindowModalAlert',
)

import ForgeryApplication
import os

if usePyObjC:
	
	from Foundation import *
	from AppKit import *
	
	buttonText = {
		ID.APPLY:  u"Apply",
		ID.CANCEL: u"Cancel",
		ID.NO:     u"No",
		ID.OK:     u"OK",
		ID.SAVE:   u"Save",
		ID.YES:    u"Yes",
	}
	dontSaveText = u"Don't Save"
	
else:
	
	import wx
	
	buttonText = {
		ID.APPLY:  u"&Apply",
		ID.CANCEL: u"&Cancel",
		ID.NO:     u"&No",
		ID.OK:     u"&OK",
		ID.SAVE:   u"&Save",
		ID.YES:    u"&Yes",
	}
	dontSaveText = u"&Don't Save"

def runApplicationModalAlert(messageText, informativeText, buttons):
	if usePyObjC:
		
		alert = NSAlert.alloc().init()
		alert.setMessageText_(messageText)
		if informativeText:
			alert.setInformativeText_(informativeText)
		for buttonID in buttons:
			alert.addButtonWithTitle_(buttonText[buttonID]).setTag_(buttonID)
		return alert.runModal()
		
	else: # this shouldn't be nearly this complex
		
		# the numbers in here come from Apple's HIG
		dialog = wx.Dialog(ForgeryApplication.sharedApplication().frontDocument, style = 0)
		try:
			dialog.Centre(wx.BOTH)
			#text = wx.TextCtrl(dialog, wx.NewId(), style = wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH | wx.TE_LEFT | wx.TE_BESTWRAP)
			#style = wx.TextAttr()
			#style.SetFont(wx.Font(
			#	13,
			#	wx.FONTFAMILY_DEFAULT,
			#	wx.FONTSTYLE_NORMAL,
			#	wx.FONTWEIGHT_BOLD,
			#))
			#text.SetDefaultStyle(style)
			#text.AppendText(messageText)
			#style.SetFont(wx.Font(
			#	11,
			#	wx.FONTFAMILY_DEFAULT,
			#	wx.FONTSTYLE_NORMAL,
			#	wx.FONTWEIGHT_NORMAL,
			#))
			#text.SetDefaultStyle(style)
			#text.AppendText("\n")
			#text.AppendText(informativeText)
			
			buttonSizer = dialog.CreateStdDialogButtonSizer(0)
			
			buttons = set(buttons)
			
			if buttons == set([ID.SAVE, ID.DONTSAVE, ID.CANCEL]):
				
				dialog.Bind(wx.EVT_KEY_DOWN, lambda event: (event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER)) and dialog.EndModal(ID.SAVE) or event.Skip())
				addButton(dialog, buttonSizer, ID.SAVE).SetDefault()
				addButton(dialog, buttonSizer, ID.DONTSAVE, dontSaveText)
				addButton(dialog, buttonSizer, ID.CANCEL)
				
			else:
				
				if ID.APPLY in buttons:
					addButton(dialog, buttonSizer, ID.APPLY)
					buttons.remove(ID.APPLY)
				
				if ID.CANCEL in buttons:
					addButton(dialog, buttonSizer, ID.CANCEL)
					buttons.remove(ID.CANCEL)
				
				if ID.NO in buttons:
					addButton(dialog, buttonSizer, ID.NO)
					buttons.remove(ID.NO)
				
				if ID.OK in buttons:
					dialog.Bind(wx.EVT_KEY_DOWN, lambda event: (event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER)) and dialog.EndModal(ID.OK) or event.Skip())
					addButton(dialog, buttonSizer, ID.OK).SetDefault()
					buttons.remove(ID.OK)
				
				if ID.YES in buttons:
					dialog.Bind(wx.EVT_KEY_DOWN, lambda event: (event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER)) and dialog.EndModal(ID.YES) or event.Skip())
					addButton(dialog, buttonSizer, ID.YES).SetDefault()
					buttons.remove(ID.YES)
			
			buttonSizer.Realize()
			
			sizer = buildSizers(
				wx.HORIZONTAL,
				24,
				(
					15,
					wx.StaticBitmap(dialog, -1, wx.BitmapFromImage(wx.Image(os.path.join(resourcesDir, 'Forgery.png')).Scale(64, 64))),
					20,
				),
				16,
				(
					15,
					wx.StaticText(
						dialog,
						wx.NewId(),
						messageText,
					),
					8,
					wx.StaticText(
						dialog,
						wx.NewId(),
						informativeText,
					),
					10, # None,
					buttonSizer,
					20,
				),
				24,
			)
			dialog.SetSizer(sizer)
			sizer.Fit(dialog)
			dialog.Layout()
			result = dialog.ShowModal()
		finally:
			dialog.Destroy()
		return result

def runWindowModalAlert(window, alertFunc, messageText, informativeText, buttons):
	if usePyObjC:
		
		alert = NSAlert.alloc().init()
		alert.setMessageText_(messageText)
		if informativeText:
			alert.setInformativeText_(informativeText)
		for buttonID in buttons:
			alert.addButtonWithTitle_(buttonText[buttonID]).setTag_(buttonID)
		alert.beginSheetModalForWindow_modalDelegate_didEndSelector_contextInfo_(window, ForgeryWindowModalAlertDelegate.alloc().initWithFunc_(alertFunc), 'alertDidEnd:returnCode:contextInfo:', None)
		
	else:
		alertFunc(runApplicationModalAlert(messageText, informativeText, buttons))

if usePyObjC:
	
	class ForgeryWindowModalAlertDelegate(NSObject):
		func = None
		
		@traced
		def initWithFunc_(self, func):
			self = super(ForgeryWindowModalAlertDelegate, self).init()
			if self:
				self.func = func
			return self
		
		@traced
		def alertDidEnd_returnCode_contextInfo_(self, alert, result, context):
			alert.window().orderOut_(alert)
			self.func(result)
	
else:
	
	def addButton(dialog, sizer, buttonID, name = None):
		if not name:
			name = buttonText[buttonID]
		result = wx.Button(dialog, buttonID, name)
		result.Bind(wx.EVT_BUTTON, lambda event: dialog.EndModal(buttonID))
		sizer.AddButton(result)
		return result
