# ForgerysceAExporter.py
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
	'ForgerysceAExporter',
)

def _indexer(code):
	def indexer(self, elements):
		elements = elements.items()
		elements.sort()
		self.[code] = [element for elementID, element in elements]
	return indexer

class ForgerysceAExporter(object):
	data = None
	indexedData = None
	
	annotations = NOTE = property(
		fget = lambda self, self.indexedData.__getitem__('NOTE'),
		fset = lambda self, value: self.indexedData.__setitem__('NOTE', value),
		fdel = lambda self: self.indexedData.__delitem__('NOTE'),
	)
	lights      = LITE = property(
		fget = lambda self, self.indexedData.__getitem__('LITE'),
		fset = lambda self, value: self.indexedData.__setitem__('LITE', value),
		fdel = lambda self: self.indexedData.__delitem__('LITE'),
	)
	lines       = LINS = property(
		fget = lambda self, self.indexedData.__getitem__('LINS'),
		fset = lambda self, value: self.indexedData.__setitem__('LINS', value),
		fdel = lambda self: self.indexedData.__delitem__('LINS'),
	)
	objects     = OBJS = property(
		fget = lambda self, self.indexedData.__getitem__('OBJS'),
		fset = lambda self, value: self.indexedData.__setitem__('OBJS', value),
		fdel = lambda self: self.indexedData.__delitem__('OBJS'),
	)
	polygons    = POLY = property(
		fget = lambda self, self.indexedData.__getitem__('POLY'),
		fset = lambda self, value: self.indexedData.__setitem__('POLY', value),
		fdel = lambda self: self.indexedData.__delitem__('POLY'),
	)
	sides       = SIDS = property(
		fget = lambda self, self.indexedData.__getitem__('SIDS'),
		fset = lambda self, value: self.indexedData.__setitem__('SIDS', value),
		fdel = lambda self: self.indexedData.__delitem__('SIDS'),
	)
	vertices    = PNTS = property(
		fget = lambda self, self.indexedData.__getitem__('PNTS'),
		fset = lambda self, value: self.indexedData.__setitem__('PNTS', value),
		fdel = lambda self: self.indexedData.__delitem__('PNTS'),
	)
	
	def __init__(self, data):
		self.data = data
		self.indexData()
	
	def __getitem__(self, key):
		return self.__getattr__(key)
	
	def __setitem__(self, key, value):
		return self.__setattr__(key, value)
	
	def __delitem__(self, key):
		return self.__delattr__(key)
	
	def indexData(self, data):
		for polygon in data.polygons.itervalues():
			polygon.findSides()
		
		self.indexedData = {}
		for category, elements in data.iteritems():
			indexer = getattr(self, 'index' + capitalize(category))
			if callable(indexer):
				indexer(elements)
			else:
				print "No indexer for %s" % (category, )
		
		self.indexSides(self.LINS)
	
	indexAnnotations = _indexer('NOTE')
	indexLights      = _indexer('LITE')
	indexLines       = _indexer('LINS')
	indexObjects     = _indexer('OBJS')
	indexPolygons    = _indexer('POLY')
	indexVertices    = _indexer('PNTS')
	
	def indexSides(self, lines):
		result = []
		for line in lines:
			if line.side0:
				result.append(line.side0)
			if line.side1:
				result.append(line.side1)
		self.SIDS = result
	
	def indexOfElement(self, element, code):
		for result, e in enumerate(self[code]):
			if e is element:
				return result
		else:
			raise ValueError, element
	
	indexOfAnnotation = indexOfNOTE = (lambda self, element: indexOfElement(element, 'NOTE'))
	indexOfLight      = indexOfLITE = (lambda self, element: indexOfElement(element, 'LITE'))
	indexOfLine       = indexOfLINS = (lambda self, element: indexOfElement(element, 'LINS'))
	indexOfObject     = indexOfOBJS = (lambda self, element: indexOfElement(element, 'OBJS'))
	indexOfPolygon    = indexOfPOLY = (lambda self, element: indexOfElement(element, 'POLY'))
	indexOfSide       = indexOfSIDS = (lambda self, element: indexOfElement(element, 'SIDS'))
	indexOfVertex     = indexOfPNTS = (lambda self, element: indexOfElement(element, 'PNTS'))
	
	def writeNulls(self, length):
		self.seek(length, 1)
	
	def writeBytes(self, data):
		self.write(data)
	
	def writeChar(self, data):
		self.writeBytes(data)
	
	def writeFourCharCode(self, data):
		self.writeBytes(data[:4])
	
	def writeInt8(self, data):
		self.writeChar(chr(data))
	
	def writeInt16(self, data):
		self.writeInt8((data >> 8) & 0xFF)
		self.writeInt8((data >> 0) & 0xFF)
	
	def writeInt32(self, data):
		self.writeInt16((data >> 16) & 0xFFFF)
		self.writeInt16((data >>  0) & 0xFFFF)
	
	def writePString(self, data, length = None):
		if length is None:
			length = min(len(data) + 1, 256)
		data = data[:length - 1]
		self.writeInt8(len(data))
		self.writeBytes(data)
		self.writeNulls(length - len(data) - 1)
	
	def writeCString(self, data, length = None):
		if length is None:
			length = len(data) + 1
		data = data[:length - 1]
		self.writeBytes(data)
		self.writeNulls(length - len(data))
	
	def writeEntryHeader(self, tag, nextOffset, length, offset):
		self.writeFourCharCode(tag)
		self.writeInt32(nextOffset + length + 16)
		self.writeInt32(length)
		self.writeInt32(offset)
	
	def writePNTSEntry(self, data):
		if self.vertices:
