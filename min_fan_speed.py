# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 21:59:38 2023

@author: bjans
This script changes the value of the fan speed to the number where it is actually spinning.
This prevents not cooling the layers when it's actually intended.
If the fan speed is set to 0 the program won't change that since it's intantually not spinning

I would recommend to test the program first to see that everything is working
Use at your own risk!
"""
#!/usr/bin/python
import re
import sys
from math import ceil

run_in_slicer = True #run from slicer or from path
use_percent = False
#this setting speeds up the fan first and then sets the min fan speed
#this is needed if the fan can run at the min speed, but doesn't start on it's own
blib_function = True 
wait_for_error = True #recomended to set to True otherwise you won't be notifyed if there was an error

blib_speed = 100 #must be value between 0 and 255 fan speed which accelerates fan to get it started for lower fan speed

# make sure that the fan keeps spinning at that speed
min_fan_percent = 16 #enter lowest value where the fan is spinning as whole number 25% is 25

min_fan_speed = 41 #must be value between 0 and 255 but will be ignored if use_percent is set to True

if(use_percent == True):
    min_fan_speed = ceil(255*min_fan_percent/100) #rounded up value
        
#main function
def change_fan_speed(i):
    line = lines[i]
    
    if(re.search('^M106 S', line)): #search for the M106 command
        line_start = line.find('S') + 1 #+1 one to exclude S itself
        if(re.search(';', line)):
           line_end = line.find(';') #value is in between of S and ;
           comment = ' ' + line[line_end:len(line) - 1] #saves comment
           
        else:
            line_end = len(line) - 1 # value is in between S and the end of the line
            comment = ';min fan speed' #adds comment 
        
        fan_speed = line[line_start:line_end] # value is behind S
        
        fan_speed = float(fan_speed) # convert string to float for the if condition
        
        if(fan_speed != 0 and fan_speed < min_fan_speed ):
            fan_speed = min_fan_speed
            
            if(blib_function == True):
                #insert blib then insert min fan speed after g1 move
                #if blib and fan speed would be directly after eachother the blib doesn't work
                line_blib = ';added blib'+ '\n' + 'M106 S'+ str(blib_speed) + '\n' # bumbs up fan speed to start fan
                lines[i] = line_blib #write blib to initial fan speed
                for j in range(i, len(lines)-1):
                    move = lines[j]
                    if(re.search('^G1', move)): 
                       lines[j] = move + comment + '\n' + line[0:line_start]+ str(fan_speed) + '\n'#insert min fan speed after g1
                       break
                   
            else:
                line = comment + '\n' + line[0:line_start]+ str(fan_speed) + '\n'#\n initiates newline
                lines[i] = line #write new line
            
                
            

if (run_in_slicer == True):
    path_input = sys.argv[1]
    path_output = path_input #same input and output
    
else:#if not running in slicer
    #insert the path for the input and output file here
    path_input = "C:/Users/bj/Downloads/funko_wall_mount_5h0m_0.20mm_215C_PLA_ENDER5PRO.gcode"
    #you can name the output file however you want but don't forget to name it .gcode
    #if input and output path are the same the old file will be overwritten
    path_output = "C:/Users/bj/Downloads/funko_wall_mount_5h0m_0.20mm_215C_PLA_ENDER5PRO_test.gcode"
    
with open(path_input, "r") as input_file:
    lines = input_file.readlines() #saves the read gcode as an list
    
error_n = 0  

#call the main function and go through all of the g-code
for l in range(0, len(lines)-1, 1):
    try:
        change_fan_speed(l)
        
    except Exception as error:
        #if a bug occures in the function it will tell you the error message at the end of the gcode
        #and inside the terminal
        end_line = len(lines)-1
        
        error_message = ';' + str(error) + '\n'
        lines.append(error_message)
        
        print('ERROR check gcode in line:'+ str(l))
        print('Error message:' + str(error_message))
        error_n += 1
        
 
#prevents the terminal from beeing closed and shows you that there has been an error        
if(wait_for_error == True and error_n > 0):
    print('Press Enter to close')
    input()


#writes the file
with open(path_output, "w") as output_file:
    for t in range(0,len(lines)):        
        output_file.write("%s"  % lines[t])           
output_file.close() # close the file

input_file.close()
