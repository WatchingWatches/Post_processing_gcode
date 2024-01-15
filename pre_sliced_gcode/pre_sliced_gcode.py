# -*- coding: utf-8 -*-
# user/bin/python3
"""
Created on Mon Nov 13 11:48:13 2023

@author: bjans
"""

""" Script to change presliced gcode to match your printer
- not implemented yet (devlopement in process)
+ implemented
Features:
    + manually change position by aplying offset
    + change retraction ditance
        - change retraction speed
    + change start procede (custom purgeline...)
        + change temperature
    + automatically center the model (only based on firts layer)
    - change speed settings
    
"""

import re
import time


# User Input
# acessing file:
path_input = r"C:\Users\bjans\Downloads\try_this.gcode" # path to file you want to edit
# you can name the output file however you want but don't forget to name it .gcode
# if input and output path are the same the old file will be overwritten
file_name = 'center_test_presliced_script' # without .gcode
folder_output = r"C:\Users\bjans\Downloads" # folder to write the new file to

own_start_gcode = True
# line in which the old start gcode ends (remember that in programming we start counting from 0)
old_start_gcode = 52
temp_end = 200 # nozzle temperature in C
temp_bed = 60 # bed temperature in C
path_start_gcode = r"C:\Users\bjans\OneDrive\Dokumente\CAD\Software\post_processing_gcode\pre_sliced_gcode\start_gcode.gcode"

change_retr = True
retr_d_1 = 4.5 # your retraction distance in mm

# recommended to use own start gcode otherwise the purgeline will be moved too
center_model = True # automatically centering the model
first_layer_height = 0.2 # first layer height in gcode (used to autmatically center models on buildplate)
# only square build plates
build_plate = 220 # saves build plate size in mm (used to calculate the center of the buildplate)


# manually move object by adding this value to every coordinate
manual_offset = False
X_offset = 60
Y_offset = -100

"""
NOT USED CURRENTLY

max_speed = 80 # maximum speed in mm/s
# convert to feedrate
max_Feedr = max_speed / 60
"""

# compile search key words
prog_move = re.compile(r'X.*Y') #'[X|Y]') #r'^G[1-3].*[X|Y]'
prog_comment = re.compile('[;]')
prog_digit = re.compile(r'[0-9\-.]+')
prog_F = re.compile('[F]') 
prog_G = re.compile(r'^G[1-3](?:\s|$)')#.*E
prog_comment = re.compile('[;]')
prog_E = re.compile('[E]')
prog_z_height = re.compile('^G1.*Z')


#middle_X_Y = (build_plate[0]/2,build_plate[1]/2) # calculate the middle of the buildplate
middle_buildplate = build_plate/2
    

# passed tests                
def read_position(direction: str, i: int)-> list:
    """
    Args: 
        direction (str): find value after key word
        i (int): line of gcode
    
    return:
        info (list): list with line start , line end end value

    """   
    line = lines[i]
    
    
    line_start = line.find(direction) + 1
    
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
    
                
def offset(direction: str, offset: float, i: int)-> None: # apply offset to coordinate
    """
    Args: 
        direction (str): which value to change
        offset (float): gets added to the current value
        i (int): line of gcode
    
    return:
        none

    """   
    global file_name
    line = lines[i]
    
    L_value = read_position(direction, i)
    
    value = L_value[2] + offset 
    # write new position value
    line_start = L_value[0]
    line_end = L_value[1]
    
            
    # writing line and inserting the new value
    line = line[0:line_start]+ str(round(value,4)) + line[line_end:] #+''
    
    if(value < 0 or value > build_plate):
        print(f'Error gcode outside of buildplate in line {i}')
        file_name = 'ERROR_WARNING!'
        
    # writing to gcode list
    lines[i] = line 
    
    
