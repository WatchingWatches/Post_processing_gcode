# Post_processing_gcode_Prusa_slicer
How to run script from Slic3r/Prusaslicer:
go to print settings => output options => Post processing scripts then enter your path to the python.exe and the python script like this: "C:\Users\bj\anaconda3\python.exe" "C:\Users\bj\OneDrive\Dokumente\CAD\Software\post_processing_gcode\min_fan_speed.py";
If you want to run the script from the slicer "set run_in_slicer = True".
If the slicer can't execute python you'll get the error: Win32 error 193
For debugging run the script in an IDE with a presliced gcode.
Use on your own risk!
![image](https://github.com/WatchingWatches/Post_processing_gcode/assets/106354710/d433713b-6e07-48ab-8253-5edffec04f27)

Example of how the script limit_retractions.py manipulates the retractions of the gcode file

![Collage_before_after](https://github.com/WatchingWatches/Post_processing_gcode/assets/106354710/bc6427a8-e1f5-40dd-9481-be738bed33a3)
