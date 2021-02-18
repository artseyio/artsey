#!/usr/bin/env python

# -*- coding: utf-8 -*-

#####
# Dependencies (pip install)
#   - pyyaml
#####

#####
# Imports
#####
import argparse
import pprint
import sys
import yaml
from copy import deepcopy

#####
# Globals
#####
key_active = '⚫'
key_inactive = '⚪'
combo_empty = [
    [key_inactive, key_inactive, key_inactive, key_inactive], 
    [key_inactive, key_inactive, key_inactive, key_inactive], 
]

#####
# CLI Related
#####
parser = argparse.ArgumentParser(description='Parse ARTSEY.IO yaml into reference materials')
parser.add_argument('--exclude-left', action='store_true',
                    help='Exclude left handed information')
parser.add_argument('--exclude-right', action='store_true',
                    help='Exclude rigth handed information')
parser.add_argument('--input-file', action='store', default='artsey.yaml',
                    help='The ARTSEY.IO yaml definition to use for processing')
parser.add_argument('--exclude-cheat-sheet-markdown', action='store_true',
                    help='Exclude (skip) cheat sheet markdown processing')
parser.add_argument('--exclude-detailed-markdown', action='store_true',
                    help='Exclude (skip) detailed markdown processing')
parser.add_argument('--cheat-sheet-markdown-file', action='store', default='artsey_cheat.md',
                    help='The filename for writing the cheat sheat markdown')
parser.add_argument('--detailed-markdown-file', action='store', default='artsey.md',
                    help='The filename for writing the detailed markdown')
parser.add_argument('--debug', action='store_true',
                    help='Print debugging information')
args = parser.parse_args()

if args.exclude_left and args.exclude_right:
    print('ERROR: You *MUST* not exclude both left and right')
    sys.exit(1)

if args.exclude_cheat_sheet_markdown and args.exclude_detailed_markdown:
    print('ERROR: You *MUST* not exclude all output options')
    sys.exit(1)

#####
# Load ARTSEY yaml definition
#####
stream = open(args.input_file, 'r')
data = yaml.full_load(stream)

#####
# Debug print to ensure data is correct
#####
if args.debug:
    pprint.pprint(data)

#####
# Convert combo to markdown
#####
def generate_combo_markdown(code):
    to_return = b''
    left = deepcopy(combo_empty)
    right = deepcopy(combo_empty)
    if not args.exclude_left:
        for key in code['combo']['left']:
            x = key['x']
            y = key['y']
            left[y][x] = key_active
    if not args.exclude_right:
        for key in code['combo']['right']:
            x = key['x']
            y = key['y']
            right[y][x] = key_active

    to_return += b'| '
    to_return += str(code['description']).replace('_', ' ').encode()
    to_return += b' | '
    to_return += code['layer']['layer'].replace('_', ' ').encode()
    to_return += b' | '
    if not args.exclude_right:
        if not args.exclude_left:
            to_return += b'**Right**<br>'
        for (y, row) in enumerate(right):
            for (x,column) in enumerate(row):
                to_return += column.encode()
            to_return += b'<br>'
    if not args.exclude_left and not args.exclude_right:
        to_return += b'<br>'
    if not args.exclude_left:
        if not args.exclude_right:
            to_return += b'**Left**<br>'
        for (y, row) in enumerate(left):
            for (x,column) in enumerate(row):
                to_return += column.encode()
            to_return += b'<br>'
    to_return += b' |'
    to_return += b'\n'


    return to_return

