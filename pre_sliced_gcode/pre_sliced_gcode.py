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
    + manually change position by applaying offset
    + change retraction
    - centers the model
    - change temperature
    - change speed settings
    - apply offset
    - change start procede (purgeline etc.) #text datei einfügen

"""
import re
import time

# Setup enable functions
center = True
change_temp = True
change_retr = True


# User Input
retr_d_1 = 4.5 # your retraction distance in mm
# only square build plates
build_plate = 220 # saves build plate size in mm
"""
NOT USED CURRENTLY
temp_end = 200 # nozzle temperature in C
temp_bed = 60 # bed temperature in C
z_offset = 0 
max_speed = 80 # maximum speed in mm/s
"""

# compile serch key words
prog_move = re.compile('[X|Y]') #r'^G[1-3].*[X|Y]'
prog_comment = re.compile('[;]')
prog_digit = re.compile(r'[0-9\-.]+')
prog_F = re.compile('[F]') 
prog_G = re.compile(r'^G[1-3]')#.*E
prog_comment = re.compile('[;]')
prog_E = re.compile('[E]')


#middle_X_Y = (build_plate[0]/2,build_plate[1]/2) # calculate the middle of the buildplate
middle_buildplate = build_plate/2
    
    
""" calculate offset from distance of points to middle
Method will run into problems since there are different amount of ponits for specific shape 
(round more than straight!)
"""

# passed tests                
def read_position(direction, i):
    """
    Args: 
        direction (str): find value after key word
        i (int): line of gcode
    
    return:
        info (list): list with line start , line end end value

    """   
    line = lines[i]
    
    line_start = line.find(direction) + 1
    
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
    
                
def offset(direction, offset, i): # apply offset to coordinate
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
    #print(value, L_value[2], offset)
    # write new position value
    line_start = L_value[0]
    line_end = L_value[1] + 2 # +2 because of blank space and then new Capital letter like Y or E
    
            
    #line_end += 2
    # writing line and inserting the new value
    line = line[0:line_start]+ str(round(value,3)) + ' ' + line[line_end:len(line)]
    
    if(value < 0 or value > build_plate):
        print('Error gcode outside of buildplate')
        file_name = 'ERROR_WARNING!'
        
    # writing to gcode list
    lines[i] = line
    
    
def change_retr_d(factor, i):
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
        #print(value, L_value[2], offset)
        # write new position value
        line_start = L_value[0]
        line_end = L_value[1]
        
                
        line_end += 2
        # writing line and inserting the new value rounded to 5 places
        line = line[0:line_start]+ str(round(value,5)) + ' ' + line[line_end:len(line)]
        
        # writing to gcode list
        lines[i] = line + '\n'
    
def calculate_offset(i):
    #TODO
    # calculate the X and Y positional offsets
    pass


def extrusion(i): #reads E value
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
def get_retr_d(Ex_list):
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
def sort_gcode(gcode_list)-> None:
    """
    Args:
        gcode_list (list :str)

    Returns:
        None
    
    sort gcode in lists

    """
    global retr_d_0
    i = 0 
    l_comp = 0
    comp_flag = False
    
    for line in gcode_list:
        # check for G 1-3
        if(prog_G.match(line)):
            match_comment = prog_comment.search(line)
            # check for move
            if(prog_move.search(line)):
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
        else:
            if comp_flag:
                l_comp += ex
                retr_list.append(i)
                # compensation complete
                if(l_comp >= retr_d_0):
                    comp_flag = False
                    l_comp = 0
    
    

start_1 = time.time()  
# MAIN
path_input = r"C:\Users\bjans\Downloads\Shape-Cylinder_35m_0.20mm_210C_PLA_ENDER5PRO.gcode"
# you can name the output file however you want but don't forget to name it .gcode
# if input and output path are the same the old file will be overwritten
file_name = 'test_presliced_script'
folder_output = r"C:\Users\bjans\Downloads"

#path_output = r"C:\Users\bjans\Downloads\test_presliced script.gcode"


with open(path_input, "r") as input_file:
    lines = input_file.readlines() # saves the gcode as an list

# sort gcode
sort_gcode(lines)  

# calculate retr factor  
retr_factor =  retr_d_1 / retr_d_0

# only change retr if enabled and the retraction distances are not the same
if(change_retr and retr_factor != 1):
    for retr in retr_list: 
        change_retr_d(retr_factor, retr)
    

# manually move object
X_offset = 10
Y_offset = 10

for line in move_list:
    offset('X', X_offset, line)
    offset('Y', Y_offset, line)
    

path_output = folder_output + '/' + file_name + '.gcode'   

with open(path_output, 'w') as output:
    for line in lines:
        output.write("%s"  % line)           
output.close()

end_1 = time.time()
print('time to execute:',end_1-start_1) 
print('path to file:', path_output)
    
