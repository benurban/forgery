# ForgeryCommon.py
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

__all__ = (
	'usePyObjC',
	'resourcesDir',
	'WU',
	'sqrt2',
	'errorWrap',
	'trueFunc',
	'falseFunc',
	'roundUp',
	'roundDown',
	'roundToNearest',
	'angleBetween',
	'capitalize',
	'ID',
	'ForgeryError',
	'ForgeryBadDataError',
	'ForgeryFillError',
	'ForgerySpaceOccupiedError',
	'ForgeryNoPolygonFoundError',
	'ForgeryDeadEndError',
	'ForgeryOpenPolygonError',
	'ForgeryInvalidLineError',
	'ForgeryZeroLengthLineError',
	'ForgerySideConflictError',
	'ForgeryPointOutsidePolygonError',
)

try:
	import objc
except ImportError:
	hasPyObjC = False
else:
	hasPyObjC = True

try:
	import wx
except ImportError:
	hasWX = False
else:
	hasWX = True

if hasPyObjC:
	if hasWX:
		if preferWX:
			usePyObjC = False
		else:
			usePyObjC = True
	else:
		usePyObjC = True
else:
	if hasWX:
		usePyObjC = False
	else:
		raise ImportError, u"Forgery requires wxPython or PyObjC, or both"

import math, os, sys, traceback

if sys.platform == 'darwin' and '.app' in __file__:
	# __file__ is probably something like
	# '.../Forgery.app/Contents/Resources/ForgeryCommon.py'
	resourcesDir = os.path.dirname(__file__)
else:
	resourcesDir = os.path.dirname(__file__)

WU = 1024

sqrt2 = math.sqrt(2.0)

def errorWrap(func):
	def wrap(*posArgs, **kwdargs):
		try:
			return func(*posArgs, **kwdargs)
		except:
			traceback.print_exc(file = sys.stdout)
			raise
	
	wrap.__doc__ = func.__doc__
	wrap.__module__ = func.__module__
	wrap.__name__ = func.__name__
	return wrap

trueFunc = lambda *posArgs, **kwdArgs: True
falseFunc = lambda *posArgs, **kwdArgs: False

def roundUp(x, y):
	return math.ceil(float(x) / float(y)) * y

def roundDown(x, y):
	return math.floor(float(x) / float(y)) * y

def roundToNearest(x, y):
	return math.floor(float(x) / float(y) + 0.5) * y

if True: # Both algorithms work;  I don't know which is faster.
	def angleBetween((x0, y0), (x1, y1)):
		"""Returns the directed angle between two vectors, in radians.
The result is between -pi and pi."""
		alpha = math.atan2(y0, x0)
		beta = math.atan2(y1, x1)
		if beta - alpha > math.pi:
			alpha += 2 * math.pi
		elif alpha - beta >= math.pi:
			beta += 2 * math.pi
		return beta - alpha
else:
	def angleBetween((x0, y0), (x1, y1)):
		"""Returns the directed angle between two vectors, in radians.
The result is between -pi and pi."""
		theta = math.acos((x0 * x1 + y0 * y1) / math.sqrt((x0 * x0 + y0 * y0) * (x1 * x1 + y1 * y1)))
		if x1 * y0 > y1 * x0:
			return -theta
		else:
			return theta

def capitalize(s):
	return s[0].upper() + s[1:]