#####
# Process cheat sheet markdown output and write to file
#####
if not args.exclude_cheat_sheet_markdown:
    with open(args.cheat_sheet_markdown_file, 'wb') as f:
        f.write(b'# ARTSEY.IO Cheat Sheet\n')
        f.write(b'\n')
        if args.exclude_left:
            f.write(b'# RIGHT HANDED LAYOUT\n')
            f.write(b'\n')
        if args.exclude_right:
            f.write(b'# LEFT HANDED LAYOUT\n')
            f.write(b'\n')
        f.write(b'## Version: ')
        f.write(data['version'].encode())
        f.write(b'\n')
        f.write(b'\n')
        f.write(b'## Changelog\n')
        f.write(b'\n')
        for change in data['changelog']:
            f.write(b'- ')
            f.write(change.encode())
            f.write(b'\n')
        f.write(b'\n')
        layer_data = {}
        for layer in data['layers']:
            layer_data[layer['layer']] = []
        for code in data['keymap']:
            layer_name = code['layer']['layer']
            layer_data[layer_name].append(code)
        for layer in layer_data.keys():
            f.write(b'## Layer: ')
            f.write(layer.replace('_', ' ').encode())
            f.write(b'\n')
            f.write(b'\n')
            single_key_left = deepcopy(combo_empty)
            single_key_right = deepcopy(combo_empty)
            single_key_left_seen = False
            single_key_right_seen = False
            multi_key = []
            for combo in layer_data[layer]:
                if not args.exclude_right:
                    if len(combo['combo']['right']) > 1:
                        multi_key.append(generate_combo_markdown(combo))
                    else:
                        single_key_right_seen = True
                        single_key_right[combo['combo']['right'][0]['y']][combo['combo']['right'][0]['x']] = combo['description']
                if not args.exclude_left:
                    if len(combo['combo']['left']) > 1:
                        multi_key.append(generate_combo_markdown(combo))
                    else:
                        single_key_left_seen = True
                        single_key_left[combo['combo']['left'][0]['y']][combo['combo']['left'][0]['x']] = combo['description']
            
            f.write(b'### Keys\n')
            f.write(b'\n')
            if not args.exclude_right:
                if single_key_right_seen:
                    if not args.exclude_left:
                        f.write(b'#### Right\n')
                        f.write(b'\n')
                    f.write(b'| C1 | C2 | C3 | C4 |\n')
                    f.write(b'| -- | -- | -- | -- |\n')
                    for (y, row) in enumerate(single_key_right):
                        for (x,column) in enumerate(row):
                            f.write(b' ')
                            f.write(str(column).replace('_', ' ').encode())
                            f.write(b' |')
                        f.write(b'\n')
                    f.write(b'\n')
            if not args.exclude_left:
                if single_key_left_seen:
                    if not args.exclude_right:
                        f.write(b'#### Left\n')
                        f.write(b'\n')
                    f.write(b'| C1 | C2 | C3 | C4 |\n')
                    f.write(b'| -- | -- | -- | -- |\n')
                    for (y, row) in enumerate(single_key_left):
                        for (x,column) in enumerate(row):
                            f.write(b' ')
                            f.write(str(column).replace('_', ' ').encode())
                            f.write(b' |')
                        f.write(b'\n')
                    f.write(b'\n')

            multi_key = set(multi_key)
            if len(multi_key) > 0:
                f.write(b'### Combos\n')
                f.write(b'\n')
                f.write(b'| Character | Layer | Combo |\n')
                f.write(b'| --------- | ----- | ----- |\n')
                for combo in multi_key:
                    f.write(combo)


#####
# Process detailed markdown output and write to file
#####
if not args.exclude_detailed_markdown:
    with open(args.detailed_markdown_file, 'wb') as f:
        f.write(b'# ARTSEY.IO Detailed Layout\n')
        f.write(b'\n')
        if args.exclude_left:
            f.write(b'# RIGHT HANDED LAYOUT\n')
            f.write(b'\n')
        if args.exclude_right:
            f.write(b'# LEFT HANDED LAYOUT\n')
            f.write(b'\n')
        f.write(b'## Version: ')
        f.write(data['version'].encode())
        f.write(b'\n')
        f.write(b'\n')
        f.write(b'## Changelog\n')
        f.write(b'\n')
        for change in data['changelog']:
            f.write(b'- ')
            f.write(change.encode())
            f.write(b'\n')
        f.write(b'\n')
        f.write(b'## Layers\n')
        f.write(b'\n')
        f.write(b'| Index | Layer |\n')
        f.write(b'| ----- | ----- |\n')
        layers = []
        for layer in data['layers']:
            f.write(b'| ')
            f.write(layer['layer'].replace('_', ' ').encode())
            f.write(b' | ')
            f.write(str(layer['index']).encode())
            f.write(b' |\n')
        f.write(b'\n')
        f.write(b'## Codes\n')
        f.write(b'\n')
        f.write(b'| Code | Layer | Combo |\n')
        f.write(b'| ---- | ----- | ----- |\n')
        for code in data['keymap']:
            f.write(generate_combo_markdown(code))
