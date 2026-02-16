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

questre = re.compile('toggle_quest\(\d+,\d+\)')

def main():
	inputFolder = ''
	parser = argparse.ArgumentParser(description='Finds all the quest toggles in GF5 scripts')
	parser.add_argument('-i', '--input', help='input file folder')
	args = parser.parse_args()
	inputFolder = args.input
	if inputFolder:
		quest_dict = parseQuests(inputFolder)
		#print(quest_dict)
		prettyPrintQuests(quest_dict)
	else:
		print('Missing input folder')

def prettyPrintQuests(quest_dict):
	for key in sorted(quest_dict):
		print('Quest ' + key)
		print('Zone  Value Script')
		for tupleval in quest_dict[key]:
			print('{0:>4} {2:>6} {1}'.format(*tupleval))
		print()

def parseQuests(inputDir):
	quest_dict = {}

	for root, dirs, files in os.walk(inputDir):
		for filename in files:
			#test, change back
			if filename.startswith('z') and filename.endswith('.txt'):
				parseQuest(os.path.join(inputDir, filename), filename, quest_dict)
	return quest_dict

def parseQuest(filePath, fileName, quest_dict):
	QuestToggle = namedtuple('QuestToggle', ['zone', 'script', 'value'])
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
			matches = questre.findall(text)
			for match in matches:
				quest = match.split('toggle_quest(')[1].split(',')[0]
				value = match.split('toggle_quest(')[1].split(',')[1].split(')')[0]
				questkey = quest.zfill(3)
				if not questkey in quest_dict:
					quest_dict[questkey] = []
				quest_dict[questkey].append(QuestToggle(zone, fileName, value))
	#print(quest_dict)

if __name__ == '__main__':
	main()