if not usePyObjC:
	__all__ += (
		'addStaticSpacer',
		'addStretchSpacer',
		'buildNonuniformGrid',
		'buildSizers',
	)
	
	def addStaticSpacer(sizer, size):
		try:
			return sizer.AddSpacer(size)
		except TypeError: # wx 2.6 does this
			return sizer.AddItem(wx.SizerItemSpacer(size, size, 0, 0, 0))
	
	def addStretchSpacer(sizer):
		try:
			return sizer.AddStretchSpacer()
		except TypeError: # wx 2.6 does this
			return sizer.AddItem(wx.SizerItemSpacer(0, 0, 1, 0, 0))
	
	def buildNonuniformGrid(columns, *items):
		# 0 * 1 * 2
		# * * * * *
		# 3 * 4 * 5
		# * * * * *
		# 6 * 7 * 8
		# The numbers represent the items; the *s represent 8x8 spacers
		#realColumns = 2 * columns - 1
		#result = wx.FlexGridSizer(cols = realColumns)
		#for index, item in enumerate(items[:-1]):
		#	if isinstance(item, (int, long)):
		#		addStaticSpacer(result, item)
		#	elif isinstance(item, wx.Object):
		#		result.Add(item)
		#	else:
		#		addStretchSpacer(result)
		#	if (index + 1) % columns:
		#		addStaticSpacer(result, 8)
		#	else:
		#		for i in xrange(realColumns):
		#			addStaticSpacer(result, 8)
		#if isinstance(items[-1], (int, long)):
		#	addStaticSpacer(result, items[-1])
		#elif isinstance(items[-1], wx.Object):
		#	result.Add(items[-1])
		#else:
		#	addStretchSpacer(result)
		result = wx.FlexGridSizer(
			cols = columns,
			hgap = 8, vgap = 8,
		)
		for item in items:
			if isinstance(item, (int, long)):
				addStaticSpacer(result, item)
			elif isinstance(item, wx.Object):
				result.Add(item)
			else:
				addStretchSpacer(result)
		return result
	
	def buildSizers(direction, *items):
		result = wx.BoxSizer(direction)
		for item in items:
			if item is None:
				addStretchSpacer(result)
			elif isinstance(item, (int, long)):
				addStaticSpacer(result, item)
			elif isinstance(item, wx.Object):
				result.Add(item)
			elif direction == wx.HORIZONTAL:
				result.Add(buildSizers(wx.VERTICAL, *item))
			else:
				result.Add(buildSizers(wx.HORIZONTAL, *item))
		return result

