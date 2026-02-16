# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Lookup
from django.db.models.fields import Field

class ItemVariety(models.Model):
	variety_id = models.IntegerField(default=0, primary_key=True)
	name = models.CharField(max_length=200)

	def __str__(self):
		return '{}: {}'.format(self.variety_id, self.name)

class Stat(models.Model):
	#TODO: Add all percent stats and fix the display text (names are inconsistent)
	#Stats that should display with a % appending the amount
	PERCENT_STATS = [202, 205, 208]

	stat_id = models.IntegerField(default=0, primary_key=True)
	name = models.CharField(max_length=200)

	def __str__(self):
		return '{}: {}'.format(self.stat_id, self.name)

	def get_display_text(self, amount):
		# hit chance
		if self.stat_id == 202:
			return '{}{}%'.format('+' if amount > 0 else '', amount * 5)
		else:
			return '{}{}{}'.format('+' if amount > 0 else '', amount, '%' if self.stat_id in self.PERCENT_STATS else '')

class ObjectTemplate(models.Model):
	object_id = models.IntegerField(default=0, primary_key=True)
	name = models.CharField(max_length=200)
	graphic_template = models.IntegerField(null=True)
	graphic_sheet = models.IntegerField(null=True)
	base_icon_num = models.IntegerField(null=True)
	width = models.IntegerField(null=True)
	height = models.IntegerField(null=True)
	blockage_type = models.IntegerField(null=True)
	can_target = models.IntegerField(null=True)
	start_health = models.IntegerField(null=True)
	default_script = models.CharField(max_length=200)
	number_anim_steps_destroyed = models.IntegerField(null=True)
	which_icon_destroyed = models.IntegerField(null=True)
	block_move_when_destroyed = models.IntegerField(null=True)
	object_type = models.IntegerField(null=True)
	effect_when_slain = models.IntegerField(null=True)
	glow_type = models.IntegerField(null=True)
	anim_in_reverse = models.IntegerField(null=True)
	glow_trans = models.IntegerField(null=True)
	num_anim_steps = models.IntegerField(null=True)
	object_trait = models.IntegerField(null=True)
	in_space_offset_y = models.IntegerField(null=True)
	in_space_offset_x = models.IntegerField(null=True)
	graphic_coloradj = models.IntegerField(null=True)
	part_of_terrain = models.IntegerField(null=True)
	graphic_appearadj = models.IntegerField(null=True)
	light_level = models.IntegerField(null=True)
	glow_offset = models.IntegerField(null=True)

	def __str__(self):
		return '{}: {}'.format(self.object_id, self.name)

#TODO: take out some of the nullable-ness in some fields
class ItemTemplate(models.Model):
	item_id = models.IntegerField(default=0, primary_key=True)
	name = models.CharField(max_length=200)
	ability = models.IntegerField(null=True) #TODO: add ability foreign key
	level = models.IntegerField(null=True)
	variety = models.ForeignKey(ItemVariety, on_delete=models.CASCADE)
	value = models.IntegerField(null=True)
	weight = models.IntegerField(null=True)
	charges = models.IntegerField(null=True)
	protection = models.IntegerField(null=True)
	can_augment = models.IntegerField(null=True)
	
	extra_description = models.IntegerField(null=True)
	graphic_sheet = models.IntegerField(null=True)
	graphic_template = models.IntegerField(null=True)
	which_icon_ground = models.IntegerField(null=True)
	which_icon_inven = models.IntegerField(null=True)
	graphic_color_adj = models.IntegerField(null=True)

	def __str__(self):
		return '{}: {}; type: {}'.format(self.item_id, self.name, self.variety.name)

	def get_display_text(self):
		return '{}'.format(self.name)

	def get_display_weight(self):
		weight = str(self.weight)
		if weight[-1] == 0:
			return '{} lbs'.format(weight[:-1])
		else:
			return '{}.{} lbs'.format(weight[:-1], weight[-1])

class ItemStat(models.Model):
	item = models.ForeignKey(ItemTemplate, on_delete=models.CASCADE)
	stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
	amount = models.IntegerField()
	is_pet_stat = models.IntegerField()

	def __str__(self):
		return '[{}, {}]: +{}; is_pet: {}'.format(self.item, self.stat, self.amount, self.is_pet_stat)

	def getDisplayStat(self):
		display = ''
		stat_type = self.stat.stat_id
		amount = self.amount
		if stat_type == 6: #armor
			display = '{}: +{}%'.format(stat_type, amount)
		else:
			display = '{} to {}'.format(self.stat.get_display_text(self.amount), self.stat.name)
		if self.is_pet_stat:
			display = display + ' of creations'
		return display

class Zone(models.Model):
	zone_id = models.IntegerField(default=0, primary_key=True)
	name = models.CharField(max_length=200)
	town_script = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	def get_script(self):
		return '{}.txt'.format(self.name)

	def get_dialog_script(self):
		return '{}dlg.txt'.format(self.name)

