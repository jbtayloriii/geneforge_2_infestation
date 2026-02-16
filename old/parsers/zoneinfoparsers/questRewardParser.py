#!usr/bin/python

'''
Parser used to get the item rewards from all the relevant geneforge 5 scripts.
'''

import re
import os
import argparse
from collections import namedtuple

import item_creature_parser

rewardre = re.compile('reward_give\(\d+\)')

creature_itemfile = '../../gf5data/gf5itemschars.txt'

def main():
	inputFolder = ''
	parser = argparse.ArgumentParser(description='Finds all the item rewards in GF5 scripts')
	parser.add_argument('-i', '--input', help='input file folder')
	args = parser.parse_args()
	inputFolder = args.input
	if inputFolder:
		reward_dict = parseRewards(inputFolder)
		prettyPrintRewards(reward_dict)
	else:
		print('Missing input folder')

def prettyPrintRewards(reward_dict):
	for key in sorted(reward_dict):
		print('Item ' + key + ':')
		for tupleval in reward_dict[key]:
			print(tupleval)
			#print('{0:>4} {2:>6} {1}'.format(*tupleval))
		print()

def parseRewards(inputDir):
	reward_dict = {}
	iteminfo = item_creature_parser.parseItems(creature_itemfile)
	print 

	for root, dirs, files in os.walk(inputDir):
		for filename in files:
			#test, change back
			if filename.startswith('z') and filename.endswith('.txt'):
				parseReward(os.path.join(inputDir, filename), filename, reward_dict, iteminfo)
	return reward_dict

def parseReward(filePath, fileName, reward_dict, iteminfo):
	RewardItem = namedtuple('RewardItem', ['zone', 'script', 'itemid', 'itemname'])
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
			matches = rewardre.findall(text)
			for match in matches:
				itemid = match.split('reward_give(')[1].split(',')[0].split(')')[0]
				itemname = ''
				if not str(itemid) in iteminfo:
					print(str(itemid) + ' is not in the item info dict')
				else:
					itemname = iteminfo[str(itemid)]['it_name']

				itemkey = itemid.zfill(3)
				if not itemkey in reward_dict:
					reward_dict[itemkey] = []
				reward_dict[itemkey].append(RewardItem(zone, fileName, itemid, itemname))
				
	#print(quest_dict)

if __name__ == '__main__':
	main()