class ID(object):
	
	if usePyObjC:
		
		# File menu
		NEW                    = 5002
		OPEN                   = 5000
		CLOSE                  = 5001
		SAVE                   = 5003
		SAVEAS                 = 5004
		REVERT                 = 5005
		IMPORT_SHAPES          = 5999 + 0x0101
		EXIT                   = 5006
		# Edit menu
		UNDO                   = 5007
		REDO                   = 5008
		CUT                    = 5031
		COPY                   = 5032
		PASTE                  = 5033
		DELETE                 = 5038
		DUPLICATE              = 5036
		SELECTALL              = 5037
		SELECTNONE             = 5999 + 0x0201
		PREFERENCES            = 5022
		# View menu
		TOGGLE_PALETTE         = 5999 + 0x0301
		TOGGLE_INSPECTOR       = 5999 + 0x0302
		TOGGLE_GRID            = 5999 + 0x0303
		MODES_START            = 5999 + 0x0381
		DRAW_MODE              = 5999 + 0x0381
		VISUAL_MODE            = 5999 + 0x0382
		FLOOR_ELEVATION_MODE   = 5999 + 0x0383
		CEILING_ELEVATION_MODE = 5999 + 0x0384
		FLOOR_TEXTURES_MODE    = 5999 + 0x0385
		CEILING_TEXTURES_MODE  = 5999 + 0x0386
		POLYGON_TYPE_MODE      = 5999 + 0x0387
		FLOOR_LIGHTS_MODE      = 5999 + 0x0388
		CEILING_LIGHTS_MODE    = 5999 + 0x0389
		MEDIA_LIGHTS_MODE      = 5999 + 0x038A
		LIQUIDS_MODE           = 5999 + 0x038B
		AMBIENT_SOUNDS_MODE    = 5999 + 0x038C
		RANDOM_SOUNDS_MODE     = 5999 + 0x038D
		MODES_END              = 5999 + 0x038D
		# Tools menu
		TOOLS_START            = 5999 + 0x0401
		SELECT_TOOL            = 5999 + 0x0401
		LINE_TOOL              = 5999 + 0x0402
		REGULAR_POLYGON_TOOL   = 5999 + 0x0403
		FILL_TOOL              = 5999 + 0x0404
		PAN_TOOL               = 5999 + 0x0405
		ZOOM_TOOL              = 5999 + 0x0406
		TEXT_TOOL              = 5999 + 0x0407
		OBJECT_TOOL            = 5999 + 0x0408
		TOOLS_END              = 5999 + 0x0408
		# Dialog buttons
		APPLY                  = 5102
		CANCEL                 = 5101
		DONTSAVE               = 5104
		NO                     = 5104
		OK                     = 5100
		#SAVE                  = 5003
		YES                    = 5103
		# Inspector tabs
		NO_SELECTION           = 5999 + 0x0601
		MULTIPLE_SELECTION     = 5999 + 0x0602
		VERTEX                 = 5999 + 0x0603
		LINE                   = 5999 + 0x0604
		POLYGON                = 5999 + 0x0605
		OBJECT                 = 5999 + 0x0606
		SOUND                  = 5999 + 0x0607
		# Surface actions
		EFFECT_NORMAL          = 5999 + 0x0701
		EFFECT_PULSATE         = 5999 + 0x0702
		EFFECT_WOBBLE          = 5999 + 0x0703
		EFFECT_SLIDE           = 5999 + 0x0704
		EFFECT_WANDER          = 5999 + 0x0705
		ACTION_SWITCH          = 5999 + 0x0781
		ACTION_PATTERN_BUFFER  = 5999 + 0x0782
		ACTION_TERMINAL        = 5999 + 0x0783
		ACTION_RECHARGER       = 5999 + 0x0784
		
	else:
		
		# File menu
		NEW                    = wx.ID_NEW
		OPEN                   = wx.ID_OPEN
		CLOSE                  = wx.ID_CLOSE
		SAVE                   = wx.ID_SAVE
		SAVEAS                 = wx.ID_SAVEAS
		REVERT                 = wx.ID_REVERT
		IMPORT_SHAPES          = wx.ID_HIGHEST + 0x0101
		EXIT                   = wx.ID_EXIT
		# Edit menu
		UNDO                   = wx.ID_UNDO
		REDO                   = wx.ID_REDO
		CUT                    = wx.ID_CUT
		COPY                   = wx.ID_COPY
		PASTE                  = wx.ID_PASTE
		DELETE                 = wx.ID_DELETE
		DUPLICATE              = wx.ID_DUPLICATE
		SELECTALL              = wx.ID_SELECTALL
		SELECTNONE             = wx.ID_HIGHEST + 0x0201
		PREFERENCES            = wx.ID_PREFERENCES
		# View menu
		TOGGLE_PALETTE         = wx.ID_HIGHEST + 0x0301
		TOGGLE_INSPECTOR       = wx.ID_HIGHEST + 0x0302
		TOGGLE_GRID            = wx.ID_HIGHEST + 0x0303
		MODES_START            = wx.ID_HIGHEST + 0x0381
		DRAW_MODE              = wx.ID_HIGHEST + 0x0381
		VISUAL_MODE            = wx.ID_HIGHEST + 0x0382
		FLOOR_ELEVATION_MODE   = wx.ID_HIGHEST + 0x0383
		CEILING_ELEVATION_MODE = wx.ID_HIGHEST + 0x0384
		FLOOR_TEXTURES_MODE    = wx.ID_HIGHEST + 0x0385
		CEILING_TEXTURES_MODE  = wx.ID_HIGHEST + 0x0386
		POLYGON_TYPE_MODE      = wx.ID_HIGHEST + 0x0387
		FLOOR_LIGHTS_MODE      = wx.ID_HIGHEST + 0x0388
		CEILING_LIGHTS_MODE    = wx.ID_HIGHEST + 0x0389
		MEDIA_LIGHTS_MODE      = wx.ID_HIGHEST + 0x038A
		LIQUIDS_MODE           = wx.ID_HIGHEST + 0x038B
		AMBIENT_SOUNDS_MODE    = wx.ID_HIGHEST + 0x038C
		RANDOM_SOUNDS_MODE     = wx.ID_HIGHEST + 0x038D
		MODES_END              = wx.ID_HIGHEST + 0x038D
		# Tools menu
		TOOLS_START            = wx.ID_HIGHEST + 0x0401
		SELECT_TOOL            = wx.ID_HIGHEST + 0x0401
		LINE_TOOL              = wx.ID_HIGHEST + 0x0402
		REGULAR_POLYGON_TOOL   = wx.ID_HIGHEST + 0x0403
		FILL_TOOL              = wx.ID_HIGHEST + 0x0404
		PAN_TOOL               = wx.ID_HIGHEST + 0x0405
		ZOOM_TOOL              = wx.ID_HIGHEST + 0x0406
		TEXT_TOOL              = wx.ID_HIGHEST + 0x0407
		OBJECT_TOOL            = wx.ID_HIGHEST + 0x0408
		TOOLS_END              = wx.ID_HIGHEST + 0x0408
		# Dialog buttons
		APPLY                  = wx.ID_APPLY
		CANCEL                 = wx.ID_CANCEL
		DONTSAVE               = wx.ID_NO
		NO                     = wx.ID_NO
		OK                     = wx.ID_OK
		#SAVE                  = wx.ID_SAVE
		YES                    = wx.ID_YES
		# UI elements
		STATUS_BAR             = wx.ID_HIGHEST + 0x0501
		# Inspector tabs
		NO_SELECTION           = wx.ID_HIGHEST + 0x0601
		MULTIPLE_SELECTION     = wx.ID_HIGHEST + 0x0602
		VERTEX                 = wx.ID_HIGHEST + 0x0603
		LINE                   = wx.ID_HIGHEST + 0x0604
		POLYGON                = wx.ID_HIGHEST + 0x0605
		OBJECT                 = wx.ID_HIGHEST + 0x0606
		SOUND                  = wx.ID_HIGHEST + 0x0607
		# Surface actions
		EFFECT_NORMAL          = wx.ID_HIGHEST + 0x0701
		EFFECT_PULSATE         = wx.ID_HIGHEST + 0x0702
		EFFECT_WOBBLE          = wx.ID_HIGHEST + 0x0703
		EFFECT_SLIDE           = wx.ID_HIGHEST + 0x0704
		EFFECT_WANDER          = wx.ID_HIGHEST + 0x0705
		ACTION_SWITCH          = wx.ID_HIGHEST + 0x0781
		ACTION_PATTERN_BUFFER  = wx.ID_HIGHEST + 0x0782
		ACTION_TERMINAL        = wx.ID_HIGHEST + 0x0783
		ACTION_RECHARGER       = wx.ID_HIGHEST + 0x0784

