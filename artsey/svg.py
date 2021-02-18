#!/usr/bin/env python

# -*- coding: utf-8 -*-

#####
# Dependencies (pip install)
#   - pycairo
#   - pyyaml
#####

#####
# Imports
#####
import argparse
import cairo
import math
import pprint
import sys
import yaml
from copy import deepcopy

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
parser.add_argument('--debug', action='store_true',
                    help='Print debugging information')
args = parser.parse_args()

if not args.exclude_left and not args.exclude_right:
    print('ERROR: You *MUST* exclude left or right')
    sys.exit(1)

#####
# Load ARTSEY yaml definition
#####
stream = open(args.input_file, 'r')
data = yaml.full_load(stream)

#####
# Constants
#####
# Base image size
width_canvas = 3276
height_canvas = 4096
# Key Icon (standard)
key_width = 200
key_height = key_width
key_padding = key_width * 0.05
# Key Icon (small)
key_small_scale = 0.5
key_width_small = key_width * key_small_scale
key_height_small = key_width_small
key_padding_small = key_width_small * 0.05
# Highlighted key color
key_highlight_color_r = 0
key_highlight_color_g = 0.71
key_highlight_color_b = 0.81
key_highlight_color_a = 1.0
# Empty key color
key_empty_color_r = 1.0
key_empty_color_g = 1.0
key_empty_color_b = 1.0
key_empty_color_a = 1.0
# Pressed key color
key_pressed_color_r = 0.0
key_pressed_color_g = 0.0
key_pressed_color_b = 0.0
key_pressed_color_a = 1.0
combo_empty = [
    [False, False, False, False],
    [False, False, False, False],
]

#####
# Draw an arrow pointed right
#####
def arrow_right(ctx, x, y, width, height, a, b, rotation):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rotation*(math.pi/180))
    ctx.move_to(0, b)
    ctx.line_to(0, height - b)
    ctx.line_to(a, height - b)
    ctx.line_to(a, height)
    ctx.line_to(width, height/2)
    ctx.line_to(a, 0)
    ctx.line_to(a, b)
    ctx.restore()
    ctx.close_path()

