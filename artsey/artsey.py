#!/usr/bin/env python

# -*- coding: utf-8 -*-

#####
# Dependencies (pip install)
#   - pyyaml
#####

#####
# Imports
#####
import markdown
import pprint
import yaml
from copy import deepcopy

#####
# Load ARTSEY yaml definition
#####
stream = open('artsey.yaml', 'r')
data = yaml.load(stream)

# Debug print to ensure data is correct
pprint.pprint(data)

with open('artsey.md', 'wb') as f:
    f.write(b'# ARTSEY.IO Cheat Sheet\n')
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
        f.write(layer['layer'].encode())
        f.write(b' | ')
        f.write(str(layer['index']).encode())
        f.write(b' |\n')
    f.write(b'\n')

    f.write(b'| Character | Layer | Combo |\n')
    f.write(b'| --------- | ----- | ----- |\n')

    key_active = '⚫'
    key_inactive = '⚪'
    combo_empty = [
        [key_inactive, key_inactive, key_inactive, key_inactive], 
        [key_inactive, key_inactive, key_inactive, key_inactive], 
    ]

    for code in data['keymap']:
        left = deepcopy(combo_empty)
        right = deepcopy(combo_empty)
        f.write(b'| ')
        f.write(str(code['description']).encode())
        f.write(b' | ')
        f.write(code['layer']['layer'].encode())
        f.write(b' | ')
        for key in code['combo']['left']:
            x = key['x']
            y = key['y']
            left[y][x] = key_active
        for key in code['combo']['right']:
            x = key['x']
            y = key['y']
            right[y][x] = key_active
        f.write(b'**Right**<br>')
        for (y, row) in enumerate(right):
            for (x,column) in enumerate(row):
                f.write(column.encode())
            f.write(b'<br>')
        f.write(b'<br>')
        f.write(b'**Left**<br>')
        for (y, row) in enumerate(left):
            for (x,column) in enumerate(row):
                f.write(column.encode())
            f.write(b'<br>')
        f.write(b' |')
        f.write(b'\n')
