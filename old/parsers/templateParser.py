#!usr/bin/python

import sys
import argparse	
import re
import copy
from pprint import pprint

'''Parser for going through the geneforge 5 template files. Currently includes parsing creatures and items ("gf5itemschars"), abilities and objects("gf5objsmisc"), and floor and terrain ("gf5floorster"). Adding additional parsing for projectiles, sfx, etc. can be done by adding the correct term and prefix, and removal list.

The general approach used in the template lists is to begin defining new templates with the current values used from the previous template. This allowed the ability to quickly create multiple copies of similar templates with only one or two differences (some stats or graphics changes usually). If import is used, then instead of using the previously parsed template, we import from another previously parsed template. The import number is always above the currently parsing template to ensure that its information is available in a single read.

The removal list dictionary is a dictionary of field value keys that will remove all attributes associated with the key if a value of -1 is reached. For example, reaching "it_stats_to_affect" = -1 will remove "it_stats_to_affect" and "it_stats_addition" for whatever number stat is being removed. If "it_stats_addition" = -1 is reached, this is presumed to mean that a stat of -1 is applied (nothing is removed from the current item.

I got a little lazy with the copy pasting on the different types, that could be improved. Also might be missing a couple things in the remove list dictionaries.'''

creatureremovelists_dict = {'cr_graphic_appearadj' : ['cr_graphic_appearadj'],
'cr_abil_num' : ['cr_abil_num', 'cr_abil_level', 'cr_abil_step_of_launch', 'cr_abil_anim_in_reverse', 'cr_abil_casting_sound'],
'cr_start_item' : ['cr_start_item', 'cr_start_item_chance'],
'cr_stain_when_slain' : ['cr_stain_when_slain']}

itemremovelists_dict = {'it_extra_description' : ['it_extra_description'],
'it_ability' : ['it_ability'],
'it_pet_stats_to_affect' : ['it_pet_stats_to_affect', 'it_pet_stats_addition'],
'it_stats_to_affect' : ['it_stats_to_affect', 'it_stats_addition']}

objectremovelists_dict = {'ob_effect_when_slain' : ['ob_effect_when_slain'],
'ob_glow_type' : ['ob_glow_type']}

abilityremovelists_dict = {'ab_stat_for_ability_bonus' : ['ab_stat_for_ability_bonus'],
'ab_impact_sound' : ['ab_impact_sound'],
'ab_impact_sfx_effect' : ['ab_impact_sfx_effect'],
'ab_effect_type' : ['ab_effect_type'],
'ab_status_effect' : ['ab_status_effect'],
'ab_graphic_type' : ['ab_graphic_type']}

floorremovelists_dict = {}

terrainremovelists_dict = {}

#currently supported parsing types
typelist = ['creature', 'item', 'object', 'ability', 'floor', 'terrain']
prefixlist = ['cr', 'it', 'ob', 'ab', 'fl', 'tr']

def main():
	inputfilename = ''
	outputfilename = ''
	parser = argparse.ArgumentParser(description='Parses the items and creatures in the GF5 script file')
	parser.add_argument('-i', '--input', help='input file name')
	parser.add_argument('-o', '--output', help='output file name')
	parser.add_argument('-t', '--type', help='parse type (item, creature)')
	args = parser.parse_args()
	inputfilename = args.input
	outputfilename = args.output
	parsetype = args.type
	if inputfilename and parsetype in typelist:
		type_dict = {}
		if parsetype == 'item':
			type_dict = parseItems(inputfilename)
		elif parsetype == 'creature':
			type_dict = parseCreatures(inputfilename)
		elif parsetype == 'ability':
			type_dict = parseAbilities(inputfilename)
		elif parsetype == 'floor':
			type_dict = parseFloors(inputfilename)
		elif parsetype == 'object':
			type_dict = parseObjects(inputfilename)
		elif parsetype == 'terrain':
			type_dict = parseTerrain(inputfilename)

		if outputfilename:
			sys.stdout = open(outputfilename, 'w')
		prettyPrintType(parsetype, type_dict)
		if outputfilename:
			sys.stdout.close()
	else:
		if not parsetype in typelist:
			print('Need a type in ' + typelist)
		if not inputfilename:
			print('Need an input file to parse')

