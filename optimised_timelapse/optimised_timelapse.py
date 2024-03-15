# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 16:02:42 2024

@author: bjans

The purpose of the script is to insert the TAKE_FRAME everylayer at an optimal point,
to get a better timelapse, without influencing the printing process.

You can choose a point on the print plate, where the picture should be taken.
The program then finds the gcode line, where the distance to this point is minimal.

The program also allows you to automatically enable or disable the timelapse,
if the model has a low height and you don't want to have a timelapse.


                    ***Limitations***
Not supported:
- Z hop retractions (only with search_for_comment set to False)
- non planar slicing (only with search_for_comment set to False)
- relative movements

Unsolved Problem:
- latencyof camera fotage leeds to "incorrect pictures", since position of the
toolhead and picture are not synchronous
"""
import re
import sys
import traceback

# X and Y coordinates where the picture should be taken
picture_point = (220,220)

# minimum amount of layers at which a timelapse should be taken
minimum_layers = 100

# command which takes the frame
picture_command = "TIMELAPSE_TAKE_FRAME"

run_in_slicer = True
search_for_comment = True # set to False to initiate new layer with Z movement

# to use this feature change the output path 
# open the gcode in a gcode viewer to see where the pictures will be taken
# i doesn't work well with G2/G3 commands (see README.md)
visualize_picture_coordinates = False
layer_height = 0.2 
path_output_picture =  r"C:\Users\bjans\Downloads\picture_visualisation.gcode"
# set to X or Y which coordinate should be compared if the distance of two points is equal
preffered_coordinate_direction = 'X'


prog_G = re.compile(r'^G[0-3].*X.*Y(?!.*Z)') # normal move without Z movement
prog_Z = re.compile(r'^G1.*Z')
prog_comment_layerchange = re.compile(r';AFTER_LAYER_CHANGE')

#tested
def read_coordinate(i: int)-> list:
    """
    Args: 
        i (int): line of gcode
    
    return:
        point (list): coordinates of point

    """   
    line = lines[i]
    point = []
    direction = ('X','Y')
    
    for i in direction:
        line_start = line.find(i) + 1
        
        # using or is slow!
        # instead use re.search?!
        for k in range(line_start, len(line)):
            if(line[k].isdigit() or line[k] == '.' or line[k] == '-'): # if it's a number
            # if(prog_digit.search(line[k]))
                line_end = k
            else:
                break # when a character comes stop here
                
        #print(line_start, line_end)
        coordinate = float(line[line_start:line_end+1])
        point.append(coordinate)
    
    return point

#tested
def distance(point: tuple[float])-> float:
    # calculates distance in between point and picture_point (pythagoras)
    return ((point[0]-picture_point[0])**2 + (point[1]-picture_point[1])**2)**(1/2)


# tested
def search_pattern(pattern)->list:
    match_list = []
    for i in range(len(lines)):
        line = lines[i]
        
        if(pattern.search(line)):
            match_list.append(i)
            
    return match_list

# Reading gcode
if run_in_slicer:
    path_input = sys.argv[1] # the path of the gcode given by the slicer
    path_output = path_input # same input and output
    print('Program', sys.argv[0], 'initiated') # prints out path to program
    
else:# if not running in slicer
    # insert the path for the input and output file here
    path_input = r"C:\Users\bjans\Downloads\Cone_PETG_11m57s.gcode"
    # you can name the output file however you want but don't forget to name it .gcode
    # if input and output path are the same the old file will be overwritten
    path_output =  r"C:\Users\bjans\Downloads\picture_test_result.gcode"

with open(path_input, "r") as input_file:
    lines = input_file.readlines() # saves the gcode as an list
    
    
# main
# generate lists with lines of gcode
if search_for_comment:
    layer_change = search_pattern(prog_comment_layerchange)  
else:
    layer_change = search_pattern(prog_Z)    
    
move_list = search_pattern(prog_G)
    
layer_i = []
start_move = 0 
picture_gcode = [] 
n = 0.2

# only take timelapse if more or equal layers 
if len(layer_change) >= minimum_layers:
    try:  
        for layer in range(len(layer_change)-1):
            # define start and end of layer
            start = layer_change[layer]
            end = layer_change[layer+1]
                
            # write list with moves within the layer
            for i in move_list[start_move:]:
                if i <= end:
                    layer_i.append(i)
                else:
                    #start_move = i
                    break
              
            # define first coordinate on layer as refference starting point    
            min_distance = distance(read_coordinate(layer_i[0]))
            index_min_d = layer_i[0]
            
            # find index with minimum distance to point
            for k in range(1,len(layer_i)):
                c = distance(read_coordinate(layer_i[k]))
                
                if c < min_distance:
                    min_distance = c
                    
                    index_min_d = layer_i[k]
                    
                # define logic what to do if equal distance
                # the logic itself isn't impotant it just needs to be a constant rule
                # you can invert the logic by putting a not after the if at the lines where the two coordinates get compared
                elif c == min_distance:
                    if preffered_coordinate_direction == 'X':
                        if read_coordinate(layer_i[k])[0] >= read_coordinate(index_min_d)[0]:
                            min_distance = c
                            
                            index_min_d = layer_i[k]
                    else:
                        if read_coordinate(layer_i[k])[1] >= read_coordinate(index_min_d)[1]:
                            min_distance = c
                            
                            index_min_d = layer_i[k]
                    
            #print(lines[index_min_d])
            # insert the take picture command at the line with the minimum distance
            lines[index_min_d] +=  picture_command + '\n'
            
            if visualize_picture_coordinates:
                picture_gcode.append(lines[index_min_d])
                picture_gcode.append('G1 Z'+ str(round(n,3))+ '\n')
                n += layer_height
                
            start_move += len(layer_i)
            # delete list entries
            layer_i = []
        
    except Exception as error:
        # if a bug occures in the function it will tell you the error message at the end of the gcode
        # and inside the terminal
        
        error_message = str(error) + '\n'
        
        print('Error message:' + str(error_message))    
        traceback.print_exc()
        if run_in_slicer:
            print('Press enter to close window')
            input()
            
    # saves a list as a file
    with open(path_output, "w") as output:
        for t in range(0,len(lines)):        
            output.write("%s"  % lines[t])           
    output.close()    
        
  
    if visualize_picture_coordinates:
        with open(path_output_picture, "w") as output:
            for t in picture_gcode:        
                output.write("%s"  % t)           
        output.close()    
        
        