# ForgeryRegularPolygonTool.py
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
	'ForgeryRegularPolygonTool',
)

import ForgeryCursor, ForgeryElements, ForgeryTool

from OpenGL.GL import *

import math

class ForgeryRegularPolygonTool(ForgeryTool.ForgeryTool):
	iconFileName = 'Polygon.png'
	cursor = ForgeryCursor.cross
	toolID = ID.REGULAR_POLYGON_TOOL
	position = (1, 0)

ForgeryTool.tools[ForgeryRegularPolygonTool.toolID] = ForgeryRegularPolygonTool
