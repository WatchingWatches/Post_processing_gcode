# Script to modify presliced gcode
## Features:
- Change the retraction distance
- Change position of object on buildplate (manually)
- Automatically center the model on your buildplate, based on the first layer (use with your own start gcode)
- Change the start gcode with custom temperature

## How to use the script:
Edit the variables underneath User Input to your needs and follow the instructions of the comments in the script. 

## How to insert start gcode:
Copy you start gcode from your slicer inside of a gcode file and change the bed temperature to "{bed_temp}" and the hotend temperature to "{end_temp}". Look inside of the excample gcode file.
Write the path of the start gcode to "path_start_gcode =". 
The program doesn't automatically know where the start gcode of the given file ends. This means you have to give it the line, in which the start gcode ends.

## Limitations:
- When changing the position of the object the purge line will be moved too which might lead to a problem (when this happens the program warns you). If you use your own start gcode the offset won't affect your purgeline.
- Absolute coordinates must be used (X,Y)
- Relative Extrusion must be used (check if the E values get added up, this would mean it's absolute extrusion)
- If Z-Hop is used the automatic center feature won't work properly
- You must have the same nozzle size, which the gcode uses

## Goals for the future:
Develope the script so far, that presliced gcode made for different printers can be used with minimal effort.
There are many more features planned for the future see the docstring of the script to learn more.

Before printing always check if everything looks fine with a gcode viewer. If you got any issues just start an issue here on Github.
