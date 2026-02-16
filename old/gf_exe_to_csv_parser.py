import os
import csv

GENEFORGE_FILE_DIR = os.path.join(os.path.expanduser('~'), '.wine/drive_c/Program Files (x86)/Spiderweb Software/Geneforge 5')

GENEFORGE_EXE_FILE_PATH = os.path.join(GENEFORGE_FILE_DIR, 'Geneforge 5.exe')
STAT_TEXT_FILEPATH = 'data/csv/stat_text.csv'

SPELL_NAMES_OFFSET = 218788 * 16
SPELL_NAME_SIZE = 16 * 16

HARD_CODED_STAT_DICT = {
	8:'Creation Armor',
	100: 'Spore Baton',
	200: 'Melee Damage Protection',
	201: 'Action Points',
	202: 'chance to hit',
	203: 'combat damage levels',
	204: 'hostile effect resistance',
	205: 'energy resistance',
	206: 'fire resistance',
	207: 'poison resistance',
	208: 'acid resistance',
	210: 'mind effect resistance',
	211: 'stun resistance',
	212: 'cold resistance',
	213: 'damage shield',
	214: 'energy preservation',
	215: 'stealth',
	216: 'damage vs undead, constucts',
	217: 'vampiric touch',
	220: 'blessing',
	221: 'fire essence',
	222: 'cold essence',
	223: 'acid infusion',
	224: 'curse power',
	225: 'magic essence',
	226: 'speed',
	227: 'spines',
	228: 'stability',
	229: 'strong blessing',
}

STAT_PROP_LIST = ['name']

def parse_exe():
	print('parsing exe file')
	stat_dict = {}
	with open(GENEFORGE_EXE_FILE_PATH, 'rb') as inputfile:
		inputfile.seek(SPELL_NAMES_OFFSET)
		for x in range(99):
			stat_name = bin_to_string(inputfile.read(SPELL_NAME_SIZE))
			if stat_name:
				stat_dict[x] = stat_name
	stat_dict.update(HARD_CODED_STAT_DICT)
	basic_dict_to_csv(STAT_TEXT_FILEPATH, stat_dict, STAT_PROP_LIST)

def basic_dict_to_csv(filepath, obj_dict, prop_list):
	with open(filepath, 'w+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['id'] + prop_list)
		for key, val in sorted(obj_dict.items()):
			row = [key, val]
			writer.writerow(row)

def bin_to_string(dataslice):
	binStr = ''
	for val in dataslice:
		if val in range(32, 127):
			binStr += chr(val)
		else:
			break
	return binStr
