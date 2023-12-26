# Script to modify presliced gcode
## Features:
- Change the retraction distance
- Change position of object on buildplate (manually)

## Limitations:
- When changing the position of the object the purge line will be moved too which might lead to a problem (when this happens the program warns you)
- Absolute coordinates must be used

## Goals for the future:
Develope the script so far, that presliced gcode made for different printers can be used with minimal effort.
There are many more features planned for the future see the docstring of the script to learn more.