#####
# Draw a standard, highlighted key rectangle
#####
def key_standard_highlight(ctx, x, y, legend):
    ctx.rectangle(x, y, key_width, key_height)
    ctx.set_source_rgba(key_highlight_color_r, key_highlight_color_g, key_highlight_color_b, key_highlight_color_a)
    ctx.fill_preserve()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.set_line_width(key_padding)
    ctx.stroke()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.select_font_face('DejaVuSansMono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(96)
    ctx.move_to(x + key_width / 2, y + key_height / 2)
    ctx.show_text(str(legend))

#####
# Draw a standard, empty key rectangle
#####
def key_standard_empty(ctx, x, y, legend):
    ctx.rectangle(x, y, key_width, key_height)
    ctx.set_source_rgba(key_empty_color_r, key_empty_color_g, key_empty_color_b, key_empty_color_a)
    ctx.fill_preserve()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.set_line_width(key_padding)
    ctx.stroke()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.select_font_face('DejaVuSansMono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(96)
    ctx.move_to(x + key_width / 2, y + key_height / 2)
    ctx.show_text(str(legend))

#####
# Draw a standard, pressed key rectangle
#####
def key_standard_pressed(ctx, x, y, legend):
    ctx.rectangle(x, y, key_width, key_height)
    ctx.set_source_rgba(key_pressed_color_r, key_pressed_color_g, key_pressed_color_b, key_pressed_color_a)
    ctx.fill_preserve()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.set_line_width(key_padding)
    ctx.stroke()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.select_font_face('DejaVuSansMono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(96)
    ctx.move_to(x + key_width / 2, y + key_height / 2)
    ctx.show_text(str(legend))

#####
# Draw a small, highlighted key rectangle
#####
def key_small_highlight(ctx, x, y, legend):
    ctx.rectangle(x, y, key_width_small, key_height_small)
    ctx.set_source_rgba(key_highlight_color_r, key_highlight_color_g, key_highlight_color_b, key_highlight_color_a)
    ctx.fill_preserve()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.set_line_width(key_padding_small)
    ctx.stroke()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.select_font_face('DejaVuSansMono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(96)
    ctx.move_to(x + key_width_small / 2, y + key_height_small / 2)
    ctx.show_text(str(legend))

#####
# Draw a small, empty key rectangle
#####
def key_small_empty(ctx, x, y, legend):
    ctx.rectangle(x, y, key_width_small, key_height_small)
    ctx.set_source_rgba(key_empty_color_r, key_empty_color_g, key_empty_color_b, key_empty_color_a)
    ctx.fill_preserve()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.set_line_width(key_padding_small)
    ctx.stroke()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.select_font_face('DejaVuSansMono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(96)
    ctx.move_to(x + key_width_small / 2, y + key_height_small / 2)
    ctx.show_text(str(legend))

#####
# Draw a small, pressed key rectangle
#####
def key_small_pressed(ctx, x, y, legend):
    ctx.rectangle(x, y, key_width_small, key_height_small)
    ctx.set_source_rgba(key_pressed_color_r, key_pressed_color_g, key_pressed_color_b, key_pressed_color_a)
    ctx.fill_preserve()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.set_line_width(key_padding_small)
    ctx.stroke()
    ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
    ctx.select_font_face('DejaVuSansMono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(96)
    ctx.move_to(x + key_width_small / 2, y + key_height_small / 2)
    ctx.show_text(str(legend))

#####
# Image Generation
#####

# Setup surface for drawing
surface = cairo.SVGSurface('test.svg', width_canvas, height_canvas)
ctx = cairo.Context(surface)

# Set background of image to silver
ctx.rectangle(0, 0, width_canvas, height_canvas)
ctx.set_source_rgba(0.75, 0.75, 0.75, 1.0)
ctx.fill()
ctx.stroke()

# Set title of document
ctx.set_source_rgba(0, 0, 0, 1.0)
ctx.select_font_face('DejaVuSansMono', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(96)
ctx.move_to(100, 150)
ctx.show_text('ARTSEY.IO')

# Set version info
ctx.move_to(100, 250)
ctx.set_font_size(72)
ctx.show_text('Version: ' + data['version'])

# Set handed info (left/right)
ctx.move_to(100, 350)
ctx.set_font_size(72)
if args.exclude_right:
    ctx.show_text('LEFT Handed')
if args.exclude_left:
    ctx.show_text('RIGHT Handed')


layer_data = {}
for layer in data['layers']:
    layer_data[layer['layer']] = []
for code in data['keymap']:
    layer_name = code['layer']['layer']
    layer_data[layer_name].append(code)
for layer in layer_data.keys():
    single_key_left = deepcopy(combo_empty)
    single_key_right = deepcopy(combo_empty)
    single_key_left_seen = False
    single_key_right_seen = False
    multi_key = []
    for combo in layer_data[layer]:
        if not args.exclude_right:
            if len(combo['combo']['right']) > 1:
                multi_key.append(combo)
            else:
                single_key_right_seen = True
                single_key_right[combo['combo']['right'][0]['y']][combo['combo']['right'][0]['x']] = combo['description']
        if not args.exclude_left:
            if len(combo['combo']['left']) > 1:
                multi_key.append(combo)
            else:
                single_key_left_seen = True
                single_key_left[combo['combo']['left'][0]['y']][combo['combo']['left'][0]['x']] = combo['description']

pprint.pprint(layer_data['global'])

ctx.set_font_size(64)
x_offset = 100
y_offset = 500
ctx.move_to(x_offset, y_offset)
ctx.show_text('global')
x_offset = 100
y_offset += 100
ctx.move_to(x_offset, y_offset)
for code in layer_data['global']:
    print(code)
    ctx.move_to(x_offset, y_offset)
    ctx.set_source_rgba(0, 0, 0, 1.0)
    ctx.set_font_size(64)
    ctx.show_text(code['description'])
    y_offset += 50
    key_presses = deepcopy(combo_empty)
    if not args.exclude_left:
        for key in code['combo']['left']:
            x = key['x']
            y = key['y']
            key_presses[y][x] = True
    if not args.exclude_right:
        for key in code['combo']['right']:
            x = key['x']
            y = key['y']
            key_presses[y][x] = True

    for (y, row) in enumerate(key_presses):
        for (x,column) in enumerate(row):
            if column:
                key_small_pressed(ctx, x_offset, y_offset, '')
            else:
                key_small_empty(ctx, x_offset, y_offset, '')
            x_offset += key_width_small
        x_offset = 100
        y_offset += key_height_small
    
    y_offset += 75

#####
# Write image to filesystem
#####
surface.write_to_png('test.png')
