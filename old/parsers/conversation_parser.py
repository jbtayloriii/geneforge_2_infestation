import re

node_pattern = re.compile(r'begintalknode (?P<node_id>\d+);')


def parse_file(filepath):
	print('Parsing conversation file')
	with open(filepath, 'r') as f:
		lines = f.readlines()

		current_id = -1
		current_template = {}
		for line in lines:
			#Remove trailing comments
			line = line.split('\/\/')[0]
			match = node_pattern.search(line)
			if not match is None:
				current_id = match.group('node_id')
				current_template = {}
			elif re.match(
