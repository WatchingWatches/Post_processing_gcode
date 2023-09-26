"""
This script changes the value of the fan speed to the number where it is actually spinning.
This prevents not cooling the layers when it's actually intended.
If the fan speed is set to 0 the program won't change that, since it's intended not to spin.

I would recommend to test the program first to see that everything is working.
To do so save a presliced file and set "run_in_slicer = False". Then insert the path in line 55..., run the program and compare both files
"""
#!/usr/bin/python
import re
import sys
from math import ceil

run_in_slicer = True
use_percent = True

min_fan_percent = 22 #enter lowest value where the fan is spinning as whole number 25% is 25

min_fan_speed = 57 #must be value between 0 and 255 but will be ignored if use_percent is set to True

if(use_percent == True):
    min_fan_speed = ceil(255*min_fan_percent/100) #rounded up value
        
#main function
def change_fan_speed(i):
    line = lines[i]
    
    if(re.search('^M106 S', line)): #search for the M106 command
        line_start = line.find('S')
        if(re.search(';', line)):
           line_end = line.find(';') #value is in between of S and ;
           comment = ' ' + line[line_end:len(line) - 1] #saves comment
           
        else:
            line_end = len(line) - 1 # value is in between S and the end of the line
            comment = ''
        
        fan_speed = line[line_start+1:line_end] # value is behind S
        
        fan_speed = float(fan_speed) # convert string to float for the if condition
        
        if(fan_speed != 0 and fan_speed < min_fan_speed ):
            fan_speed = min_fan_speed
            
            line = line[0:line_start]+ str(fan_speed) + comment + '\n'#\n initiates newline
            
            lines[i] = line #write new line
                

if (run_in_slicer == True):
    path_input = sys.argv[1]
    path_output = path_input #same input and output
    
else:#if not running in slicer
    #insert the path for the input and output file here
    path_input = "C:/Users/bj/Downloads/funko_wall_mount_5h0m_0.20mm_215C_PLA_ENDER5PRO.gcode" #example path use your own path!
    #you can name the output file however you want but don't forget to name it .gcode
    #if input and output path are the same the old file will be overwritten
    path_output = "C:/Users/bj/Downloads/funko_wall_mount_5h0m_0.20mm_215C_PLA_ENDER5PRO_test.gcode"

with open(path_input, "r") as input_file:
    lines = input_file.readlines() #saves the read gcode as an list
    

#call the main function and go through all of the g-code
for l in range(0, len(lines)-1, 1):
    change_fan_speed(l)


#saves a list as a file
with open(path_output, "w") as output_file:
    for t in range(0,len(lines)):        
        output_file.write("%s"  % lines[t])           
output_file.close() # close the file

input_file.close()
