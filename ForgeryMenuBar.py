# ForgeryMenuBar.py
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

if not usePyObjC:
	
	__all__ = (
		'menus',
		'CreateMenu',
	)
	
	import ForgeryApplication
	
	import wx
	
	menus = [
		(
			'menu',
			"&File",
			[
				(
					'item',
					ID.NEW,
					"&New",
					'CTRL-N',
					None,
					lambda document: ForgeryApplication.sharedApplication().OnNewDocument,
				),
				(
					'item',
					ID.OPEN,
					"&Open...",
					'CTRL-O',
					None,
					lambda document: ForgeryApplication.sharedApplication().OnOpenDocument,
				),
				(
					'submenu',
					None,
					"Open Recent",
					None,
					[],
				),
				(
					'separator',
				),
				(
					'item',
					ID.CLOSE,
					"&Close",
					'CTRL-W',
					None,
					lambda document: ForgeryApplication.sharedApplication().OnCloseDocument,
				),
				(
					'item',
					ID.SAVE,
					"&Save",
					'CTRL-S',
					None,
					lambda document: document.OnSaveDocument,
				),
				(
					'item',
					ID.SAVEAS,
					"Save &As...",
					'CTRL-SHIFT-S',
					None,
					lambda document: document.OnSaveDocumentAs,
				),
				(
					'item',
					ID.REVERT,
					"&Revert to Saved",
					None,
					None,
					lambda document: document.OnRevertDocument,
				),
				(
					'separator',
				),
				(
					'item',
					ID.IMPORT_SHAPES,
					"&Import Shapes...",
					None,
					None,
					lambda document: document.OnImportShapes,
				),
				(
					'separator',
				),
				(
					'item',
					ID.EXIT,
					"&Quit",
					'CTRL-Q',
					None,
					lambda document: ForgeryApplication.sharedApplication().OnQuit,
				),
			],
		),
		(
			'menu',
			"&Edit",
			[
				(
					'item',
					ID.UNDO,
					"&Undo",
					'CTRL-Z',
					None,
					lambda document: document.OnUndo,
				),
				(
					'item',
					ID.REDO,
					"&Redo",
					'CTRL-SHIFT-Z',
					None,
					lambda document: document.OnRedo,
				),
				(
					'separator',
				),
				(
					'item',
					ID.CUT,
					"Cu&t",
					'CTRL-X',
					None,
					lambda document: document.OnCut,
				),
				(
					'item',
					ID.COPY,
					"&Copy",
					'CTRL-C',
					None,
					lambda document: document.OnCopy,
				),
				(
					'item',
					ID.PASTE,
					"&Paste",
					'CTRL-V',
					None,
					lambda document: document.OnPaste,
				),
				(
					'item',
					ID.DELETE,
					"&Delete",
					'DELETE',
					None,
					lambda document: document.OnDelete,
				),
				(
					'separator',
				),
				(
					'item',
					ID.DUPLICATE,
					"Du&plicate",
					'CTRL-D',
					None,
					lambda document: document.OnDuplicate,
				),
				(
					'separator',
				),
				(
					'item',
					ID.SELECTALL,
					"Select &All",
					'CTRL-A',
					None,
					lambda document: document.OnSelectAll,
				),
				(
					'item',
					ID.SELECTNONE,
					"Select &None",
					'CTRL-SHIFT-A',
					None,
					lambda document: document.OnSelectNone,
				),
				(
					'separator',
				),
				(
					'item',
					ID.PREFERENCES,
					"Pr&eferences...",
					'CTRL-,',
					None,
					None, # lambda document: document.OnPreferences,
				),
			],
		),
		(
			'menu',
			"&View",
			[
				(
					'submenu',
					None,
					"&Map",
					None,
					[],
				),
				(
					'separator',
				),
				(
					'checked item',
					ID.DRAW_MODE,
					"&Draw",
					'CTRL-0',
					None,
					lambda document: document.OnChangeMode,
				),
				(
					'checked item',
					ID.VISUAL_MODE,
					"&Visual",
					'CTRL-1',
					None,
					lambda document: document.OnChangeMode,
				),
				(
					'separator',
				),
				(
					'submenu',
					None,
					"&Elevation",
					None,
					[
						(
							'checked item',
							ID.FLOOR_ELEVATION_MODE,
							"&Floor",
							None,
							None,
							lambda document: document.OnChangeMode,
						),
						(
							'checked item',
							ID.CEILING_ELEVATION_MODE,
							"&Ceiling",
							None,
							None,
							lambda document: document.OnChangeMode,
						),
					],
				),
				(
					'submenu',
					None,
					"&Textures",
					None,
					[
						(
							'checked item',
							ID.FLOOR_TEXTURES_MODE,
							"&Floor",
							None,
							None,
							lambda document: document.OnChangeMode,
						),
						(
							'checked item',
							ID.CEILING_TEXTURES_MODE,
							"&Ceiling",
							None,
							None,
							lambda document: document.OnChangeMode,
						),
					],
				),
				(
					'checked item',
					ID.POLYGON_TYPE_MODE,
					"&Polygon Type",
					None,
					None,
					lambda document: document.OnChangeMode,
				),
				(
					'separator',
				),
				(
					'submenu',
					None,
					"&Lights",
					None,
					[
						(
							'checked item',
							ID.FLOOR_LIGHTS_MODE,
							"&Floor Lights",
							None,
							None,
							lambda document: document.OnChangeMode,
						),
						(
							'checked item',
							ID.CEILING_LIGHTS_MODE,
							"&Ceiling Lights",
							None,
							None,
							lambda document: document.OnChangeMode,
						),
						(
							'checked item',
							ID.MEDIA_LIGHTS_MODE,
							"&Media",
							None,
							None,
							lambda document: document.OnChangeMode,
						),
					],
				),
				(
					'checked item',
					ID.LIQUIDS_MODE,
					"&Liquids",
					None,
					None,
					lambda document: document.OnChangeMode,
				),
				(
					'submenu',
					None,
					"&Sounds",
					None,
					[
						(
							'checked item',
							ID.AMBIENT_SOUNDS_MODE,
							"&Ambient Sounds",
							None,
							None,
							lambda document: document.OnChangeMode,
						),
						(
							'checked item',
							ID.RANDOM_SOUNDS_MODE,
							"&Random Sounds",
							None,
							None,
							lambda document: document.OnChangeMode,
						),
					],
				),
				(
					'separator',
				),
				(
					'item',
					ID.TOGGLE_PALETTE,
					"Toggle &Palette",
					None,
					None,
					lambda document: ForgeryApplication.sharedApplication().OnTogglePalette,
				),
				(
					'item',
					ID.TOGGLE_INSPECTOR,
					"Toggle &Inspector",
					'CTRL-ALT-I',
					None,
					lambda document: ForgeryApplication.sharedApplication().OnToggleInspector,
				),
				(
					'separator',
				),
				(
					'item',
					ID.TOGGLE_GRID,
					"Toggle &Grid",
					None,
					None,
					lambda document: document.OnToggleGrid,
				),
			],
		),
	]
	
	def CreateMenu(document, items, result = None):
		if not result:
			result = wx.Menu()
		for item in items:
			kind, item = item[0], item[1:]
			if kind == 'separator':
				result.AppendSeparator()
			elif kind == 'item':
				itemID, name, shortcut, helpText, func = item
				if not itemID:
					itemID = wx.NewId()
				if shortcut:
					name = name + '\t' + shortcut
				if not helpText:
					helpText = ""
				result.Append(itemID, name, helpText, wx.ITEM_NORMAL)
				if func:
					document.Bind(wx.EVT_MENU, errorWrap(func(document)), id = itemID)
			elif kind == 'checked item':
				itemID, name, shortcut, helpText, func = item
				if not itemID:
					itemID = wx.NewId()
				if shortcut:
					name = name + '\t' + shortcut
				if not helpText:
					helpText = ""
				result.Append(itemID, name, helpText, wx.ITEM_CHECK)
				if func:
					document.Bind(wx.EVT_MENU, errorWrap(func(document)), id = itemID)
			elif kind == 'radio item':
				itemID, name, shortcut, helpText, func = item
				if not itemID:
					itemID = wx.NewId()
				if shortcut:
					name = name + '\t' + shortcut
				if not helpText:
					helpText = ""
				result.Append(itemID, name, helpText, wx.ITEM_RADIO)
				if func:
					document.Bind(wx.EVT_MENU, errorWrap(func(document)), id = itemID)
			elif kind == 'submenu':
				itemID, name, helpText, menu = item
				if not itemID:
					itemID = wx.NewId()
				if not helpText:
					helpText = ""
				result.AppendMenu(itemID, name, CreateMenu(document, menu), helpText)
			elif kind == 'menu':
				name, menu = item
				result.Append(CreateMenu(document, menu), name)
			else:
				raise KeyError, kind
		return result
