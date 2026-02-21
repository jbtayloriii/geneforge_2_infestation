import argparse
import json
import os
import pathlib
import pprint
import re

from src.objects import talk_node

'''Dialogue parser tester for G5. Used to determine the different parsable pieces in GF5. '''

_NODE_BEGIN_PATTERN = re.compile("begintalknode ?(?P<node_id>\d*);")

_TAG_PATTERN = re.compile("tag = (?P<tag_id>\d+);")
_STATE_PATTERN = re.compile("state = (?P<state_id>-?\d+);")
_NEXTSTATE_PATTERN = re.compile("nextstate = (?P<nextstate_id>-?\d+);")
_CONDITION_PATTERN = re.compile("condition = (?P<condition_text>[^;]+);")

textre = re.compile('text\d = \"(?P<text>.+)\";')
conditionre = re.compile('condition = (?P<condition>.+);')
actionre = re.compile('action = (?P<action>.+);')


actions = []
conditions = []

GENEFORGE_FILE_DIR = os.path.join(os.path.expanduser('~'), '.wine/drive_c/Program Files (x86)/Spiderweb Software/Geneforge 5/Geneforge 5 Files')

SCRIPTS_DIR = os.path.join(GENEFORGE_FILE_DIR, "Scripts")

def parse_dialog(dialog_filepath) -> list[talk_node.TalkNode]:
    print(f"Parsing dialog for {dialog_filepath}")
    with open(dialog_filepath, "r") as f:
        contents = f.read()
    
    # Split text contents on talk node begin declarations, and throw away contents before first node
    node_contents_split = _NODE_BEGIN_PATTERN.split(contents)[1:]
    if len(node_contents_split) % 2 != 0:
        raise ValueError(f"Invalid dialog parsing for {dialog_filepath}, got odd node ID/contents length")
    
    talk_nodes = []

    # TODO: parse entire file, not just first couple of nodes
    for x in range(len(node_contents_split)//2)[:2]:
        next_node = parse_node(node_id=node_contents_split[x * 2], node_contents=node_contents_split[x * 2 + 1])
    return talk_nodes

def parse_node(node_id, node_contents):
    print(f"node_id: {node_id}")
    # Remove whitespace padding and inline comments
    updated_lines = [l.strip().split("\/\/")[0] for l in node_contents.splitlines()]

    # Remove empty lines and join back together
    updated_contents = "\n".join([l for l in updated_lines if l])

    tag_match = _TAG_PATTERN.search(updated_contents)
    tag = tag_match.group("tag_id") if tag_match else None

    state_match = _STATE_PATTERN.search(updated_contents)
    state = state_match.group("state_id") if state_match else None

    nextstate_match = _NEXTSTATE_PATTERN.search(updated_contents)
    nextstate = nextstate_match.group("nextstate_id") if nextstate_match else None

    condition_match = _CONDITION_PATTERN.search(updated_contents)
    condition_text = condition_match.group("condition_text") if condition_match else None
    print(f"condition text: {condition_text}")

    # TODO: Continue parsing the node

    print()
    

def main():
    with open("parsers/geneforge_filepaths.json", "r") as f:
        filepath_info = json.loads(f.read())
        # print(filepath_info)
    file_source = pathlib.Path(filepath_info["geneforge_2_remake"]["root"]["mac2"])
    # scripts_dir = file_source / "Scripts"

    print(file_source)
    # print(scripts_dir)
    for root, dirs, files in os.walk(file_source):
        print("hi")
        for filename in files:
            print(filename)
        return

    # for root, dirs, files in os.walk(SCRIPTS_DIR):
    # 	for filename in files:
    # 		if filename.startswith('z') and filename[1].isdigit() and filename.endswith('dlg.txt'):
    # 			parseFile(filename)

    # printLists()
            

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
