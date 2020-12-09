#!/usr/bin/env python
import re
import random

# original stl: https://www.thingiverse.com/thing:966908
# input gcode: PrusaSlicer export
# view output gcode: https://ncviewer.com/

regex_G1_X = re.compile(r"^G1 X(\d+\.\d+).*$", re.IGNORECASE)

layer_start = 10
layer_stop = 40

inputLines = [line.strip() for line in tuple(open('sample.gcode', 'r'))]
layer_num = 0
latest_shift_layer_num = 0

output = open("output.gcode", "w")

for line in inputLines:
    if(line == ";BEFORE_LAYER_CHANGE"):
        layer_num += 1
        current_layer_shift = random.random() * layer_num * 0.3

    if layer_num > layer_start:
        if layer_num < layer_stop:
                re_match = re.search(regex_G1_X, line)
                if(re_match and len(re_match.group(1)) > 0):
                        x_value_origin = float(re_match.group(1))
                        x_value_modified = x_value_origin + current_layer_shift
                        line = line.replace("%3.3f" % (x_value_origin), "%3.3f" % (x_value_modified))
                        latest_shift = current_layer_shift
        else:
                re_match = re.search(regex_G1_X, line)
                if(re_match and len(re_match.group(1)) > 0):
                        x_value_origin = float(re_match.group(1))
                        x_value_modified = x_value_origin + latest_shift_layer_num
                        line = line.replace(str(x_value_origin), str(x_value_modified))

    output.write('\n%s' % line)