class ForgeryError(Exception):
	pass

class ForgeryBadDataError(ForgeryError):
	pass

class ForgeryFillError(ForgeryError):
	pass

class ForgerySpaceOccupiedError(ForgeryFillError):
	def __init__(self, polygon):
		super(ForgerySpaceOccupiedError, self).__init__(u"Polygon '%s' is already there" % (polygon.elementID, ))

class ForgeryNoPolygonFoundError(ForgeryFillError):
	def __init__(self):
		super(ForgeryNoPolygonFoundError, self).__init__(u"Could not find any lines that intersect the projection")

class ForgeryDeadEndError(ForgeryFillError):
	def __init__(self, line, vertex):
		super(ForgeryDeadEndError, self).__init__(u"Encountered a dead end\nfollowing line '%s' to vertex '%s'" % (line.elementID, vertex.elementID))

class ForgeryOpenPolygonError(ForgeryFillError):
	def __init__(self, line):
		super(ForgeryOpenPolygonError, self).__init__(u"The polygon did not close, or two lines share the same vertices\nline '%s' appears to be the cause" % (line0.elementID, ))

class ForgeryInvalidLineError(ForgeryBadDataError, ForgeryFillError):
	def __init__(self, line):
		super(ForgeryInvalidLineError, self).__init__(u"Line '%s' is invalid" % (line.elementID, ))

class ForgeryZeroLengthLineError(ForgeryInvalidLineError):
	def __init__(self, line):
		super(ForgeryInvalidLineError, self).__init__(u"Line '%s' has zero length" % (line.elementID, ))

class ForgerySideConflictError(ForgeryInvalidLineError):
	def __init__(self, line):
		super(ForgeryInvalidLineError, self).__init__(u"Line '%s' already has two sides" % (line.elementID, ))

class ForgeryPointOutsidePolygonError(ForgeryFillError):
	def __init__(self):
		super(ForgeryPointOutsidePolygonError, self).__init__(u"The fill point is not inside the new polygon")