#			self.writeEntryHeader('PNTS', [mapDataToSave length], len(self.vertices) * 4, 0)
			for vertex in self.vertices:
				self.writeInt16(int(vertex.x))
				self.writeInt16(int(vertex.y))
	
	def writeLINSEntry(self, data):
		if self.lines:
#			self.writeEntryHeader('LINS', [mapDataToSave length], len(self.lines) * 32, 0)
			for line in self.lines:
				self.writeInt16(self.indexOfVertex(line.vertex0))
				self.writeInt16(self.indexOfVertex(line.vertex1.index))
				self.writeInt16(line.flags)
				self.writeInt16(line.length)
				self.writeInt16(line.getHighestAdjacentFloor(data))
				self.writeInt16(line.getLowestAdjacentCeiling(data))
				self.writeInt16(self.indexOfSide(line.getClockwisePolygonSide(data)))
				self.writeInt16(self.indexOfSide(line.getCounterclockwisePolygonSide(data)))
				self.writeInt16(self.indexOfPolygon(line.getClockwisePolygonOwner(data)))
				self.writeInt16(self.indexOfPolygon(line.getCounterclockwisePolygonOwner(data)))
				self.writeNulls(12)
	
	def writePOLYEntry(self, data):
		if self.polygons:
#			self.writeEntryHeader('POLY', [mapDataToSave length], len(self.polygons) * 128, 0)
			for polygon in self.polygons:
				if len(polygon) > 8:
					raise ForgeryExportError(self, polygon, "may not have more than 8 sides")
				self.writeInt16(polygon.polygonType)
				self.writeInt16(polygon.flags)
				self.writeInt16(polygon.getPermutation())
				
				self.writeInt16(len(polygon))
				
				for line, side in zip(polygon, polygon.sides):
					self.writeInt16(self.indexOfVertex(getattr(line, 'vertex' + str(side))))
				self.writeBytes('\xFF\xFF' * (8 - len(polygon)))
				
				for line in polygon:
					self.writeInt16(self.indexOfLine(line))
				self.writeBytes('\xFF\xFF' * (8 - len(polygon)))
				
				self.writeInt16(polygon.floor.texture.index)
				self.writeInt16(polygon.ceiling.texture.index)
				self.checkInt16(int(polygon.floorHeight), polygon, "%%s's floor height %s")
				self.writeInt16(int(polygon.floorHeight))
				self.checkInt16(int(polygon.ceilingHeight), polygon, "%%s's ceiling height %s")
				self.writeInt16(int(polygon.ceilingHeight))
				self.writeInt16(self.indexOfLight(polygon.floor.light))
				self.writeInt16(self.indexOfLight(polygon.ceiling.light))
				
				#self.writeInt32(int(polygon.area))
				self.writeNulls(4)
				
				#self.writeInt16([polygon getFirst_object_index])
				self.writeInt16(-1)
				#self.writeInt16([polygon getFirst_exclusion_zone_index])
				#self.writeInt16([polygon getLine_exclusion_zone_count])
				#self.writeInt16([polygon getPoint_exclusion_zone_count])
				self.writeNulls(6)
				
				self.writeInt16(polygon.floor.transferMode) # effect
				self.writeInt16(polygon.ceiling.transferMode)
				
				#for line, side in zip(polygon, polygon.sides):
				#	self.indexOfPolygon(self.data.polygonForSide(line, 1 - side))
				#self.writeBytes('\xFF\xFF' * (8 - len(polygon)))
				self.writeNulls(32)
				
				#self.writeInt16([polygon getFirst_neighbor_index])
				#self.writeInt16([polygon getNeighbor_count])
				self.writeNulls(4)
				
				#self.writeInt16(polygon.center[0])
				#self.writeInt16(polygon.center[1])
				self.writeNulls(4)
				
				for line in polygon:
					self.writeInt16(self.indexOfLine(line))
				self.writeBytes('\xFF\xFF' * (8 - len(polygon)))
				
				self.writeInt16(int(polygon.floor.dx))
				self.writeInt16(int(polygon.floor.dy))
				
				self.writeInt16(int(polygon.ceiling.dx))
				self.writeInt16(int(polygon.ceiling.dy))
				
				#self.writeInt16(polygon.media.index)
				#self.writeInt16(polygon.media.light.index)
				self.writeNulls(4)
				
				#self.writeInt16([polygon getSound_source_indices])
				self.writeNulls(2)
				
