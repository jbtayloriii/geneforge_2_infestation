import csv

from geneforge5.models import *
from django.db import connection

def delete_table(model):
	name = model._meta.db_table
	model.objects.all().delete()
	cursor = connection.cursor()
	
	sql = "DELETE FROM sqlite_sequence WHERE name = " + "'" + name + "'"
	cursor.execute(sql)

def with_iter(context):
	iterable = context
	with context:
		for value in iterable:
			yield value

def int_or_none(val):
	if val == '':
		return None
	return int(val)

def load_csv(filename):
	return csv.reader(with_iter(open('data/csv/' + filename , 'r')), delimiter=',')

def build_item_variety():
	print('building item variety table')
	delete_table(ItemVariety)

	csv = load_csv('item_variety.csv')

	for index, info in enumerate(csv):
		if index > 0:
			variety = ItemVariety(
				variety_id = int(info[0]),
				name = info[1],
			)
			variety.save()

def build_stat():
	print('building stat table')
	delete_table(Stat)

	csv = load_csv('stat_text.csv')

	for index, info in enumerate(csv):
		if index > 0:
			stat = Stat(
				stat_id = int(info[0]),
				name = info[1],
			)
			stat.save()

def build_object_template():
	print('building object template table')
	delete_table(ObjectTemplate)

	csv = load_csv('object_template.csv')
	for index, info in enumerate(csv):
		if index > 0:
			key = int(info[0])
			if key > 0:
				object_template = ObjectTemplate(
					object_id = int(info[0]),
					name = info[1],
					graphic_template = int_or_none(info[2]),
					graphic_sheet = int_or_none(info[3]),
					base_icon_num = int_or_none(info[4]),
					width = int_or_none(info[5]),
					height = int_or_none(info[6]),
					blockage_type = int_or_none(info[7]),
					can_target = int_or_none(info[8]),
					start_health = int_or_none(info[9]),
					default_script = info[10],
					number_anim_steps_destroyed = int_or_none(info[11]),
					which_icon_destroyed = int_or_none(info[12]),
					block_move_when_destroyed = int_or_none(info[13]),
					object_type = int_or_none(info[14]),
					effect_when_slain = int_or_none(info[15]),
					glow_type = int_or_none(info[16]),
					anim_in_reverse = int_or_none(info[17]),
					glow_trans = int_or_none(info[18]),
					num_anim_steps = int_or_none(info[19]),
					object_trait = int_or_none(info[20]),
					in_space_offset_y = int_or_none(info[21]),
					in_space_offset_x = int_or_none(info[22]),
					graphic_coloradj = int_or_none(info[23]),
					part_of_terrain = int_or_none(info[24]),
					graphic_appearadj = int_or_none(info[25]),
					light_level = int_or_none(info[26]),
					glow_offset = int_or_none(info[27]),
				)
				object_template.save()

def build_item_template():
	print('building item template table')
	delete_table(ItemTemplate)

	csv = load_csv('item_template.csv')
	for index, info in enumerate(csv):
		if index > 0:
			key = int(info[0])
			if key > 0:
				item_template = ItemTemplate(
					item_id = int(info[0]),
					name = info[1],
					ability = int_or_none(info[2]), #TODO: add ability foreign key
					level = int_or_none(info[3]),
					variety = ItemVariety.objects.get(variety_id = int(info[4])),
					value = int_or_none(info[5]),
					weight = int_or_none(info[6]),
					charges = int_or_none(info[7]),
					protection = int_or_none(info[12]),
					can_augment = int_or_none(info[15]),
	
					extra_description = int_or_none(info[13]),
					graphic_sheet = int_or_none(info[8]),
					graphic_template = int_or_none(info[9]),
					which_icon_ground = int_or_none(info[10]),
					which_icon_inven = int_or_none(info[11]),
					graphic_color_adj = int_or_none(info[14]),
				)
				item_template.save()

def build_item_stat():
	print('building item stat table')
	delete_table(ItemStat)

	csv = load_csv('item_stats.csv')
	for index, info in enumerate(csv):
		if index > 0:
			item_stat = ItemStat(
				item = ItemTemplate.objects.get(item_id = int(info[0])),
				stat = Stat.objects.get(stat_id = int(info[1])),
				amount = int(info[2]),
				is_pet_stat = int(info[3]),
			)
			item_stat.save()

def build_zone():
	print('building zone table')
	delete_table(Zone)

	csv = load_csv('zone/zones.csv')
	for index, info in enumerate(csv):
		if index > 0:
			zone = Zone(
				zone_id = int(info[0]),
				name = info[1],
				town_script = info[2],
			)
			zone.save()

