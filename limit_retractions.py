# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Sat Aug 26 12:25:10 2023

@author: bjans
Post processing script to limit maximum amount of retractions,
to prevent ground down filament from the extruder
If you are interested in how the program works read the explenation of the main loop
in line 246... 
"""

"""        ***Limitations***
-no support for G2/G3 commands yet only G1
-only relative extrusion mode supported!!
    (in prusaslicer go to printer settings and activate "Use relative E distance" You must be in expert mode)

"""

"""        ***PLEASE NOTE:***
In Prusa slicer the script gets called when saving the gcode
Therefore it's not displayed with the modifications of the script in the preview
When you want a correct preview open the saved gcode in an gcode viewer
When you run the script for the first few time check that everything is working as it should
 
The larger the file the longer the processing time

if you have questions write on reddit to me u/Watching-Watches
Use at your own risk!
"""

import re
import sys
from time import time
#from icecream import ic #helps with debugging

#start timer
start_time = time()

#debugging options
debugging_extrusion = False
debugging_run = False
debugging_remove_E = False
debugging_del_retr = False

#operating options
#set all three to True if you want to run it in slicer
Output = True
run_mainloop = True
run_in_slicer = True

#optional parameters i recommend to set all to True
control_stats = True
wait_for_error = True
serach_for_retr_d = True #decide if it should search the comments in gcode file for ; retract_length = 4.5
pause_for_info = True #pauses at the end of the script to show control stats

#important parameters
#retr_d will be overwritten when "serach_for_retr_d = True"
retr_d = 4.5 #retraction distance must be positive!!
n_retract_max = 10 #maximum retracts in interval
k = 1 #factor for distance / interval in which the retractions are looked at


n_retract = 0
i = 0
p_0 = 0
ex = 0
k_n = 0
l_ex = 0
l_retr = 0
n_corrections = 0

Ex_list = [] #list of lines with extrusions
REMOVE_list = [] # list of lines where the retraction needs to be removed


#passed tests
def find_E(i):#writes list with lines, which contain G1 moves with E 
    line = lines[i]
    
    if(re.search('^G1\s+[X+Y+F+E]', line)):
        if(re.search('[E]', line)):#searches for E in G1 move
            if not(re.search('[F]', line) and re.search('[X|Y]', line)):# both are in line do nothing
                if not(re.search('[;]', line)): #prevents findig the E in the comments like ;WIPE
                    Ex_list.append(i)
                    
                else:
                    #in case line has a comment
                    E = line.find('E') #finds the first E in line 
                    comment = line.find(';')
                    
                    #when the E is in front of the ; it's an extrusion
                    if(E < comment):
                        Ex_list.append(i)
            
#passed tests
def extrusion(i): #reads E value
    global k_n
    line = lines[i]
    
    #find the position of extrusion value and save it as output
    if(re.search('[F]', line)):#in case F is behind E
        line_end = line.find('F')-1
    else:
        line_end = len(line) - 1
    
    line_start = line.find('E') + 1
    
    ex = line[line_start:line_end]
    
    if(ex == ''):#if ex is empty
        ex = 0
    
    ex = float(ex)
    
    if (debugging_extrusion == True):
        k_n +=1 #counts extrusions
        print(ex,'line:',i+1) # for debugging purpose print extrusion value and the line 
           
    return ex


"""How  del_retr works:
This fuction deletes retractions
 
when called search:
    inserted list and romove n_remove retractions
    starting from the back of the list

deleting:
    find negative value (retraction)
    when whole retraction found go front in list until retraction compensation is found
    
    do this n_remove times all lines are saved in a list
    
    when the loop is finished remove all the extrusion values in gcode

