import csv
import os
import re

import parsers.templateParser as templateParser

GENEFORGE_FILE_DIR = os.path.join(os.path.expanduser('~'), '.wine/drive_c/Program Files (x86)/Spiderweb Software/Geneforge 5/Geneforge 5 Files')
GENEFORGE_DATA_FILE_PATH = os.path.join(GENEFORGE_FILE_DIR, 'aGF5ScenData.dat')

GENEFORGE_ITEM_CHAR_FILE_PATH = os.path.join(GENEFORGE_FILE_DIR, 'Scripts/gf5itemschars.txt')
GENEFORGE_OBJECT_MISC_FILE_PATH = os.path.join(GENEFORGE_FILE_DIR, 'Scripts/gf5objsmisc.txt')
TRAP_FILEPATH = os.path.join(GENEFORGE_FILE_DIR, 'Scripts/trapbox.txt')

ITEM_PROP_LIST = ['it_name', 'it_ability', 'it_level', 'it_variety', 'it_value', 'it_weight', 'it_charges', 'it_graphic_sheet', 'it_graphic_template', 'it_which_icon_ground', 'it_which_icon_inven', 'it_protection', 'it_extra_description', 'it_graphic_coloradj', 'it_can_augment']

OBJECT_PROP_LIST = ['ob_name', 'ob_graphic_template', 'ob_graphic_sheet', 'ob_base_icon_num', 'ob_width', 'ob_height', 'ob_blockage_type', 'ob_can_target', 'ob_start_health', 'ob_default_script', 'ob_num_anim_steps_destroyed', 'ob_which_icon_destroyed', 'ob_block_move_when_destroyed', 'ob_object_type', 'ob_effect_when_slain', 'ob_glow_type', 'ob_anim_in_reverse', 'ob_glow_trans', 'ob_num_anim_steps', 'ob_object_trait', 'ob_in_space_offset_y', 'ob_in_space_offset_x', 'ob_graphic_coloradj', 'ob_part_of_terrain', 'ob_graphic_appearadj', 'ob_light_level', 'ob_glow_offset',]

CREATURE_PROP_LIST = ['cr_name', 'cr_regen_rate', 'cr_max_health', 'cr_max_essence', 'cr_max_energy', 'cr_graphic_template', 'cr_energy_regen_rate', 'cr_default_script', 'cr_default_courage', 'cr_default_aggression', 'cr_base_level', 'cr_size', 'cr_sound_when_slain', 'cr_default_strategy', 'cr_graphic_coloradj', 'cr_bonus_aps', 'cr_stain_when_slain', 'cr_graphic_appearadj', 'cr_walk_speed', 'cr_effect_when_slain', 'cr_vert_adjust', 'cr_multiple_facings', 'cr_nimbleness', 'cr_missile_firing_height']

# TODO: add to new tables as necessary
CREATURE_OTHER_PROPS = ['cr_resistances', 'cr_abil_step_of_launch', 'cr_abil_num', 'cr_abil_level', 'cr_abil_anim_in_reverse', 'cr_statistic', 'cr_abil_time_per_step', 'cr_abil_casting_sound', 'cr_creature_type', 'cr_default_attitude', 'cr_start_item', 'cr_start_item_chance']

ITEM_VARIETY = ['Cloak', 'Armor', 'Weapon', 'Shield', 'Ring', 'Feet', 'Belt', 'Gloves', 'Usable', 'Ammunition', 'No Use', 'Throwable', 'Living Tool', 'Coins', 'Spore Baton', 'Necklace', 'Pants']


def parseAllToCsv():
	print('Parsing item templates to csv')
	item_dict = templateParser.parseItems(GENEFORGE_ITEM_CHAR_FILE_PATH)
	dict_to_csv('data/csv/item_template.csv', item_dict, ITEM_PROP_LIST)
	print()

	print('Parsing object templates to csv')
	object_dict = templateParser.parseObjects(GENEFORGE_OBJECT_MISC_FILE_PATH)
	dict_to_csv('data/csv/object_template.csv', object_dict, OBJECT_PROP_LIST)
	print()

	print('Parsing item template stats to csv')
	item_stats_to_csv('data/csv/item_stats.csv', item_dict)
	print()

	print('Parsing creature templates to csv')
	creature_dict = templateParser.parseCreatures(GENEFORGE_ITEM_CHAR_FILE_PATH)
	dict_to_csv('data/csv/creature_template.csv', creature_dict, CREATURE_PROP_LIST)
	print()

	print('Parsing creature template item drops to csv')
	creature_template_item_to_csv('data/csv/creature_template_item_drops.csv', creature_dict)
	print()

	print('Parsing trap effects text to csv')
	trap_text_to_csv(TRAP_FILEPATH, 'data/csv/trap_effect_text.csv')
	print()

	print('Parsing item variety list to csv')
	basic_list_to_csv('data/csv/item_variety.csv', ITEM_VARIETY)

def basic_list_to_csv(filepath, prop_list):
	with open(filepath, 'w+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['id', 'name'])
		for x in range(len(prop_list)):
			writer.writerow([(x + 1), prop_list[x]])

def creature_template_item_to_csv(filepath, creature_dict):
	with open(filepath, 'w+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['creature_id', 'item_id', 'item_drop_chance'])
		for key, val in sorted(creature_dict.items()):
			if 'cr_start_item' in val:
				for num in val['cr_start_item']:
					row = [key, val['cr_start_item'][num], val['cr_start_item_chance'][num]]
					writer.writerow(row)

def trap_text_to_csv(trap_filepath, trap_csv_filepath):
	p = re.compile(r'\/\/(?P<id>\d{2,3}) - (?P<name>.*)')
	trap_dict = {}
	with open(trap_filepath, 'r') as f:
		for line in f:
			match = p.search(line)
			if match:
				trap_id = match.group('id')
				trap_name = match.group('name')
				trap_dict[trap_id] = trap_name

	with open(trap_csv_filepath, 'w+') as f:
		writer = csv.writer(f, delimiter = ',')
		writer.writerow(['trap_id', 'trap_name'])
		for trap_id, trap_name in sorted(trap_dict.items()):
			writer.writerow([trap_id, trap_name])

def item_stats_to_csv(filepath, item_dict):
	with open(filepath, 'w+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['item_id', 'stat_affected', 'stat_amount', 'is_pet'])
		for key, val in sorted(item_dict.items()):
			if 'it_stats_to_affect' in val:
				for num in val['it_stats_to_affect']:
					row = [key, val['it_stats_to_affect'][num], val['it_stats_addition'][num], 0]
					writer.writerow(row)
			if 'it_pet_stats_to_affect' in val:
				for num in val['it_pet_stats_to_affect']:
					row = [key, val['it_pet_stats_to_affect'][num], val['it_pet_stats_addition'][num], 1]
					writer.writerow(row)


""" Takes a dictionary of template data and parses it into a csv file. The expected dictionary is keyed by an int ID and each value object is a single template dictionary containing some or all of the properties listed in prop_list. Note that there will be some an additional tier for some properties on a template where there is a many-to-one relationship. An example is stat ups on  equipment. """
def dict_to_csv(filepath, obj_dict, prop_list):
	with open(filepath, 'w+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['id'] + prop_list)
		for key, val in sorted(obj_dict.items()):
			row = [key]
			for prop in prop_list:
				if prop in val:
					row.append(val[prop])
				else:
					row.append('')
			writer.writerow(row)