def build_zone_object():
	print('building zone object table')
	delete_table(ZoneObject)

	csv = load_csv('zone/objects.csv')
	for index, info in enumerate(csv):
		if index > 0:
			zone_object = ZoneObject(
				zone = Zone.objects.get(zone_id = int(info[0])),
				# id = info[1]
				object_template = ObjectTemplate.objects.get(object_id = int(info[2])),
				x_pos = int(info[3]), #TODO: add ability foreign key
				y_pos = int(info[4]),
				x_offset = int(info[5]),
				y_offset = int(info[6]),
				override_script = info[7],
				flags = info[8],
			)
			zone_object.save()

def build_zone_item():
	print('building zone item table')
	delete_table(ZoneItem)

	csv = load_csv('zone/items.csv')
	for index, info in enumerate(csv):
		if index > 0:
			zone_item = ZoneItem(
				zone = Zone.objects.get(zone_id = int(info[0])),
				# id = info[1]
				item = ItemTemplate.objects.get(item_id = int(info[2])),
				x_pos = int(info[3]), #TODO: add ability foreign key
				y_pos = int(info[4]),
				x_offset = int(info[5]),
				y_offset = int(info[6]),
				charges = int_or_none(info[7]),
				properties = int_or_none(info[8]),
			)
			zone_item.save()

def build_creature_template():
	print('building creature template table')
	delete_table(CreatureTemplate)

	csv = load_csv('creature_template.csv')
	for index, info in enumerate(csv):
		if index > 0:
			creature_template = CreatureTemplate(
				creature_id = int(info[0]),
				cr_name = info[1],
				cr_regen_rate =int_or_none(info[2]),
				cr_max_health = int_or_none(info[3]),
				cr_max_essence = int_or_none(info[4]),
				cr_max_energy = int_or_none(info[5]),
				cr_graphic_template = int(info[6]),
				cr_energy_regen_rate = int_or_none(info[7]),
				cr_default_script = info[8],
				cr_default_courage = int_or_none(info[9]),
				cr_default_aggression = int(info[10]),
				cr_base_level = int_or_none(info[11]),
				cr_size = int(info[12]),
				cr_sound_when_slain = int_or_none(info[13]),
				cr_default_strategy = int_or_none(info[14]),
				cr_graphic_coloradj = int_or_none(info[15]),
				cr_bonus_aps = int_or_none(info[16]),
				cr_stain_when_slain = int_or_none(info[17]),
				cr_graphic_appearadj = int_or_none(info[18]),
				cr_walk_speed = int_or_none(info[19]),
				cr_effect_when_slain = int_or_none(info[20]),
				cr_vert_adjust = int_or_none(info[21]),
				cr_multiple_facings = int_or_none(info[22]),
				cr_nimbleness = int_or_none(info[23]),
				cr_missile_firing_height = int_or_none(info[24]),
			)
			creature_template.save()

def build_creature_template_item_drop():
	print('building creature template item drop table')
	delete_table(CreatureTemplateItemDrop)

	csv = load_csv('creature_template_item_drops.csv')
	for index, info in enumerate(csv):
		if index > 0:
			creature_template_item_drop = CreatureTemplateItemDrop(
				creature = CreatureTemplate.objects.get(creature_id = int(info[0])),
				item = ItemTemplate.objects.get(item_id = int(info[1])),
				chance = int(info[2]),
			)
			creature_template_item_drop.save()

def build_zone_creature():
	print('building zone creature table')
	delete_table(ZoneCreature)

	csv = load_csv('zone/creatures.csv')
	for index, info in enumerate(csv):
		if index > 0:
			zone_creature = ZoneCreature(
				zone = Zone.objects.get(zone_id = int(info[0])),
				zone_creature_id = int(info[1]),
				creature_template = CreatureTemplate.objects.get(creature_id = int(info[2])),
				override_script = info[3],
				x_pos = int(info[4]),
				y_pos = int(info[5]),
				x_offset = int(info[6]),
				y_offset = int(info[7]),
				flags = info[8],
				extra_items = info[9],
				attitude = int_or_none(info[10]),
				personality = int_or_none(info[11]),
			)
			zone_creature.save()

def build_db():
	#build_item_variety()
	#build_stat()
	#build_object_template()
	#build_item_template()
	#build_item_stat()
	#build_zone()
	#build_zone_object()
	#build_zone_item()
	#build_creature_template()
	#build_creature_template_item_drop()
	build_zone_creature()
