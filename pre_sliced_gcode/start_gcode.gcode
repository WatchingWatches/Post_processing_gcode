M73 P0 R34
M201 X700 Y700 Z100 E1000 ; sets maximum accelerations, mm/sec^2
M203 X500 Y500 Z5 E60 ; sets maximum feedrates, mm / sec
M204 P600 R1000 T500 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
M205 X8.00 Y8.00 Z0.40 E5.00 ; sets the jerk limits, mm/sec
M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec

;TYPE:Custom
G90 ; use absolute coordinates
M83 ; extruder relative mode
M140 S{bed_temp} ; set final bed temp
G4 S30 ; allow partial nozzle warmup
G28 ; home all axis
G1 Z5 F240
G1 X2.0 Y10 F3000
M104 S{end_temp} ; set final nozzle temp
M190 S{bed_temp} ; wait for bed temp to stabilize
M109 S{end_temp} ; wait for nozzle temp to stabilize
G1 Z0.28 F240
G92 E0
G1 X2.0 Y200 E15 F1500 ; prime the nozzle
G1 X2.3 Y200 F5000
G92 E0
G1 X2.3 Y10 E30 F1200 ; prime the nozzle
G92 E0
G21 ; set units to millimeters
G90 ; use absolute coordinates
M83 ; use relative distances for extrusion
; Filament gcode
M107
;LAYER_CHANGE
;Z:0.2
;HEIGHT:0.2
;BEFORE_LAYER_CHANGE
G92 E0