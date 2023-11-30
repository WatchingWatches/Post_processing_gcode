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


Chat gpt summorized the function of my program "limit_retractions.py" like this:

This Python script appears to be a post-processing script designed for modifying G-code files generated by PrusaSlicer. Let's break down its main functionalities:

### Purpose:
The script is intended to limit the number of retractions in a 3D printing G-code file. Excessive retractions can potentially lead to filament grinding issues. The script operates on the assumption that the G-code is in relative extrusion mode.

### Key Features:

1. **Header Information:**
   - The script begins with comments providing information about its purpose, limitations, and important instructions for using it in PrusaSlicer.

2. **Parameters and Options:**
   - The script includes a section for setting various parameters and options, including debugging flags, operating options, and optional parameters like controlling statistics display.

3. **File I/O:**
   - The script reads the input G-code file and stores its lines in a list.

4. **Retraction Distance Search:**
   - The script searches for the retraction distance in the comments of the G-code. If not found, it prompts the user to enter the retraction distance manually.

5. **Main Processing Loop:**
   - The main loop iterates through the lines of the G-code.
   - It identifies lines with extrusion (G1, G2, or G3 moves with an E parameter) and builds a list (`Ex_list`) of these lines.

6. **Retraction Limiting Logic:**
   - The script observes the extrusion and retraction lengths, counting the number of retractions within a specified extrusion interval.
   - If the number of retractions exceeds a certain limit (`n_retract_max`), it identifies and removes excessive retractions.

7. **Correction Count and Debugging:**
   - The script keeps track of the number of corrections made and displays debugging information if specified.

8. **File Output:**
   - The modified G-code is saved to the output file.

9. **Control Statistics and Timing:**
   - The script optionally displays control statistics, such as the number of corrections, deleted retractions, and runtime.

10. **Debugging Flags:**
    - Various debugging flags are provided to enable or disable specific debugging features, such as removing all extrusions or deleting retractions in a specific interval.

11. **Final Information Display:**
    - The script displays information about the run, including the script name, path, number of corrections, deleted retractions, retraction distance used, and runtime.

### Notes:
- The script uses comments extensively to provide information and instructions.
- It includes error handling and displays error messages if an exception occurs.

### Recommendations:
- Before using this script, users should carefully review the provided comments and instructions.
- The script is designed to be called within PrusaSlicer, and it might not display modifications in the PrusaSlicer preview due to the timing of script execution.

This is a high-level overview, and if you have specific questions about certain parts of the script or its functionality, feel free to ask!