#				self.writeInt16([polygon getAmbient_sound_image_index])
#				self.writeInt16([polygon getRandom_sound_image_index])
				
				self.writeNulls(2)

"""
- (NSMutableData *)saveLevelAndGetMapNSData:(LELevelData *)level levelToSaveIn:(short)levelToSaveIn
{
	long projectedLevelByteCount = [self getByteCountForLevel:level];
	long levelLength;
	NSMutableData *levelData;
	NSMutableData *levelHeaderData;
	NSMutableData *mapHeaderData;
	NSMutableData *entireMapData;
	
	#ifdef useDebuggingLogs
		NSLog(@"save projectedLevelByteCount: %d", projectedLevelByteCount);
	#endif
	mapDataToSave = [[NSMutableData alloc] initWithCapacity:500 * 1000];
	
	//   -(void)saveTag:(long)theTag theLevelNumber:(short)levelNumber theLevelData:(LELevelData *)level
	
	#ifdef useDebuggingLogs
		NSLog(@"*Begining Phase 1 loading process into level %d from file...*", levelToSaveIn);
	#endif
	
	//   Get the points into this level... ('PNTS')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving points from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'PNTS' theLevelNumber:levelToSaveIn theLevelData:level];
	[self savePointsForLevel:level];
	
	//   Get the lines into this level... ('LINS')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving lines from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'LINS' theLevelNumber:levelToSaveIn theLevelData:level];
	[self saveLinesForLevel:level];
	
	//   Get the polys into this level... ('POLY')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving poly's from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'POLY' theLevelNumber:levelToSaveIn theLevelData:level];
	[self savePolygonsForLevel:level];
	
	//   Get the objects into this level... ('OBJS')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving objects from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'OBJS' theLevelNumber:levelToSaveIn theLevelData:level];
	[self saveObjectsForLevel:level];
	
	//   Get the sides into this level... ('SIDS')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving sides from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'SIDS' theLevelNumber:levelToSaveIn theLevelData:level];
	[self saveSidesForLevel:level];
	
	//   Get the lights into this level... ('LITE')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving lights from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'LITE' theLevelNumber:levelToSaveIn theLevelData:level];
	[self saveLightsForLevel:level];
	
	//   Get the annotations (notes) into this level... ('NOTE')
	//NSLog(@"*Saving annotations from file into level %d*", levelToSaveIn);
	//[self saveTag:'NOTE' theLevelNumber:levelToSaveIn theLevelData:level];
	[self saveNotesForLevel:level];
	
	//   Get the liquids (media) into this level... ('medi')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving liquids from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'medi' theLevelNumber:levelToSaveIn theLevelData:level];
	[self saveMediasForLevel:level];
	
	//   Get the ambient sounds (like the wind) into this level... ('ambi')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving ambient sounds from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'ambi' theLevelNumber:levelToSaveIn theLevelData:level];
	[self saveAmbientSoundsForLevel:level];
	
	// *** New ***
	
	 //   Get the platforms (like the wind) into this level... ('plat')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving platforms from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'plat' theLevelNumber:levelToSaveIn theLevelData:level];
	[self savePlatformsForLevel:level];
	
	//   Get the item placment entrys (like the wind) into this level... ('plac')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving item placment data from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'plac' theLevelNumber:levelToSaveIn theLevelData:level];
	[self saveItemPlacementForLevel:level];
	
	//   Get the random sounds (like dripping sounds) into this level... ('bonk')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving random sounds from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'bonk' theLevelNumber:levelToSaveIn theLevelData:level];
	[self saveRandomSoundsForLevel:level];
	
	//   Get the terminals into this level... ('bonk')
	#ifdef useDebuggingLogs
		NSLog(@"*Saving terminals from file into level %d*", levelToSaveIn);
	#endif
	//[self saveTag:'term' theLevelNumber:levelToSaveIn theLevelData:level];
	[self saveTerminalDataForLevel:level];
	
	// *** End New ***
	
	[self saveBasicLevelInfo:level];
	
	levelLength = [mapDataToSave length];
	
	levelData = mapDataToSave;
	mapDataToSave = [[NSMutableData alloc] initWithCapacity:128];
	
	[self saveMainMapHeaderForLevels:1 usingMapDataSize:levelLength];
	mapHeaderData = mapDataToSave;
	
	mapDataToSave = [[NSMutableData alloc] initWithCapacity:10];
	[self saveLevelHeaders:level usingMapDataSize:levelLength usingLocation:128 forLevelIndex:0];
	levelHeaderData = mapDataToSave;
	
	mapDataToSave = nil;
	
	#ifdef useDebuggingLogs
		NSLog(@" * The level header length after saving level into it:   %d", [levelHeaderData length]);
		NSLog(@" * The map header length after saving level into it:     %d", [mapHeaderData length]);
		NSLog(@" * The level data length after saving level into it:     %d", levelLength);
	#endif
	entireMapData = [[NSMutableData alloc] initWithCapacity:(500 * 1000)];
	
	[entireMapData appendData:mapHeaderData];
	[entireMapData appendData:levelData];
	[entireMapData appendData:levelHeaderData];
	
	[mapHeaderData release];
	[levelData release];
	[levelHeaderData release];
	
	#ifdef useDebuggingLogs
		NSLog(@"|*| Entire level data length after saving level into it:   %d", [entireMapData length]);
	#endif
	
	
	unsigned char *buffer = [entireMapData mutableBytes];
	long theLength = [entireMapData length];
	unsigned long theChecksum = calculate_data_crc(buffer, theLength);
	// at 68 for 4 bytes...
	#ifdef useDebuggingLogs
		NSLog(@"Checksum In Single Level: %d", theChecksum);
	#endif
	NSRange checksumRange = {68, 4};
	[entireMapData replaceBytesInRange:checksumRange withBytes:&theChecksum];
	
	return [entireMapData autorelease];
}

- (void)saveObjectsForLevel:(LELevelData *)level
{
	//theDataToReturn = [[NSMutableArray allocWithZone:[self zone]] initWithCapacity:(length / 16)];
	NSArray *theObjects = [level getTheMapObjects];
	long objCount = [theObjects count];
	id currentObj = nil;
	
	if (objCount < 1)
		return;
	
	[self saveEntryHeader:'OBJS' next_offset:[mapDataToSave length] length:(objCount * 16 /* objs length */) offset:0];
	
	NSEnumerator *numer = [theObjects objectEnumerator];
	while (currentObj = [numer nextObject])
	{
		[self saveShort:[currentObj getType]];
		[self saveShort:[currentObj getObjTypeIndex]];
		[self saveShort:[currentObj getFacing]];
		[self saveShort:[currentObj getPolygonIndex]];
		[self saveShort:[currentObj getX]];
		[self saveShort:[currentObj getY]];
		[self saveShort:[currentObj getZ]];
		[self saveUnsignedShort:[currentObj getMapFlags]];
	}
	#ifdef useDebuggingLogs
		NSLog(@"Saved %d map objects (Monsters, Items, Etc.).", objCount);
	#endif
}

- (void)saveSidesForLevel:(LELevelData *)level
{
	//theDataToReturn = [[NSMutableArray allocWithZone:[self zone]] initWithCapacity:(length / 64)];
	NSArray *theObjects = [level getSides];
	long objCount = [theObjects count];
	id currentObj = nil;
	
	if (objCount < 1)
		return;
	
	[self saveEntryHeader:'SIDS' next_offset:[mapDataToSave length] length:(objCount * 64 /* objs length */) offset:0];
	
	NSEnumerator *numer = [theObjects objectEnumerator];
	while (currentObj = [numer nextObject])
	{
		struct side_texture_definition theTempSideTextureDefinition;
		struct side_exclusion_zone theTempExclusionZone;
		
		[self saveShort:[currentObj getType]];
		[self saveShort:[currentObj getFlags]];
		
		// ***
		
		theTempSideTextureDefinition = [currentObj getPrimary_texture];
		
		[self saveShort:theTempSideTextureDefinition.x0];
		[self saveShort:theTempSideTextureDefinition.y0];
		//theTempSideTextureDefinition.texture = [self getShort]; // 3oisudjlifslkf sujdlifj ldsf
		//theCursor -= 2;
		[self saveShort:theTempSideTextureDefinition.texture];
		//[self saveOneByteShort:theTempSideTextureDefinition.textureCollection];
		//[self saveOneByteShort:/*(char)*/theTempSideTextureDefinition.textureNumber]; // *** May Need to Cast It??? ***
		
		// ---
		
		theTempSideTextureDefinition = [currentObj getSecondary_texture];
		
		[self saveShort:theTempSideTextureDefinition.x0];
		[self saveShort:theTempSideTextureDefinition.y0];
		//theTempSideTextureDefinition.texture = [self getShort];
		//theCursor -= 2;
		[self saveShort:theTempSideTextureDefinition.texture];
		//[self saveOneByteShort:theTempSideTextureDefinition.textureCollection = [self getOneByteShort]];
		//[self saveOneByteShort:theTempSideTextureDefinition.textureNumber = [self getOneByteShort]];
		
		// ---
		
		theTempSideTextureDefinition = [currentObj getTransparent_texture];
		
		[self saveShort:theTempSideTextureDefinition.x0];
		[self saveShort:theTempSideTextureDefinition.y0];
		//theTempSideTextureDefinition.texture = [self getShort];
		//theCursor -= 2;
		[self saveShort:theTempSideTextureDefinition.texture];
		//[self saveOneByteShort:theTempSideTextureDefinition.textureCollection];
		//[self saveOneByteShort:theTempSideTextureDefinition.textureNumber];
		
		// ***
		
		theTempExclusionZone = [currentObj getExclusion_zone];
		
		[self saveShort:theTempExclusionZone.e0.x];
		[self saveShort:theTempExclusionZone.e0.y];
		[self saveShort:theTempExclusionZone.e1.x];
		[self saveShort:theTempExclusionZone.e1.y];
		[self saveShort:theTempExclusionZone.e2.x];
		[self saveShort:theTempExclusionZone.e2.y];
		[self saveShort:theTempExclusionZone.e3.x];
		[self saveShort:theTempExclusionZone.e3.y];
			
		[self saveShort:[currentObj getControl_panel_type]];
		[self saveShort:[currentObj getControl_panel_permutation]];
			
		[self saveShort:[currentObj getPrimary_transfer_mode]];
		[self saveShort:[currentObj getSecondary_transfer_mode]];
		[self saveShort:[currentObj getTransparent_transfer_mode]];
		
		[self saveShort:[currentObj getPolygon_index]];
		[self saveShort:[currentObj getLine_index]];
		
		[self saveShort:[currentObj getPrimary_lightsource_index]];
		[self saveShort:[currentObj getSecondary_lightsource_index]];
		[self saveShort:[currentObj getTransparent_lightsource_index]];
		
		[self saveLong:[currentObj getAmbient_delta]];
		
		[self saveEmptyBytes:2]; //Skip the unused part... :)
	}
	#ifdef useDebuggingLogs
		NSLog(@"Saved %d side objects.", objCount);
	#endif
}

- (void)saveLightsForLevel:(LELevelData *)level
{
	//theDataToReturn = [[NSMutableArray allocWithZone:[self zone]] initWithCapacity:(length / 100)];
	NSArray *theObjects = [level getLights];
	long objCount = [theObjects count];
	id currentObj = nil;
	
	if (objCount < 1)
		return;
	
	[self saveEntryHeader:'LITE' next_offset:[mapDataToSave length] length:(objCount * 100 /* light length */) offset:0];
	
	NSEnumerator *numer = [theObjects objectEnumerator];
	while (currentObj = [numer nextObject])
	{
		int i;
		
		[self saveShort:[currentObj getType]];
		[self saveUnsignedShort:[currentObj getFlags]];
		
		[self saveShort:[currentObj getPhase]];
		
		for (i = 0; i < 6; i++)
		{
			[self saveShort:[currentObj getFunction_forState:i]];
			[self saveShort:[currentObj getPeriod_forState:i]];
			[self saveShort:[currentObj getDelta_period_forState:i]];
			[self saveLong:[currentObj getIntensity_forState:i]]; 
			[self saveLong:[currentObj getDelta_intensity_forState:i]];
		}
		
		[self saveShort:[currentObj getTag]];
		
		[self saveEmptyBytes:8]; //Skip the unused part... :)
	}
	#ifdef useDebuggingLogs
		NSLog(@"Saved %d light objects.", objCount);
	#endif
}

- (void)saveNotesForLevel:(LELevelData *)level
{
	//theDataToReturn = [[NSMutableArray allocWithZone:[self zone]] initWithCapacity:(length / 72)];
	
	NSArray *theObjects = [level getNotes];
	long objCount = [theObjects count];
	id currentObj = nil;
	
	if (objCount < 1)
		return;
	
	[self saveEntryHeader:'NOTE' next_offset:[mapDataToSave length] length:(objCount * 72 /* annotation length */) offset:0];
	
	NSEnumerator *numer = [theObjects objectEnumerator];
	while (currentObj = [numer nextObject])
	{
		[self saveShort:[currentObj getType]];
		
		[self saveShort:[currentObj getLocation].x];
		[self saveShort:[currentObj getLocation].y];
		[self saveShort:[currentObj getPolygon_index]];
		
		[self saveStringAsChar:[currentObj getText] withLength:64];
		
	}
	#ifdef useDebuggingLogs
		NSLog(@"Saved %d annotation objects.", objCount);
	#endif
}

- (void)saveMediasForLevel:(LELevelData *)level
{
	//theDataToReturn = [[NSMutableArray allocWithZone:[self zone]] initWithCapacity:(length / 32)];
	NSArray *theObjects = [level getMedia];
	long objCount = [theObjects count];
	id currentObj = nil;
	
	if (objCount < 1)
		return;
	
	[self saveEntryHeader:'medi' next_offset:[mapDataToSave length] length:(objCount * 32 /* media length */) offset:0];
	
	NSEnumerator *numer = [theObjects objectEnumerator];
	while (currentObj = [numer nextObject])
	{	
		[self saveShort:[currentObj getType]];
		[self saveUnsignedShort:[currentObj getFlags]];
		
		[self saveShort:[currentObj getLight_index]];
		
		[self saveShort:[currentObj getCurrent_direction]];
		[self saveShort:[currentObj getCurrent_magnitude]];
		
		[self saveShort:[currentObj getLow]];
		[self saveShort:[currentObj getHigh]];
		
		[self saveShort:[currentObj getOrigin].x];
		[self saveShort:[currentObj getOrigin].y];
		
		[self saveShort:[currentObj getHeight]];
		
		[self saveLong:[currentObj getMinimum_light_intensity]]; // ??? Should Make Object Pointer ???
		[self saveShort:[currentObj getTexture]];
		[self saveShort:[currentObj getTransfer_mode]];
		
		[self saveEmptyBytes:4]; //Skip the unused part... :)
	}
	#ifdef useDebuggingLogs
		NSLog(@"Saved %d media (water, lava, etc.) objects.", objCount);
	#endif
}

- (void)saveAmbientSoundsForLevel:(LELevelData *)level
{
	//theDataToReturn = [[NSMutableArray allocWithZone:[self zone]] initWithCapacity:(length / 16)];
	NSArray *theObjects = [level getAmbientSounds];
	long objCount = [theObjects count];
	id currentObj = nil;
	
	if (objCount < 1)
		return;
	
	[self saveEntryHeader:'ambi' next_offset:[mapDataToSave length] length:(objCount * 16 /* object length */) offset:0];
	NSEnumerator * numer = [theObjects objectEnumerator];
	while (currentObj = [numer nextObject])
	{
		[self saveUnsignedShort:[currentObj getFlags]];
		
		[self saveShort:[currentObj getSound_index]];
		[self saveShort:[currentObj getVolume]];
		
		[self saveEmptyBytes:10]; //Skip the unused part... :)
	}
	#ifdef useDebuggingLogs
		NSLog(@"Saved %d ambient sound objects.", objCount);
	#endif
}

- (void)saveRandomSoundsForLevel:(LELevelData *)level
{
	//theDataToReturn = [[NSMutableArray allocWithZone:[self zone]] initWithCapacity:(length / 28)];
	NSArray *theObjects = [level getRandomSounds];
	long objCount = [theObjects count];
	id currentObj = nil;
	
	if (objCount < 1)
		return;
	
	[self saveEntryHeader:'bonk' next_offset:[mapDataToSave length] length:(objCount * 32 /* random_sound length */) offset:0];
	
	NSEnumerator *numer = [theObjects objectEnumerator];
	while (currentObj = [numer nextObject])
	{
		[self saveShort:[currentObj getFlags]];
		[self saveShort:[currentObj getSound_index]];
		[self saveShort:[currentObj getVolume]];
		[self saveShort:[currentObj getDelta_volume]];
		[self saveShort:[currentObj getPeriod]];
		[self saveShort:[currentObj getDelta_period]];
		[self saveShort:[currentObj getDirection]];
		[self saveShort:[currentObj getDelta_direction]];
		[self saveLong:[currentObj getPitch]];
		[self saveLong:[currentObj getDelta_pitch]];
		[self saveShort:[currentObj getPhase]];
		
		[self saveEmptyBytes:6]; //Skip the unused part... :)
	}
	#ifdef useDebuggingLogs
		NSLog(@"Saved %d random sound objects.", objCount);
	#endif
}

- (void)saveItemPlacementForLevel:(LELevelData *)level
{
	//theDataToReturn = [[NSMutableArray allocWithZone:[self zone]] initWithCapacity:(length / 12)];
	NSArray *theObjects = [level getItemPlacement];
	long objCount = [theObjects count];
	id currentObj = nil;
	
	if (objCount < 1)
	return;
	
	[self saveEntryHeader:'plac' next_offset:[mapDataToSave length] length:(objCount * 12 /* objs length */) offset:0];
	
	NSEnumerator *numer = [theObjects objectEnumerator];
	while (currentObj = [numer nextObject])
	{
	[self saveShort:[currentObj getFlags]];
	
	[self saveShort:[currentObj getInitial_count]];
	[self saveShort:[currentObj getMinimum_count]];
	[self saveShort:[currentObj getMaximum_count]];
	
	[self saveShort:[currentObj getRandom_count]];
	[self saveUnsignedShort:[currentObj getRandom_chance]];
	}
	#ifdef useDebuggingLogs
		NSLog(@"Saved %d item placement objects.", objCount);
	#endif
}

- (void)savePlatformsForLevel:(LELevelData *)level
{
	//theDataToReturn = [[NSMutableArray allocWithZone:[self zone]] initWithCapacity:(length / 32)];
	NSArray *theObjects = [level getPlatforms];
	long objCount = [theObjects count];
	id currentObj = nil;
	
	if (objCount < 1)
	return;
	
	[self saveEntryHeader:'plat' next_offset:[mapDataToSave length] length:(objCount * 32 /* platform length */) offset:0];
	
	NSEnumerator *numer = [theObjects objectEnumerator];
	while (currentObj = [numer nextObject])
	{
	[self saveShort:[currentObj getType]];
	[self saveShort:[currentObj getSpeed]];
	[self saveShort:[currentObj getDelay]];
	[self saveShort:[currentObj getmaximum_height]];
	[self saveShort:[currentObj getminimum_height]];
	[self saveUnsignedLong:[currentObj getStatic_flags]];
	[self saveShort:[currentObj getPolygon_index]];
	[self saveShort:[currentObj getTag]];
	
	[self saveEmptyBytes:14]; //Skip the unused part... :)
	}
	#ifdef useDebuggingLogs
		NSLog(@"Saved %d platform objects.", objCount);
	#endif
}

- (void)saveTerminalDataForLevel:(LELevelData *)level
{
	//theDataToReturn = [[NSMutableArray allocWithZone:[self zone]] initWithCapacity:(length / 28)];
	NSArray *theObjects = [level getTerminals];
	long objCount = [theObjects count];
	id currentObj = nil;
	
	if (objCount < 1)
		return;
	
	NSEnumerator *numer = [theObjects objectEnumerator];
	{
		NSMutableData *theTerminalData = [[NSMutableData alloc] initWithCapacity:0];
		while (currentObj = [numer nextObject])
			[theTerminalData appendData:[currentObj getTerminalAsMarathonData]];
			
		[self saveEntryHeader:'term' next_offset:[mapDataToSave length] length:[theTerminalData length] offset:0];
					//	Proably extra blank space for expation, I guess???
		[self saveData:theTerminalData];
		
		[theTerminalData release];
	}
}

"""