def change_retr_d(factor: float, i: int)-> None:
        """
        Args: 
            factor (float): factor to multiply with
            i (int): line of gcode
        
        return:
            none
            
        changes gcode output
        """   
        line = lines[i]
        
        L_value = read_position('E', i)
        
        value = L_value[2] * factor # oriinally + * for retr
        
        # write new position value
        line_start = L_value[0]
        line_end = L_value[1]
        
                
        line_end += 2
        # writing line and inserting the new value rounded to 5 places
        line = line[0:line_start]+ str(round(value,5)) + ' ' + line[line_end:len(line)]
        
        # writing to gcode list
        lines[i] = line + '\n'


""" calculate offset from distance of points to middle
Method will run into problems since there are different amount of ponits for specific shape 
(round more than straight!)
"""  
  
def find_first_layer(gcode: list, first_layer_height: float)-> tuple:
    """
    Parameters
    ----------
    gcode : list
        list with gcode
        
    first_layer_height : float
        height of first layer

    Returns
    -------
    tuple
        lines in gcode of first layer (start to end)
        
    Limitation:
        if z hop is enabled it won't work
    """
    i = 0
    found_start = False
    
    
    for line in gcode:
        # search for Z height
        if(prog_z_height.search(line)):
            layer_height = read_position('Z', i)
            
            if(layer_height[2] == first_layer_height):
                start_layer = i
                found_start = True
                
            elif found_start:
                # end of first layer has been found stop searching further
                end_layer = i
                break
                
        i+=1
        
    
    return (start_layer, end_layer)
  

def calculate_offset(first_layer: tuple)-> tuple:
    """
    Parameters
    ----------
    first_layer : tuple
        start and end line of first layer

    Returns
    -------
    tuple(float)
        X and Y offset

    """
    #TODO
    # calculate the X and Y positional offsets
    
    # write list of first layer which is in betwwen the boundries of the first layer and a move
    first_layer_list = [i for i in move_list if i>= first_layer[0] and i<= first_layer[1]]
    X = 0
    Y = 0
    
    for line in first_layer_list:
        X += read_position('X', line)[2]
        Y += read_position('Y', line)[2]
        
    # calculate average distance from middle of buildplate
    offset_X = X/len(first_layer_list)-middle_buildplate
    offset_Y = Y/len(first_layer_list)-middle_buildplate
    
    return (offset_X, offset_Y)


def extrusion(i: int) -> float: #reads E value
    """
    Args:
        line of gcode with extrusion (int)
        
    return:
        E value of line (float)
    
    """
    line = lines[i]
    
    result3 = prog_F.search(line)
    #find the position of extrusion value and save it as output
    if(result3):#in case F is behind E
        line_end = line.find('F')-1
        
    else:
        line_end = len(line) - 1
    
    line_start = line.find('E') + 1
    
    ex = line[line_start:line_end]
    
    if(ex == ''):#if ex is empty
        ex = 0
    
    ex = float(ex)
    
    return ex    

                
# passed test performance seems good            
def get_retr_d(Ex_list: list)-> float:
    """
    args:
        Ex_list (list): list with lines with extrusion
        
    return:
        retr_d_0 (float): old retrection distance
    """
    l_retr_search = 0
    List_retr = []
    found_retr_d = False
    retr_d_0 = 0
    
    for extr in Ex_list:
        #line = lines[extr]
        ex = extrusion(extr)
        
        if(ex < 0):
            l_retr_search += ex
            
        else:
            if(l_retr_search < 0): # end of retrection has been detected
                List_retr.append(abs(l_retr_search)) # store possible retraction distance as positive value
                
            l_retr_search = 0 # resetting the value
            
            # when the retraction distance has been found 4 times it is the retraction distance
            # sometimes the start gcode has a different retr distance so this is necessary to do
            for retr in List_retr:
                count = List_retr.count(retr) # count how many entries with the same values are in the list
                
                if(count == 4):
                    retr_d_0 = retr
                    found_retr_d = True
                    break
                
            if found_retr_d: # stop searching
                break
        
    return retr_d_0
            
    
# creating list to sort gcode lines
retr_list = []  
move_list = []
Ex_list = []
 
