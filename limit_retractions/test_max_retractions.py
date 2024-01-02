# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 14:45:46 2024

@author: bjans
"""

"""
Test the maximum amount of retractions (n_retr_max) to calibrate for limit_retractions.py by
writing a test gcode.
If you can't print the purge line in the end lower the n_retr_max in limit_retractions.py.
Please read all of the comments carefully and adjust the code if necassary.
"""
# USER PARAMETER
# use the settings, which you normally use
temp_nozzle = 200           # in °C
retr_d = 4.5                # in mm
retr_speed = 30             # retraction speed in mm/s
deretr_speed = 30           # deretraction in mm/s (often the same as retr_speed)
n_retr_max = 30             # maximum amount of retractions (must be int)
move_z = 15                 # move nozzle away from print bed

folder_path = r"C:\Users\bjans\Downloads" # path to folder to write file to

# USER INPUT END
extrude = retr_d/n_retr_max # extrusion after retr to get some more resistance for the extruder
feedrate_retr = retr_speed*60    # calculate the feedrate of retr
feedrate_deretr = deretr_speed*60    # calculate the feedrate of deretr


filename = '/retr_limit_test-n_retr_max='+ str(n_retr_max)+ '-temp='+ str(temp_nozzle)+ '.gcode'
path_out = folder_path+ filename

# prepare for test
gcode = ['G90 ; use absolute coordinates', 'M83 ; extruder relative mode', 'G21 ; set units to millimeters', 'G28']
gcode.append('G1 Z'+ str(move_z) + ' F240')
gcode.append('M104 S'+ str(temp_nozzle)+ ' ; set final nozzle temp')
gcode.append('M109 S'+ str(temp_nozzle)+ ' ; wait for nozzle temp to stabilize')
# extrude a bit of filament, so the filament is directly at the nozzle
gcode.append('G1 E8 F1500 \n')
# start the test
gcode.append('; test started')
for i in range(n_retr_max):
    # retract
    gcode.append('G1 E'+ str(-retr_d)+ ' F'+ str(feedrate_retr))
    # extrude a tiny bit
    gcode.append('G1 E'+ str(round(retr_d+extrude, 5))+ ' F'+ str(feedrate_deretr))
gcode.append('; test finished \n')

# try printing a purge line
# if the printer is unable to do so the n_retr_max is set too high
# i have a 220 mm printed adjust this to your needs!
# MAY NEED ADJUSTMENT!
gcode.extend(['G1 Z0.28 F240',
'G92 E0',
'G1 X2.0 Y200 E15 F1500 ; prime the nozzle',
'G1 X2.3 Y200 F5000',
'G92 E0',
'G1 X2.3 Y10 E30 F1200 ; prime the nozzle',
'G92 E0'])

# end gcode
gcode.extend(['G91 ;Relative positioning',
'G1 E-4 F2700 ;retract',
'G90 ;absolute positioning',
'G1 Z'+ str(move_z)+ ' F600 ; Move print bed down',
'G28 X0 Y0 ; home xy',
'M140 S0 ; turn off heatbed',
'M104 S0 ; turn off temperature',
'M107 ; turn off fan',
'M84 X Y E ; disable motors'])

# write file
with open(path_out,'w') as f:
    f.write('; Calibration script for testing the maximum retractions \n')
    
    for line in gcode:
        f.write("%s"  % line + '\n')
        
f.close()