def prettyPrintType(parsetype, type_dict):
	for key in sorted(type_dict):
		typename = ''
		namekey = prefixlist[typelist.index(parsetype)] + '_name'
		if namekey in type_dict[key]:
			typename = type_dict[key][namekey]
		print(parsetype + ' ' + str(key) + ' ' + typename)
		pprint(type_dict[key])
		print()

def parseItems(filename):
	return parseType('item', '^it_', filename, itemremovelists_dict)

def parseCreatures(filename):
	return parseType('creature', '^cr_', filename, creatureremovelists_dict)

def parseObjects(filename):
	return parseType('object', '^ob_', filename, objectremovelists_dict)

def parseAbilities(filename):
	return parseType('ability', '^ab_', filename, abilityremovelists_dict)

def parseFloors(filename):
	return parseType('floor', '^fl_', filename, floorremovelists_dict)

def parseTerrain(filename):
	return parseType('terrain', '^tr_', filename, terrainremovelists_dict)

def parseType(templatename, templateprefix, filename, removelists_dict):
	template_dict = {}
	with open(filename, newline = '\r') as f:
		lines = f.readlines()

		currentid = -1
		currenttempobj = {}
		for line in lines:
			text = line.strip()

			#only take lines before comments
			commentText = text.split('\/\/')[0]
			if len(commentText) == 0:
				continue

			# don't process comments
			#if re.match('^\/\/', text):
			#	continue
			
			# new item definition
			newtemplatephrase = 'begindefine'
			if re.match(newtemplatephrase, text):
				if int(currentid) > -1:
					template_dict[currentid] = currenttempobj
				#if we are on a different definition type, we should clear out everything
				if not re.match(newtemplatephrase + templatename, text):
					currenttempobj = {}
					currentid = -1
				else:
					# make a new copy to retain attributes but remove previous binding
					currenttempobj = copy.deepcopy(currenttempobj) 
					currentid = re.findall('\d+', text)[0]

			if currentid == -1:
				continue

			#imports
			if re.match('^import', text):
				importid = re.findall('\d+', text)[0]
				if importid in template_dict:
					currenttempobj = copy.deepcopy(template_dict[importid])
				else:
					print('missing ' + templatename + ' import ' + str(importid) + ' for new id ' + str(currentid))
					print('text: ' + text)
					currenttempobj = {}

			#attributes
			if re.match(templateprefix, text):
				prefix = text.split('=')[0].strip().split()
				fieldvalue = text.split('=')[1].split(';')[0].strip()

				fieldname = prefix[0]
				fieldnamekey = ''
				
				if len(prefix) == 2:
					fieldnamekey = prefix[1]
					if fieldname not in currenttempobj:
						currenttempobj[fieldname] = {}

				if fieldvalue == '-1' and (fieldname in removelists_dict):

					#remove all fields (potentially just sub-values if removing ones with field keys
					#We assume that the triggering field shares having or not having field keys with its
					#other removing fields
					for removefieldname in removelists_dict[fieldname]:
						if len(prefix) == 2:
							if removefieldname in currenttempobj:
								currenttempobj[removefieldname].pop(fieldnamekey, None)
								if len(currenttempobj[removefieldname]) == 0:
									currenttempobj.pop(removefieldname)
						else:
							if removefieldname in currenttempobj:
								currenttempobj.pop(removefieldname)
							#test
							else:
								print('{} template {} has no field {}'.format(templatename, currentid, removefieldname))
					continue
				
				if len(prefix) is 1:
					currenttempobj[fieldname] = fieldvalue.strip('"')
				else:
					field_dict = currenttempobj[fieldname]
					field_dict[fieldnamekey] = fieldvalue
				
	return template_dict

if __name__ == '__main__':
	main()
