#!usr/bin/python

import sys
import argparse
from collections import namedtuple

ZONE_SIZE = 52088
ZONE_INITIAL_OFFSET = 2560
FLOOR_OFFSET = 32
terrainoffset = 4128
itemoffset = 12320
objectoffset = 15840
CREATURE_OFFSET = 30176
OBJECT_OFFSET = 15840

inputfile = '../../gf5data/aGF5ScenData.dat'
creature_itemfile = '../../gf5data/gf5itemschars.txt'
outputfile = ''

def main():
	global inputfile
	global outputfile
	zone = -1

	parser = argparse.ArgumentParser(description='Pulls the creatures, tiles, items, and objects from a single zone. Will either write to a new csv file or will print to output')
	parser.add_argument('zone', help='zone number (pacification fields is zone 0)', type=int)
	parser.add_argument('-i', '--input', help='input .dat file for GF5 data')
	parser.add_argument('-o', '--output', help='output csv file to write to')
	args = parser.parse_args()
	if args.input:
		inputfile = args.input
	outputfile = args.output
	zone = args.zone
	
	if not inputfile:
		print('Missing input .dat GF5 file')
		sys.exit(2)
	zone_dict = parsezone(inputfile, zone)
	outputprint(zone_dict)

def outputprint(zdict):
	print(zdict['name'])
	print('Floor:')
	floor = zdict['floor']
	#print(floor)

	print('Terrain:')
	terrain = zdict['terrain']
	#print(terrain[0])

	print('Objects:')

	print('Items:')
	items = zdict['items']
	#print(items[134])

	print('Creatures:')
	creature_list = zdict['creatures']
	for val in creature_list:
		print(val)

def pullZone(zoneNumber, inputfname):
	with open(inputfname, 'rb') as inputfile:
		inputfile.seek(ZONE_INITIAL_OFFSET + (ZONE_SIZE * zoneNumber))
		data = inputfile.read(ZONE_SIZE)
		return data

def parsezone(inputfile, zone):		
	zonedata = pullZone(zone, inputfile)
	zone_dict = {}

	zone_dict['global'] = get_global_data(zonedata)
	getfloordata(zonedata, zone_dict)
	getterraindata(zonedata, zone_dict)
	zone_dict['items'] = get_item_list(zonedata)
	zone_dict['objects'] = getobjectdata(zonedata)
	zone_dict['creatures'] = get_creature_list(zonedata)
	zone_dict['doors'] = get_doors(zonedata)
	zone_dict['swingdoors'] = get_swingdoors(zonedata)
	
	return zone_dict

def bin_to_string(dataslice):
	binStr = ''
	for val in dataslice:
		if val in range(32, 127):
			binStr += chr(val)
		else:
			break
	return binStr


def getfloordata(data, zonedict):
	floor = []
	for i in range(0, 64):
		floorrow = []
		for j in range(0, 64):
			floorrow.append(data[i + FLOOR_OFFSET + (j * 64)])
		floor.append(floorrow)
	zonedict['floor'] = floor

def getterraindata(data, zonedict):
	terrain = []
	for i in range(0, 64):
		terrainrow = []
		for j in range(0, 64):
			terrainrow.append(data[i + terrainoffset + (j * 64)])
		terrain.append(terrainrow)

	zonedict['terrain'] = terrain

def get_item_list(data):
	items = []
	Item = namedtuple('Item', ['id', 'itemid','x', 'y', 'x_offset', 'y_offset', 'charges', 'properties'])
	for itemnum in range(0, 220):
		offset = itemoffset + itemnum * 16
		dataslice = data[offset:offset + 16]
		itemid = dataslice[0] + 256 * dataslice[1]
		if itemid < 0 or itemid >= 500:
			continue
		x_offset = dataslice[4]
		x = dataslice[5]
		y_offset = dataslice[8]
		y = dataslice[9]
		charges = dataslice[12] + 256 * dataslice[13]
		properties = dataslice[14]

		#Make sure we aren't misrepresenting charges/properties since we don't use that piece
		if dataslice[15] > 0:
			print('Detected extra item data that is not being calculated for item {}'.format(itemid))

		items.append(Item(itemnum, itemid, x, y, x_offset, y_offset, charges, properties))
	return items

def getobjectdata(data):
	object_list = []
	Object = namedtuple('Object', ['number', 'object_id', 'x', 'y', 'x_offset', 'y_offset', 'override_script', 'flags',])

	for objectnum in range(0, 256):
		offset = OBJECT_OFFSET + objectnum * 56
		dataslice = data[offset:offset + 56]
		object_id = dataslice[0] + 256 * dataslice[1]
		if object_id < 0 or object_id >= 500:
			continue
		x_offset = dataslice[4]
		x = dataslice[5]
		y_offset = dataslice[8]
		y = dataslice[9]
		override_script = bin_to_string(dataslice[12:23])
		flags = []
		for x in range(24, 42, 2):
			flags.append(dataslice[x] + 256 * dataslice[x + 1])
		object_list.append(Object(objectnum, object_id, x, y, x_offset, y_offset, override_script, flags))

	return object_list

def get_doors(data):
	pass

def get_swingdoors(data):
	pass

def get_creature_list(data):
	creatures = []
	Creature = namedtuple('Creature', ['number', 'creatureid', 'overridescript', 'x', 'y', 'x_offset', 'y_offset', 'flags', 'extraitems', 'attitude', 'personality'])

	for creaturenum in range(0, 108):
		offset = CREATURE_OFFSET + creaturenum * 80
		dataslice = data[offset:offset + 80]
		creatureid = dataslice[0] + 256 * dataslice[1]
		if creatureid < 0 or creatureid >= 256:
			continue
		x_offset = dataslice[4]
		xpos = dataslice[5]
		y_offset = dataslice[8]
		ypos = dataslice[9]
		override_script = bin_to_string(dataslice[12:23])

		flags = []
		for x in range(24, 42, 2):
			flags.append(dataslice[x] + 256 * dataslice[x + 1])

		extraitems = []
		for x in range(0, 2):
			extra_item_id = dataslice[44 + x * 2] + 256 * dataslice[45 + x * 2]
			if extra_item_id <= 0 or extra_item_id > 500:
				continue
			extra_item_chance = dataslice[48 + x * 2]
			extraitems.append(extra_item_id)
			extraitems.append(extra_item_chance)
		attitude = dataslice[54] + 256 * dataslice[55]
		personality = dataslice[60] + 256 * dataslice[61] # ?
		creatures.append(Creature(creaturenum, creatureid, override_script, xpos, ypos, x_offset, y_offset, flags, extraitems, attitude, personality))

	return creatures

if __name__ == '__main__':
	main()
