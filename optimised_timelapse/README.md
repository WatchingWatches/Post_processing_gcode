# Postprocessing script to optimise timelapse:
## Introduction:
The script inserts the "TIMELAPSE_TAKE_FRAME" command every layer at one point, which is the closest to a choosen point.
The purpose is to take timelapse with the print head at the best possible position, without effecting the printing process.
The script also lets you pick a minimum amount of layers at which the timelapse should be activated.
If the layer number is below it won't insert the "TIMELAPSE_TAKE_FRAME" command.

## How to set up:
If you have already inserted the "TIMELAPSE_TAKE_FRAME" command inside of your gcode delete it. Otherwise there will be two pictures every layer.
If you want to run the script every time after you save the gcode set "run_in_slicer = True".
Follow the instructions of the README.md in the main folder of this repository to set it up in your slicer.
You can edit the picture command to whatever you are using.

### Option 1 (recommended):
Insert ";AFTER_LAYER_CHANGE" into your custom-gcode after layer change section and set "search_for_comment = True" inside of the script.
The program then searches for this inside of the gcode and knows, that this is a new layer. 

### Option 2:
Set "search_for_comment = False" inside of the script, to enable this option.
The script then searches for every Z movement inside of the gcode and interprets it as a layer change.
If you are using Z-hop don't activate this option since it will generates a picture every time you retract. So i highly recommend using option 1 with enabled Z-hop.
If you are using Firmware retraction with Z-hop this option will work correctly.

## Problems and limitations:
Not supported:
- Z hop retractions (only with search_for_comment set to False)
- non planar slicing (only with search_for_comment set to False)
- relative movements

Eventhough the scipt works correctly, this doesn't mean that the picture will be taken, when the print head is at the position given inside of the gcode (the coordinates in front of the "TIMELAPSE_TAKE_FRAME" command).
I had the problem, that the latency of the camera (time difference in between reality and picture) is so big, that the printhead is at a completly different location, when the picture is taken.
The faster your printer is chaning coordinates and the higher the latency of the camera the bigger the effect. On smaller prints the effect will most likely be bigger than on large ones.

I'm thinking about solving this unexpected problem, by measuring the latency and inserting the "TIMELAPSE_TAKE_FRAME" command before the gcode coordinate is reached, by calculating where the print head will be before the coordinate is reached.
Since the latency isn't constant this solution won't be perfect and will cause higher calculation time of the script.

If you have a better solution please let me know.

## Preview of the actual picture coordinates:
To activate this feature set "visualize_picture_coordinates = True" and change the "path_output_picture" to the desired path on your computer.
This feature will write a small gcode file containing all the coordinates at which the picture will be taken.
You might be able to visualize it in a gcode previewer (it doesn't always work well).

This is how it could look like in the previewer:
![example_visualization_take_frame_G1_only](https://github.com/WatchingWatches/Post_processing_gcode/assets/106354710/ac59840f-5752-4eb2-9f16-8c3bdd02c71e)

If the file contains G2/G3 commands it looks like this (same model as in the first picture):
![example_visualization_take_frame](https://github.com/WatchingWatches/Post_processing_gcode/assets/106354710/6e8f2b24-0d39-49f6-9e52-7a6257fd1adb)
