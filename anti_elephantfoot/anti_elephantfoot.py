# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 21:19:24 2024

@author: Benedikt Jansson

Prevent elephant foot by reducing flow by a given factor at the outer perimeter at the first layer.
This only works with relative extrusion.
"""

import re
import sys

# user variables
# the comments work within prusa slicer
# you probably need to adapt them to other slicers
flow_factor = 0.9 # factor which gets multiplyed with outer perimiter
run_in_slicer = True
outer_perimiter_comment = ";TYPE:External perimeter" # comment which indicates the outer perimiter
type_comment = ";TYPE:" #comment which indicates a certain feature type (followed by the actual type)
layerchange_comment = ";LAYER_CHANGE" # comment which indicates a layerchange (in prusa slicer is a layer change before the start of the first layer)

# run script manually from IDE by giving paths to file
in_path = r"C:\Users\bjans\Downloads\final_test.gcode"
out_path = r"C:\Users\bjans\Downloads\anti_elephatntfoot.gcode"
# end of user variables

# compile keywords to search inside of the gcode
prog_outer_perimiter = re.compile(r"^"+ outer_perimiter_comment)
prog_type = re.compile(r"^"+ type_comment)
prog_layerchange = re.compile(r"^"+ layerchange_comment)

prog_E = re.compile(r'^G[1-3].*E')

# passed tests                
def read_position(direction: str, line: str)-> list:
    """
    Args: 
        direction (str): find value after key word
        line (str): line of gcode
    
    return:
        info (list): list with line start , line end and value

    """   
    
    line_start = line.find(direction) + 1
    #print(line)
    # using or is slow!
    # instead use re.search?!
    for k in range(line_start, len(line)):
        if(line[k].isdigit() or line[k] == '.' or line[k] == '-'): # if it's a number
        # if(prog_digit.search(line[k]))
            line_end = k
        else:
            #line_end = line_start+1
            break # when a character comes stop here
            
    #print(line_start, line_end)
    value = float(line[line_start:line_end+1])
    info = [line_start, line_end, value]
    
    return info
    
               
def offset(direction: str, factor: float, i: int)-> None: # multiply extrusion with factor
    """
    Args: 
        direction (str): which value to change
        factor (float): gets multiplyed with the current value
        i (int): line of gcode (to write)
    
    return:
        none

    """   
    global retr_d, search_retr_d, previous_neg_number, comp
    line = lines[i]
    
    L_value = read_position(direction, line)
    
    # iterate one time so i can use continue
    for _ in range(1):
        # logic stops the program from scaling retractions within the outer perimiter
        if L_value[2] < 0 and search_retr_d:
            retr_d += abs(L_value[2])
            previous_neg_number = True
            continue
            
        elif L_value[2] < 0:
            # do nothing (retraction without scaling)
            previous_neg_number = True
            continue
        
        elif previous_neg_number:
            # retr finished so distance has been found
            search_retr_d = False
            # positive number
            if L_value[2] + comp < retr_d:
                # compensation of retraction (not complete)
                comp += L_value[2]
                continue
            
            if L_value[2] + comp >= retr_d:
                # compensation complete resetting variables
                previous_neg_number = False
                comp = 0
                continue
            
        value = L_value[2] * factor 
        # write new position value
        line_start = L_value[0]
        line_end = L_value[1]
        
                
        # writing line and inserting the new value
        line = line[0:line_start]+ str(round(value,5)) + line[line_end+1:] #+''
            
        # writing to gcode list
        lines[i] = line 
    
# read path if run in slicer    
if run_in_slicer:
    in_path = sys.argv[1]
    out_path = in_path
    
    
# open file and load it as a list of strings    
with open(in_path, "r") as input_path:
    lines = input_path.readlines()

# defining start value of variables
found_start = False
i = 0
layer = 0
retr_d = 0
comp = 0
search_retr_d = True
previous_neg_number = False

for line in lines:
    # if outer perimiter found
    if re.match(prog_outer_perimiter, line):
        found_start = True
        i += 1
        continue
        
    if found_start:
        if re.search(prog_E, line):
            offset('E', flow_factor, i)
            
        elif re.match(prog_type, line):
            # different feature started
            found_start = False
            
    if re.match(prog_layerchange, line):
        # there is one layer change at the bigginning of the first layer
        layer += 1
        if layer == 2:
            # found end of first layer program finished
            break
    # iterator of loop (count line in lines)        
    i += 1
    
# write final file
with open(out_path, 'w') as output:
    for line in lines:
        output.write("%s"  % line)    
output.close()
