#!usr/bin/python

import argparse
import os
import re

'''Dialogue parser tester for G5. Used to determine the different parsable pieces in GF5. '''

nodebeginre = re.compile('begintalknode (?P<nodeid>\d+);')
textre = re.compile('text\d = \"(?P<text>.+)\";')
conditionre = re.compile('condition = (?P<condition>.+);')
actionre = re.compile('action = (?P<action>.+);')


actions = []
conditions = []

GENEFORGE_FILE_DIR = os.path.join(os.path.expanduser('~'), '.wine/drive_c/Program Files (x86)/Spiderweb Software/Geneforge 5/Geneforge 5 Files')

SCRIPTS_DIR = os.path.join(GENEFORGE_FILE_DIR, "Scripts")

def main():
	for root, dirs, files in os.walk(SCRIPTS_DIR):
		for filename in files:
			if filename.startswith('z') and filename[1].isdigit() and filename.endswith('dlg.txt'):
				parseFile(filename)

	printLists()
			

def parseFile(filename):
	with open(os.path.join(SCRIPTS_DIR, filename), newline = '\r', errors = 'ignore') as f:
		nodes = {}

		lines = f.readlines()

		nodeId = -1
		nodeobj = {}

		print(len(lines))

		for line in lines:
			#strip whitespace and remove comments
			text = line.strip().split('\/\/')[0]
			if len(text) == 0:
				continue

			#new node
			match = nodebeginre.search(text)
			if match:
				
				if int(nodeId) > -1:
					nodes[nodeId] = nodeobj
				nodeId = match.group('nodeid')
				nodeobj = {}
				print('node id:' + nodeId + ", zone: " + filename)

			match = actionre.search(text)
			if match:
				action = match.group('action').split(' ')[0]
				if not action in actions:
					actions.append(action)

			match = conditionre.search(text)
			if match:
				condition = match.group('condition').strip()
				if not condition in conditions:
					conditions.append(condition)

def printLists():
	print('actions:')
	for action in actions:
		print(action)

	print()

	print('conditions')
	for condition in conditions:
		print(condition)
	
		

if __name__ == '__main__':
	main()