"""


#passed tests
def del_retr(REMOVE_list, n_remove): #deletes retractions inside of list n_remove times
    corrections = 0 #how often the retraction was removed within the function
    l_retr = 0
    start_search_ex = 0

    del_list = [] #list of lines with retractions, which will be empty at the begginning 
    
    for z in range(len(REMOVE_list)-1,0,-1):
        search = REMOVE_list[z] #contains lines which will lose retractions
        ex_z = extrusion(search)
        if(ex_z < 0): #retraction found
            if(l_retr == 0):
                start_search_ex = z  #start from here to search for extrusion in next loop
                
                
            l_retr += ex_z
            del_list.append(search)
            
            
            if(l_retr == -1*retr_d): # full retraction has been found
                #go front in list until the positive extrusion is found
                l_ex = 0
            
                #remove extrusion compensation
                for j in range(start_search_ex,len(REMOVE_list),1):
                    search_ex = REMOVE_list[j]
                    if(extrusion(search_ex) > 0):
                        l_ex += extrusion(search_ex)
                        
                    if(l_ex <= retr_d): #add to list to remove retraction compensation
                        del_list.append(search_ex)
                        #print('success')
                        
                        if(l_ex >= retr_d):#exits loop
                            break
                    
                l_ex = 0 #resetting the values
                l_retr = 0
                corrections +=1 #the list has been written for a full correction
                if(n_remove == corrections):
                    break
                              
        
    #finally deleting all the retractions
    for m in range(0,len(del_list),1):
        remove_E(del_list[m])
        
   
        
#passed tests
def remove_E(i): 
    global lines,line
    line = lines[i]
    if(re.search('[F]', line) or not re.search('[X|Y]', line)): #in case F is behind E
        line = ';here was an retraction\n' #adds a comment in the gcode
           
    else:
        end = line.find('E')
        start = 0
    
        line = line[start:end]+'\n' #\n initiates newline
    
    lines[i] = line
    
    

if (run_in_slicer == True):
    path_input = sys.argv[1]
    path_output = path_input #same input and output
    
else:#if not running in slicer
    #insert the path for the input and output file here
    path_input = 'C:/Users/bjans/OneDrive/Dokumente/CAD/Software/post_processing_gcode/retraction_script_test_21m_0.20mm_210C_PLA_ENDER5PRO.gcode'
    #you can name the output file however you want but don't forget to name it .gcode
    #if input and output path are the same the old file will be overwritten
    path_output = 'C:/Users/bjans/OneDrive/Dokumente/CAD/Software/post_processing_gcode/retraction_script_test_result.gcode'

with open(path_input, "r") as input_file:
    lines = input_file.readlines() #saves the gcode as an list
    
#searches in gcode for retraction distance value    
if(serach_for_retr_d):
    for find_retr_d_value in range(len(lines)-1, 0, -1):
        line = lines[find_retr_d_value]
        
        if(re.search('; retract_length = ', line)):
            line_end = len(line) - 1
        
            line_start = line.find('=') + 1
            
            retr_d = line[line_start:line_end]
            retr_d = float(retr_d)
            
            break #once it's found the value, the search ends
            
        if(find_retr_d_value == 1): #value not found in script
            print('no retraction distance value found!')
            print('Enter retraction distance manually and press enter use "." as decimal point', '\n')
            print('check your output options in the slicer settings')
            
            retr_d = input()
            

"""How the main loop works:
    
The main loop decides when and how many retractions should be deleted

First it runs the function find_E to find all the lines with extrusion in the gcode file
The while loop goes trough the file and observes the extrusion
It counts the extrusion length until it's longer than the retraction distance*k
At the same time it counts the number of retractions
When there are too many retractions in the extrusion interval it'll delete those who are above the limit (n_retract_max)
In both cases the variables and list get resetted and the next interval of extrusion get's observed

Before deleting retractions the list must end with a full retraction or must include the retraction correction