class ZoneObject(models.Model):
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
	object_template = models.ForeignKey(ObjectTemplate, on_delete=models.CASCADE)
	x_pos = models.IntegerField()
	y_pos = models.IntegerField()
	x_offset = models.IntegerField()
	y_offset = models.IntegerField()
	override_script = models.CharField(max_length=200)
	flags = models.CharField(max_length=200)

	def __str__(self):
		return '{}'.format(self.object_template.name)

	def get_script(self):
		if self.override_script:
			return self.override_script
		else:
			return self.object_template.default_script

class ZoneItem(models.Model):
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
	item = models.ForeignKey(ItemTemplate, on_delete=models.CASCADE)
	x_pos = models.IntegerField()
	y_pos = models.IntegerField()
	x_offset = models.IntegerField()
	y_offset = models.IntegerField()
	charges = models.IntegerField(null=True)
	properties = models.IntegerField()

	def is_stealable(self):
		return 1 & self.properties > 0

	def in_container(self):
		return 2 & self.properties > 0

	def __str__(self):
		return '{}; zone {}; x: {}; y: {}; charges: {}; stealable: {}; in container:{}'.format(self.item.name, self.zone_id, self.x_pos, self.y_pos, self.charges, self.is_stealable(), self.in_container())

class CreatureTemplate(models.Model):
	creature_id = models.IntegerField(default=0, primary_key=True)
	cr_name = models.CharField(max_length=200)
	cr_regen_rate = models.IntegerField(null=True)
	cr_max_health = models.IntegerField(null=True)
	cr_max_essence = models.IntegerField(null=True)
	cr_max_energy = models.IntegerField(null=True)
	cr_graphic_template = models.IntegerField()
	cr_energy_regen_rate = models.IntegerField(null=True)
	cr_default_script = models.CharField(max_length=200)
	cr_default_courage = models.IntegerField(null=True)
	cr_default_aggression = models.IntegerField()
	cr_base_level = models.IntegerField()
	cr_size = models.IntegerField()
	cr_sound_when_slain = models.IntegerField(null=True)
	cr_default_strategy = models.IntegerField(null=True)
	cr_graphic_coloradj = models.IntegerField(null=True)
	cr_bonus_aps = models.IntegerField(null=True)
	cr_stain_when_slain = models.IntegerField(null=True)
	cr_graphic_appearadj = models.IntegerField(null=True)
	cr_walk_speed = models.IntegerField(null=True)
	cr_effect_when_slain = models.IntegerField(null=True)
	cr_vert_adjust = models.IntegerField(null=True)
	cr_multiple_facings = models.IntegerField(null=True)
	cr_nimbleness = models.IntegerField(null=True)
	cr_missile_firing_height = models.IntegerField(null=True)

	def __str__(self):
		return '{}: {}'.format(self.creature_id, self.cr_name)

class CreatureTemplateItemDrop(models.Model):
	creature = models.ForeignKey(CreatureTemplate, on_delete=models.CASCADE)
	item = models.ForeignKey(ItemTemplate, on_delete=models.CASCADE)
	chance = models.IntegerField()

	def __str__(self):
		return '{} {} chance: {}'.format(self.creature, self.item, self.chance)

class ConversationNode(models.Model):
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
	node_id = models.IntegerField()
	state = models.IntegerField(default=-1)
	next_state = models.IntegerField(default=-1)
	condition = models.CharField(max_length=200)
	question = models.CharField(max_length=200)
	text = models.CharField(max_length=2000)
	code = models.CharField(max_length=2000)
	action = models.CharField(max_length=200)

class ZoneCreature(models.Model):
	zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
	zone_creature_id = models.IntegerField()
	creature_template = models.ForeignKey(CreatureTemplate, on_delete=models.CASCADE)
	override_script = models.CharField(max_length=200)
	x_pos = models.IntegerField()
	y_pos = models.IntegerField()
	x_offset = models.IntegerField()
	y_offset = models.IntegerField()
	flags = models.CharField(max_length=200)
	extra_items = models.CharField(max_length=200)
	attitude = models.IntegerField(null=True) # TODO: parse out enum for attitude, personality; see set_attitude(cr_id, attitude)
	personality = models.IntegerField(null=True)

	#todo: should change this to just be comma delimited integers instead of [] format
	def get_extra_item_ids(self):
		itemstr = self.extra_items.strip('[]')
		item_split = itemstr.split(', ')
		items = []
		if len(item_split) > 0:
			items.append(item_split[0])
		if len(item_split) > 2:
			items.append(item_split[2])
		return items

	def get_extra_item_chances(self):
		itemstr = self.extra_items.strip('[]')
		item_split = itemstr.split(', ')
		items = []
		if len(item_split) > 1:
			items.append(item_split[1])
		if len(item_split) > 3:
			items.append(item_split[3])
		return items
		

	def get_items(self):
		items = []
		ids = self.get_extra_item_ids()
		chances = self.get_extra_item_chances()
		print(ids)
		for item_id, chance in zip(ids, chances):
			items.append((ItemTemplate.objects.get(item_id = item_id), chance))
		template_items = CreatureTemplateItemDrop.objects.filter(creature_id = self.creature_template.creature_id)
		for template_item in template_items:
			items.append((template_item.item, template_item.chance))
		print(items)
		return items
		

	def __str__(self):
		return 'zone {}: {}: {}'.format(self.zone, self.creature_template.creature_id, self.creature_template.cr_name)
		






