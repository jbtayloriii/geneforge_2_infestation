#!usr/bin/python

'''
Parser used to find stat checks in the game.

Will return a dict with keys of zone number (or -1 for out of zone), and values of lists of named tuples:
'''

import re
import os
import argparse
from collections import namedtuple

statbasicre = re.compile('get_stat\([0-9]+\)')

def main():
	inputFolder = ''
	parser = argparse.ArgumentParser(description='Finds all the quest toggles in GF5 scripts')
	parser.add_argument('--input', help='input file folder')
	args = parser.parse_args()
	inputFolder = args.input
	if inputFolder:
		stat_dict = parseChecks(inputFolder)
		prettyPrintChecks(stat_dict)
	else:
		print('Missing input folder')

def prettyPrintChecks(stat_dict):
	for key in sorted(stat_dict):
		print('Zone: ' + key)
		print('Line Stat   Script')
		for tupleval in stat_dict[key]:
			print('{0:>4} {2:>4}   {1}   {3}'.format(*tupleval))
		print()

def parseChecks(inputDir):
	check_dict = {}

	for root, dirs, files in os.walk(inputDir):
		for filename in files:
			#could do without, change back
			if filename.startswith('z') and filename.endswith('.txt'):
				parseCheck(os.path.join(inputDir, filename), filename, check_dict)
	return check_dict

def parseCheck(filePath, filename, check_dict):
	CheckVals = namedtuple('CheckVals', ['line', 'filename', 'stat', 'text'])
	zone = -1
	zoneSearch = re.search('[0-9]+', filename)
	if not zoneSearch:
		return # don't search the template zones (they're empty anyways)
	zone = zoneSearch.group()

	# we're ignoring errors because some files are not utf-8 compliant
	with open(filePath, newline = '\r', errors = 'ignore') as f:		
		lines = f.readlines()
		lineCount = 0;
		for line in lines:
			lineCount = lineCount + 1
			text = line.strip()
			matches = statbasicre.findall(text)
			for match in matches:
				stat = match.split('get_stat(')[1].split(')')[0]
				zonekey = zone.zfill(3)
				if not zonekey in check_dict:
					check_dict[zonekey] = []
				check_dict[zonekey].append(CheckVals(lineCount, filename, stat, text))

if __name__ == '__main__':
	main()
