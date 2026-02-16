# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from models import *

_PIXEL_PER_COORD = 16

# Create your views here.

'''Returns the landing page'''
def indexView(request):
	return render(request, 'geneforge5/index.html')

'''Returns the list of zones in a map style'''
def zonesView(request):
	zones = Zone.objects.all()

	return render(request, 'geneforge5/zones.html', {
		'zones' : zones
	})

'''Returns the list of items in the game'''
def itemsView(request):
	items_all = ItemTemplate.objects.all()
	varieties = ItemVariety.objects.all()
	items = {}
	for variety in varieties:
		items[variety] = []

	for item in items_all:
		v = item.variety
		items[v].append(item)
		

	return render(request, 'geneforge5/items.html', {
		'item_list' : items,
	})

'''Returns the list of usable canisters in the game
TODO: Add canister checks?
'''
def canistersView(request):
	canister_template = get_object_or_404(ObjectTemplate, default_script = 'canister')
	canisters = ZoneObject.objects.filter(Q(override_script = 'canister') | Q(object_template__object_id = canister_template.object_id))

	stats = Stat.objects.all()
	canister_list = []

	p = re.compile(r'^\[(?P<flag_0>\d+), (?P<flag_1>\d+)')
	for canister in canisters:
		match = p.search(canister.flags)
		if match:
			skill_id = match.group('flag_0')
			if skill_id == '0':
				continue

			amount = match.group('flag_1')
			if amount == '0':
				amount = 1

			canister_list.append({
				'zone': canister.zone,
				'skill': stats.get(stat_id = skill_id).name,
				'amount': amount,
			})
	return render(request, 'geneforge5/canisters.html', {
		'canisters' : canister_list
	})

'''Returns the list of quests in the game
TODO: implement
'''
def questsView(request):
	get_object_or_404(ObjectTemplate, default_script = 'blah')

'''Returns the list of skills (magic and shaping) in the game
TODO: implement
'''
def skillsView(request):
	get_object_or_404(ObjectTemplate, default_script = 'blah')

'''Returns reputation changers and reputation checks in the game
TODO: implement
'''
def reputationView(request):
	get_object_or_404(ObjectTemplate, default_script = 'blah')

'''Returns special items (where gotten, where used) in the game
TODO: implement
'''
def specItemsView(request):
	get_object_or_404(ObjectTemplate, default_script = 'blah')

'''Returns shops in the game
TODO: implement
'''
def shopsView(request):
	get_object_or_404(ObjectTemplate, default_script = 'blah')

'''Returns crafting recipes and enhancing effects in the game
TODO: implement
'''
def craftingView(request):
	get_object_or_404(ObjectTemplate, default_script = 'blah')

'''Returns a single zone'''
def zoneView(request, zone_id):
	

	items = ZoneItem.objects.filter(zone_id = zone_id)
	creatures = ZoneCreature.objects.filter(zone_id = zone_id)

	selected_type = request.GET.get('sel_type', '')
	selected_id = request.GET.get('sel_id', '')

	# TODO: select a specific item if passed in
	if selected_type and selected_id:
		print('test' + selected_type)

	for item in items:
		item.x_pos = item.x_pos * _PIXEL_PER_COORD
		item.y_pos = item.y_pos * _PIXEL_PER_COORD

	return render(request, 'geneforge5/zone.html', {
		'zone_id' : zone_id,
		'items' : items,
		'creatures' : creatures,
	})

'''Returns a single item template'''
def itemTemplateView(request, item_template_id):
	def get_abilities(template, stats):
		abilities = []

		# TODO: after linking ability, pull broadsword/shortsword/elemental blade string
		if template.ability in [2,91]:
			abilities.append('Damage: {} to {}'.format(template.level, template.level * 4 ))

		if template.ability in [90, 92, 93, 94]:
			abilities.append('Damage: {} to {}'.format(template.level, template.level * 5 ))

		if template.protection:
			abilities.append('Armor: +{}%'.format(item_template.protection))
		for stat in stats:
			abilities.append(stat.getDisplayStat())

		if len(abilities) == 0:
			abilities.append('None')
		return abilities

	item_template = get_object_or_404(ItemTemplate, item_id = item_template_id)
	item_stats = ItemStat.objects.filter(item__item_id = item_template_id)

	context = {}
	context['zone_item'] = get_zone_item_context(item_template_id)

	context['item_weight'] = item_template.weight
	context['name'] = item_template.name
	context['abilities'] = get_abilities(item_template, item_stats)
	context['item_value'] = item_template.value

	return render(request, 'geneforge5/item_template.html', context)

'''Returns a single quest view
TODO: implement
'''
def questView(request):
	get_object_or_404(ObjectTemplate, default_script = 'blah')

'''Returns a single skill view
TODO: implement
'''
def skillView(request):
	get_object_or_404(ObjectTemplate, default_script = 'blah')

'''Returns a single shop view
TODO: implement
'''
def shopView(request):
	get_object_or_404(ObjectTemplate, default_script = 'blah')

def get_zone_item_context(item_id):
	items = ZoneItem.objects.filter(item__item_id = item_id)
	
	# TODO: be smarter about this?
	all_zone_creatures = ZoneCreature.objects.all()
	filtered_zone_creature_ids = [zoneCreature.id for zoneCreature in all_zone_creatures if ( item_id in zoneCreature.get_extra_item_ids())]
	creature_templates = CreatureTemplate.objects.filter(creaturetemplateitemdrop__in=CreatureTemplateItemDrop.objects.filter(item__item_id = item_id))

	print(creature_templates)
	zone_creatures = ZoneCreature.objects.filter(Q(creature_template__in=creature_templates) | Q(id__in = filtered_zone_creature_ids)).distinct()
	#creature_items = ZoneCreature.objects.filter(extra_items__creature_has_item =  item_id)

	return {
		'items': items,
		'zone_creatures': zone_creatures
	}
