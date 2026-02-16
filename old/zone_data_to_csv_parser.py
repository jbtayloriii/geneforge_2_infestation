import os
import csv

import parsers.zoneParser as zoneParser

GENEFORGE_FILE_DIR = os.path.join(os.path.expanduser('~'), '.wine/drive_c/Program Files (x86)/Spiderweb Software/Geneforge 5/Geneforge 5 Files')
GENEFORGE_DATA_FILE_PATH = os.path.join(GENEFORGE_FILE_DIR, 'aGF5ScenData.dat')
FILEPATH_ZONE = 'data/csv/zone/zones.csv'
FILEPATH_ZONE_ITEMS = 'data/csv/zone/items.csv'
FILEPATH_ZONE_OBJECTS = 'data/csv/zone/objects.csv'
FILEPATH_ZONE_CREATURES = 'data/csv/zone/creatures.csv'

""" Zone-specific headers """
ZONE_HEADER = ['name', 'script']
ITEM_ZONE_HEADER = ['id', 'item_template_id', 'x', 'y', 'x_offset', 'y_offset','charges', 'properties']
OBJECT_ZONE_HEADER = ['id', 'object_template_id', 'x', 'y', 'x_offset', 'y_offset', 'override_script', 'flags']
CREATURE_ZONE_HEADER = ['id', 'creature_template_id', 'override_script', 'x', 'y', 'x_offset', 'y_offset', 'flags', 'extraitems', 'start_attitude', 'personality']
CANISTER_ZONE_HEADER = ['zoneid', 'x', 'y', 'x_offset', 'y_offset']

def parse_zones():
	print('Parsing zone info to csv')
	with open(FILEPATH_ZONE, 'w+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['zone_id'] + ZONE_HEADER)

	with open(FILEPATH_ZONE_ITEMS, 'w+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['zone_id'] + ITEM_ZONE_HEADER)

	with open(FILEPATH_ZONE_OBJECTS, 'w+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['zone_id'] + OBJECT_ZONE_HEADER)

	with open(FILEPATH_ZONE_CREATURES, 'w+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['zone_id'] + CREATURE_ZONE_HEADER)		

	for zone in range(82):
		print('Parsing zone {}'.format(zone))
		zone_dict = zoneParser.parsezone(GENEFORGE_DATA_FILE_PATH, zone)
		item_dict = zone_dict['items']
		object_dict = zone_dict['objects']
		creature_dict = zone_dict['creatures']

		global_dict = zone_dict['global']

		zone_list_append_basic(FILEPATH_ZONE, zone, global_dict)
		
		zone_list_append_to_csv(FILEPATH_ZONE_ITEMS, zone, item_dict)
		zone_list_append_to_csv(FILEPATH_ZONE_OBJECTS, zone, object_dict)
		zone_list_append_to_csv(FILEPATH_ZONE_CREATURES, zone, creature_dict)

def zone_list_append_basic(filepath, zone_id, prop_dict):
	with open(filepath, 'a') as f:
		writer = csv.writer(f, delimiter=',')
		row = [zone_id]
		for prop, val in sorted(prop_dict.items()):
			row.append(val)
		writer.writerow(row)

def zone_list_append_to_csv(filepath, zone_id, obj_list):
	with open(filepath, 'a') as f:
		writer = csv.writer(f, delimiter=',')
		for obj in obj_list:
			row = [zone_id]
			for prop in obj:
				row.append(prop)
			writer.writerow(row)
