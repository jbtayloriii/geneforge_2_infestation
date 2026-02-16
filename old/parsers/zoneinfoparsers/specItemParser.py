#!usr/bin/python

'''
Parser used to get the quest toggles from all the relevant geneforge 5 scripts.

Will return a dict with keys of quest number, and values of lists of named tuples:
zone - integer
script - string
value - integer
'''

import re
import os
import argparse
from collections import namedtuple

setspecre = re.compile('set_spec_item\(\d+,-?\d+\)')
hasspecre = re.compile('has_spec_item\(\d+\)')

def main():
	inputFolder = ''
	parser = argparse.ArgumentParser(description='Finds all the special items in GF5 scripts')
	parser.add_argument('-i', '--input', help='input file folder')
	args = parser.parse_args()
	inputFolder = args.input
	if inputFolder:
		spec_dict = parseSpecs(inputFolder)
		#print(quest_dict)
		prettyPrintSpecs(spec_dict)
	else:
		print('Missing input folder')

def prettyPrintSpecs(spec_dict):
	for key in sorted(spec_dict):
		print('Item number ' + key)
		print('Setters:')
		for item in spec_dict[key]['set']:
			print(item)
		print('Getters:')
		for item in spec_dict[key]['get']:
			print(item)
		print()
		continue
		print('Zone  Value Script')
		for tupleval in quest_dict[key]:
			print('{0:>4} {2:>6} {1}'.format(*tupleval))
		print()

def parseSpecs(inputDir):
	spec_dict = {}

	for root, dirs, files in os.walk(inputDir):
		for filename in files:
			#test, change back
			if filename.startswith('z') and filename.endswith('.txt'):
				parseSpecFile(os.path.join(inputDir, filename), filename, spec_dict)
	return spec_dict

def parseSpecFile(filePath, fileName, spec_dict):
	SpecSet = namedtuple('SpecSet', ['zone', 'specitemid', 'value', 'script'])
	SpecCheck = namedtuple('SpecCheck', ['zone', 'specitemid', 'script'])
	zone = -1
	zoneSearch = re.search('[0-9]+', fileName)
	if not zoneSearch:
		return # don't search the template zones (they're empty anyways)
	zone = zoneSearch.group()

	# we're ignoring errors because some files are not utf-8 compliant
	with open(filePath, newline = '\r', errors = 'ignore') as f:		
		lines = f.readlines()
		for line in lines:
			text = line.strip()
			specsetmatches = setspecre.findall(text)
			spechasmatches = hasspecre.findall(text)

			for match in specsetmatches:
				specitemid = match.split('set_spec_item(')[1].split(',')[0]
				value = match.split('set_spec_item(')[1].split(',')[1].split(')')[0]
				itemkey = specitemid.zfill(3)
				if not itemkey in spec_dict:
					spec_dict[itemkey] = {}
					spec_dict[itemkey]['set'] = []
					spec_dict[itemkey]['get'] = []
				spec_dict[itemkey]['set'].append(SpecSet(zone, specitemid, value, fileName))

			for match in spechasmatches:
				specitemid = match.split('has_spec_item(')[1].split(')')[0]
				itemkey = specitemid.zfill(3)
				if not itemkey in spec_dict:
					spec_dict[itemkey] = {}
					spec_dict[itemkey]['set'] = []
					spec_dict[itemkey]['get'] = []
				spec_dict[itemkey]['get'].append(SpecCheck(zone, specitemid, fileName))

if __name__ == '__main__':
	main()
