# Post_processing_gcode_Prusa_slicer
How to run script from Slic3r/Prusaslicer:
go to print settings => output options => Post processing scripts then enter your path to the python.exe and the python script like this: "C:\Users\bj\anaconda3\python.exe" "C:\Users\bj\OneDrive\Dokumente\CAD\Software\post_processing_gcode\min_fan_speed.py";
If you want to run the script from the slicer "set run_in_slicer = True".
If the slicer can't execute python you'll get the error: Win32 error 193
For debugging run the script in an IDE with a presliced gcode.
Use on your own risk!
![image](https://github.com/WatchingWatches/Post_processing_gcode/assets/106354710/d433713b-6e07-48ab-8253-5edffec04f27)


Copyright (c) 2012-2023 Scott Chacon and others

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