# seems to work now
def sort_gcode(gcode_list: list, offset: int = 0)-> None:
    """
    Args:
        gcode_list (list :str)
        offset (int): start of searching gcode default is 0

    Returns:
        None
    
    sort gcode in lists

    """
    global retr_d_0
    i = 0 + offset # not changing start gcode
    l_comp = 0
    comp_flag = False
    
    for line in gcode_list[offset:]:
        # check for G 1-3
        if(prog_G.match(line)):
            match_comment = prog_comment.search(line)
            # check for move (must incude X and Y)
            if(prog_move.search(line)):
                move_list.append(i)
                """
                if(match_comment):
                    #in case line has a comment
                    X = line.find('X') #finds the first X in line 
                    comment = match_comment.start() # test if this works and is faster
                    # this should be faster since we dond't need to search again
                    
                    #when the E is in front of the ; it's an extrusion
                    if(X < comment):
                        move_list.append(i)
                else:
                    move_list.append(i)
                """
            # check for extrusion to write retracton list
            if(prog_E.search(line)):
                if not(match_comment): #prevents finding the E in the comments like ;WIPE
                    Ex_list.append(i)
                    
                else:
                    # in case line has a comment
                    E = line.find('E') #finds the first E in line 
                    comment = line.find(';')
                    
                    # when the E is in front of the ; it's an extrusion
                    if(E < comment):
                        Ex_list.append(i)
                   
        i += 1
        
    # get retr distance from Ex_list    
    retr_d_0 = get_retr_d(Ex_list)    
    # after the Ex_list has been written now search for retr    
    for i in Ex_list:
        ex = extrusion(i)
        if (ex < 0):
            retr_list.append(i)
            # check for compensation of retraction
            comp_flag = True
        elif comp_flag:
            l_comp += ex
            retr_list.append(i)
            # compensation complete
            if(l_comp >= retr_d_0):
                comp_flag = False
                l_comp = 0
    
    

start_1 = time.time()  
# MAIN

with open(path_input, "r") as input_file:
    lines = input_file.readlines() # saves the gcode as an list
    
    

#TODO untested
if own_start_gcode:
    
    with open(path_start_gcode, 'r') as f_start:
        # saves start gcode to list
        start_lines = f_start.readlines()
    
    # change temp in start file
    prog_bed_temp = re.compile(r'\{bed_temp\}')
    prog_end_temp = re.compile(r'\{end_temp\}')
    
    l = 0
    for k in start_lines:
        bed = prog_bed_temp.search(k)
        hotend = prog_end_temp.search(k)
        
        if bed:
            start = bed.start()
            end = bed.end()
            
            start_lines[l] = k[:start]+ str(temp_bed) + k[end:]
        
        elif hotend:
            start = hotend.start()
            end = hotend.end()
            
            start_lines[l] = k[:start]+ str(temp_end) + k[end:]
            
        l += 1
    
    # delete old start gcode
    del lines[:old_start_gcode]
    
    # write own start gcode to gcode list    
    lines[:0] = start_lines
    
    # sort gcode withot changing the start gcode
    sort_gcode(lines, len(start_lines))
    
else:
    # sort gcode
    sort_gcode(lines)
    

# calculate retr factor  
retr_factor =  retr_d_1 / retr_d_0

# only change retr if enabled and the retraction distances are not the same
if(change_retr and retr_factor != 1):
    for retr in retr_list: 
        change_retr_d(retr_factor, retr)
   
# applying manual offset    
if manual_offset:
    for line in move_list:
        offset('X', X_offset, line)
        offset('Y', Y_offset, line)
        
if center_model:
    # find the first layer
    first_layer = find_first_layer(lines, first_layer_height)
    
    # calculate the offset
    offset_X_Y = calculate_offset(first_layer)
    
    # apply offset for model
    for line in move_list:
        offset('X', round(-1*offset_X_Y[0]), line)
        offset('Y', round(-1*offset_X_Y[1]), line)
    
path_output = folder_output + '/' + file_name + '.gcode'   

with open(path_output, 'w') as output:
    for line in lines:
        output.write("%s"  % line)           
output.close()

end_1 = time.time()
print('time to execute:',end_1-start_1) 
print('path to file:', path_output)

    