"""

error_n = 0
ges_retr = 0
ges_retr_remove = 0

if (run_mainloop):
    for l in range(0, len(lines)-1, 1):#get the list with extrusion
        find_E(l)
    i = 0
    try:
        while(i < len(Ex_list)-1): #main loop 
            i += 1
            p = Ex_list[i] #only observes lines with relevant E's 
            REMOVE_list.append(p) #writes list in which gcode lines the algorythem is searching
            ex_p = extrusion(p)
            
            l_ex += ex_p #sum of extrusion
            
            if(ex_p < 0): #negative values = retraction
                l_retr += ex_p #sum of retraction (negative value)
            
                if(l_retr <= -1*retr_d):
                    n_retract += 1 #retraction count
                    ges_retr += 1
                    
                    l_retr = 0 #resetting of the retraction length
                    
                
               
            if(l_ex > k*retr_d):# checks if to many retractions in extrusion interval
                if(n_retract > n_retract_max): #innitiate deletions of retractions
                    n_remove = n_retract - n_retract_max #how many retractions need to be removed
                    compensation = 0
                    #check if last value is negative
                    if(ex_p < 0):
                        for front in range(i+1,len(Ex_list)):
                            p = Ex_list[front]
                            ex_p0 = extrusion(p)
                            
                            if(ex_p0 < 0):
                                REMOVE_list.append(p)
                                
                            else:
                                REMOVE_list.append(p)
                                
                                compensation += ex_p0
                                
                                if(compensation >= retr_d):# full retraction in the end of list
                                    break #stops adding more to the list
                                    
                    #check if the extrusion of the last elements is bigger/equal than retrction distance                
                    if(ex_p >= 0):
                        compensation_back = 0
                        for back in range(len(REMOVE_list)-1,0,-1):
                            p = REMOVE_list[back]
                            ex_p = extrusion(p)
                            
                            if(ex_p < 0): #retraction before break condition in list
                                for front in range(i+1,len(Ex_list)):
                                    p = Ex_list[front]
                                    ex_p0 = extrusion(p)
                                    if(ex_p0 < 0):
                                        REMOVE_list.append(p)
                                        
                                    else:
                                        REMOVE_list.append(p)
                                        compensation += ex_p0
                                        
                                        if(compensation >= retr_d):
                                            i = front 
                                            break #stops adding more to the list
                                            
                            else: #positive value
                                compensation_back += ex_p
                                if(compensation_back >= retr_d): #do nothing, if negative value comes before it it will add more to the list
                                    break
                            
                               
                    ges_retr_remove += n_remove #counts all the deleted retractions   
                    del_retr(REMOVE_list, n_remove) #run function which deletes retractions within the list
                    
                    n_corrections += 1 #this shows in the end how many corrections the program made
                    
                    #reset all values
                    n_retract = 0
                    #print('called')
                    l_ex = 0
                    l_retr = 0
                    
                    REMOVE_list = [] #deleting the previous list
                    
                else:    
                    #reset all values
                    n_retract = 0
                    
                    l_ex = 0
                    l_retr = 0
                    
                    REMOVE_list = [] #deleting the previous list
            
        
        
    except Exception as error:
        #if a bug occures in the function it will tell you the error message at the end of the gcode
        #and inside the terminal
        end_line = len(lines)-1
        
        error_message = ';' + str(error) + '\n'
        lines.append(error_message)
        
        print('ERROR check gcode in line:'+ str(Ex_list[i]))
        print('Error message:' + str(error_message))
        error_n += 1
            
     
    #prevents the terminal from beeing closed and shows you that there has been an error        
    if(wait_for_error == True and error_n > 0):
        print(str(error_n) + 'Errors')
        print('successful corrections:' + str(n_corrections))
        print('Press Enter to close')
        input()
        

           
if(debugging_run): #run different debugging tests
    for l in range(0, len(lines)-1, 1): #get the list with extrusion
        find_E(l)
    
    if(debugging_remove_E):
        for h in range(0,len(Ex_list)-1,1): #remove all E to see if it's working
            remove_E(Ex_list[h])
    
    
    if(debugging_del_retr):
        Test_del_retr = []
        for dd in range(3800,4000,1): #test in interval to delete retractions
            Test_del_retr.append(Ex_list[dd])
        
        del_retr(Test_del_retr, 3)

end_time = time()
        
#prints useful information in Terminal    
if(control_stats  and run_mainloop):
    print('Script called: limit_retractions.py')
    print('Path to script: ', sys.argv[0], '\n')
    
    print('Number of corrections made: ', n_corrections)
    print('Number of deleted retractions: ', ges_retr_remove)
    print('Total number of retrections in file: ', ges_retr, '\n')
    
    print('Retraction distance used: ', retr_d)
    print('Used factor k = ', k, '& n_retract_max = ', n_retract_max, '\n')
    
    total_time = end_time - start_time
    print('Run time: ', total_time, '[s]', '\n')
    
    if(pause_for_info and run_in_slicer):
        print('Press Enter to close')
        input()
    
    
if(Output == True):
    #saves a list as a file
    with open(path_output, "w") as output:
        for t in range(0,len(lines)):        
            output.write("%s"  % lines[t])           
    output.close()
input_file.close()  
