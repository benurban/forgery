# ForgeryCursor.py
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
	'getCursorFromFile',
	'arrow',
	'bucket',
	'closedHand',
	'cross',
	'openHand',
	'zoomIn',
	'zoomOut',
)

if usePyObjC:
	
	from AppKit import *
	
	def getCursorFromFile(filename, (x, y)):
		return NSCursor.alloc().initWithImage_hotSpot_(
			NSImage.imageNamed_(filename),
			(x, y),
		)
	
else:
	
	import wx
	import os

	def getCursorFromFile(filename, (x, y)):
		image = wx.Image(os.path.join(resourcesDir, filename))
		image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, x)
		image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, y)
		return wx.CursorFromImage(image)

arrow = None
bucket = None
closedHand = None
cross = None
openHand = None
zoomIn = None
zoomOut = None

def initCursors():
	global arrow, bucket, closedHand, cross, openHand, zoomIn, zoomOut
	
	if usePyObjC:
		
		arrow = NSCursor.arrowCursor()
		closedHand = NSCursor.closedHandCursor()
		cross = NSCursor.crosshairCursor()
		openHand = NSCursor.openHandCursor()
		
	else:
		
		arrow = wx.StockCursor(wx.CURSOR_ARROW)
		closedHand = getCursorFromFile('ClosedHandCursor.png', (8, 6))
		cross = wx.StockCursor(wx.CURSOR_CROSS)
		openHand = getCursorFromFile('OpenHandCursor.png', (8, 6))
	
	bucket = getCursorFromFile('BucketCursor.png', (13, 15))
	zoomIn = getCursorFromFile('ZoomInCursor.png', (5, 6))
	zoomOut = getCursorFromFile('ZoomOutCursor.png', (5, 6))
