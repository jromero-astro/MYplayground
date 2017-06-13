#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 12:41:32 2016

@author: jromero
"""
import sys,os
import modifier_POVRay as my_functions  # I call the python file where functions are defined
#										   usage: my_function.NAME_OF_A_FUNCTION(arguments)
#
yes_posibilities = ['y','yes','Y','Yes','YES']
no_posibilities  = ['n','no','N','No','NO']
all_posibilities = ['all','a','All','ALL','All']
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#### MODIFY IF NECESSARY ##############
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
# 1 - Do you want to modify the .pov
#     and to generate teh PNGs?
ModifyPov = 'y'
# 2 - Do you want to run the video/GIF
#     generator?
video_GIF = 'y'
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
####### Tips #######
# check the list of functions, if you don't need one of them just 
#  comment those not needed in this Main file (with # at the beginning
#  of the line).
###############################################################################
#
#
###### 1. ASKING THE USER FOR THE WORK DIRECTORY ######
#
#
""" Directories """
# Select directories.
# Printing the current path to user
current_wd = os.getcwd()        # Getting the path to current dir
print('\nCurrent path:\n\t>> '+str(current_wd))
print('\n')
#
# Asking user the path to be used (DEFAULT = current)
print('Path to your work dir:\nExample: [/home/Your_User/dir1/dir2.../workDir]:\n')
path = raw_input("\t(current)>>")
if path == "": path = str(current_wd)
#
#
###### 2. CALLING THE FUNCTIONS TO BE USED ######
if ModifyPov in yes_posibilities:
	#
	""" Modifying .pov files """
	emphasis, list_file_names = my_functions.replacer(DIRECTORY=path)
	#
	#
	""" Getting naming format  """
	# Max number of files (FOR FILE NOMENCLATURE IN FUNCTIONS)
	#  When generating files I want to generate them all
	#  with the same number of characters as string names
	#  for this reason I firstly look for the number of 
	#  files to work with, then I'll know if the 
	#  appropiare nomenclature is 01-99, 001-999, 0001-9999...
	Nfiles = len(list_file_names)
	Ndigit = len(str(Nfiles))
	print('>> Number of digits: {:d}'.format(Ndigit))
	#
	if emphasis in yes_posibilities or emphasis in all_posibilities:
		path = path+'/emphasised'
	""" Generating image files with POVRay """
	my_functions.ImagePOVRay(path , list_file_names , 'y' , Ndigit)
	## ImagePOVRay(path,files,INI_flag,Ndig)
	#
	# Nomenclature system used in the previous function
	#  e.g. crystal_%03d.png = crystal_001.png, crystal_002.png, etc
#
#
if video_GIF in yes_posibilities:
 #	images_id = "im_%0"+str(Ndigit)+"d.png"
	""" Generating video/GIF output of files """
	# Note: in the last flag put 'n', that part is not working yet
	my_functions.videoGeneratorHQ(path,'.png',flag='vg') 
    # add   delay = X   for setting the delay time between images in the gif
	#
print('Finished!')
