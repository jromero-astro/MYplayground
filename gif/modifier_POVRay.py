import os
import sys
import numpy as np

###############################################################################
"""
USEFULL INFO
#
# Emphasising only works if initial POVRay files are made 
#  using STICK geometry for atoms (option available 
#  f.ex. in MOLDRAW).
#  (Not tested with other molecular visualizers)
#
# This script works entirely from terminal. Tested
#  with python 2.7 ubuntu 14. The script can be stored in 
#  a different directory than the one where you
#  want to run it (so you can call it remotely),
#  for example you can put it in "~/scripts" and 
#  run it from wherever like "python ~/scripts/name.py".
#
#  Then it will ask the path to your POVRay files
#  (e.g. ~/work/my_system/pov_files) and the 
#  atomic labels (according to MOLDRAW) to
#  be used (e.g. N125 C43 H387) put it in a single
#  string separated by spaces only. 
#
#  Finally you will find the new data files inside a new 
#   directory. Recalling the previous example:
#   it will be at "~/work/my_system/pov_files/emphasised"
"""
#----------------------------------------------------------------------------

yes_posibilities = ['y','yes','Y','Yes','YES']
all_posibilities = ['all','a','All','ALL','All']

#### FUNCTION FOR TERMIANL PROGRESS BAR #### #Not used, but nice function
# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', 
			decimals = 1, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '/' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()
#----------------------------------------------------------------------------
def NameMod(DIRECTORY,start): # not used here, but useful function
    
    path, dirs, files = next(os.walk(DIRECTORY)) 
    # saving in strings the dir content
    listfilenames = []
    for file in files:
        if '.pov' in file:
            listfilenames.append(file)
    
    new_dir = DIRECTORY+'/renamed'
    os.system('mkdir '+new_dir)
    
    for k,file in enumerate(listfilenames):
        name,extension = file.split('.')
        letter,numbers = name.split('_')
        numbers = int(numbers) + int(start) # change the number
        new_name = letter+'_'+str(numbers)+'.'+extension
        os.system('cp '+DIRECTORY+'/'+file+' '+new_dir+'/'+new_name)
        printProgress (iteration=k+1, total=len(listfilenames), 
			prefix = 'Progress', suffix = 'Completed', 
					decimals = 1, barLength = 50)
    print('Finished')

def int_or_letter(list): 
    # used in fileModifier function, for separating
    #  the letters from the numbers that have to be used in the 
    #  pov files. Example: H15 --> H,15
    letters,numbers=[],[]
    for i in list:
        try: int_value = int(i)
        except ValueError: letters.append(str(i))
        else: numbers.append(str(int_value))
    return str(''.join(letters)),int(''.join(numbers)) 
    # separates letters and digits in any string into 2 lists

def fileModifier(data2,atomLIST): # used in replacer function
    #AtomType_and_Nnumber = []
    for atom_label in atomLIST:
        atom_type,atom_num = int_or_letter(list(atom_label))
        for i,line in enumerate(data2):
            if '//Atom number:' in line and atom_num == int(line.split(':')[1]):
                data2[i+1] = data2[i+1].split('>,')[0]+'>,Radius_'+atom_type+'\n'
    return data2
def last(list):
    return list[-1]
def getAtomLabels(fileREAD): 
    # used in replacer function. It looks for the atomic 
    #  labels in the .pov file (only if pov was made with Moldraw)
    labels = []
    for i,line in enumerate(fileREAD):
        if "//Atom number:" in line and "texture{pigment{color Color_" in fileREAD[i+2]:
            numb = int(line.split(':')[1])
            line2 = fileREAD[i+2]
            p1, p2 = line2.find('Color_'), line2.find('} finish')
            typeOfAtom = line2[p1:p2].split('_')[1].split('}')[0]
            labels.append(str(typeOfAtom)+str(numb))
    string = " ".join(labels )
    #print('>> Labels: {}'.format(string))
    return string

   
#----------------------------------------------------------------------------
###############################################################################
############ MODIFYING .pov FILES IN ORDER TO MAKE NICE FIGURES ###############
###############################################################################
"""
This function is thought to perform changes in the .pov files that are generated
with MOLDRAW. You can generate .pov files from a opt process and use them to 
make figures with POVRay and  afterwards you can make even videos or gif files.
the changes that this function perform are minimal. It changes some colors and
sizes in order to make fancy figures. There is a cool thing you can do with this
funciton: If you generate the .pov with stick-like atoms & links then this function
can change some of the atoms to be solid-like, so you gain enphasis in the atoms 
you want. Everythong is explained in the code itself and is screened to the user
during the excecution. Just follow them. 
"""
def replacer(DIRECTORY):

    ################### Modify if necessary ###################
    fileReplacement = open('/home/jromero/scripts/linesToModPOVRAY.dat','r')
    ###########################################################

    emphasis = raw_input('>> Emphazise RX atoms?\n   (y/n/all): ')
    # Emphasis will make the picture look great (only if input are Stick-like)
    #e.g.: DIRECTORY = 'ch3_hco_opt_sticks'
    replacement = fileReplacement.readlines()
    fileReplacement.close()
    #--------------------------------------------------------------------------
    # Searching files in work directory 
    while 1:
        dir_path, dirs, files = next(os.walk(DIRECTORY))
        listfilenames=[ i for i in files if '.pov' == i[-4:] ]
        if listfilenames==[]: print('No .pov files found, try again.')
        else: break
    print('>> {:d} .pov files found'.format(len(listfilenames)))
    #--------------------------------------------------------------------------        
    if emphasis in yes_posibilities: # Ex. H255 C252 goes to: [H255,C252]
        atomLIST = raw_input('>> ATOM LABELS (caps) to emphasize, separated by SPACE\n   -->  ').split()
    elif emphasis in all_posibilities:
        for file2 in listfilenames:
            with open(file2,'r') as file1:
                atoms = getAtomLabels([i for i in file1])
            atomLIST = atoms.split()
    else: atomLIST = []
    #-------------------------------------------------------------------------- 
    print('>> Modifying .pov files...')

    for j, filename in enumerate(listfilenames):
        #data = []
        datanew,data = [],[]
        with open(DIRECTORY+'/'+filename,'r') as file2:
            for k,line in enumerate(file2):
                if 'phong .9}' in line:   start = k
                elif 'camera{'   in line:   end = k
                data.append(line) # I use 'phong .9}' and 'camera{' as flags to point where do I have to modify the properties
        data1 = data[:start-1]
        data2 = data[end+1:] 
        del(data)
        for line in data2:
            if 'background {' in line:  data2.remove(line) #removing background
        # Modifying atom sizes
        if emphasis in yes_posibilities or emphasis in all_posibilities:
            data2 = fileModifier(data2,atomLIST) # I modify the 2nd part where objects to plot are specified
        datanew = data1
        datanew.extend(replacement)
        datanew.extend(data2)
        if os.path.exists(DIRECTORY+'/emphasised') != True:
            os.system('mkdir '+DIRECTORY+'/emphasised')
        with open(DIRECTORY+'/emphasised/'+filename,'w') as file_out:
            for line in datanew:
                file_out.write(str(line))
        printProgress (j+1, total=len(listfilenames), prefix = 'Progress:', 
			suffix = 'Complete', decimals = 1, barLength = 50)        
    #--------------------------------------------------------------------------
    print('>> Finished. New POVRay files in:\n>> '+DIRECTORY+'/emphasised')
    return emphasis, listfilenames
###############################################################################
############# IMAGE & VIDEO GENERATION, USING POVRay & ffmpeg #################
###############################################################################

"""
INSTALL POVRAY: for linux you have to go to the official webpage (just google it)
    and look for the GitHub link for unix systems. Then just untar (or unzip)
    the downloaded file, get in and run the 'install' script: 
        $ ./install
Maybe it will ask you to run the script without checking the directory tree,
I did it and for me worked (Ubuntu 14.04 LTS).
#
POV-Ray command line summary: in bash just type: 
    1. povray name.INI
    2. povray +Iinfile.pov <options>
        (.INI files are scripts for command line povray)
1--------------------------------------------------------------------------
In .ini files one can specify lots of options. For them, the ; symbol
is the comment flag (like # in python). 
In general you will only use teh .INI to set the name of the input file with: 
     >> Input_File_Name=simple.pov
the name of output file with: 
    >> Output_to_File=off.pov
the resolution with: 
    >> +W80 +H60; width and height in pixels 
for moldraw the max recommended is +W1600 +H1200.
You can set different options just using squared brackets, for example:
    name.INI >>
          Input_File_Name = simple.pov
          [Low]
          +W80 +H60    
          [Med]
          +W320 +H200
then in terminal you only have to type: 
    $ povray name.INI[Low] 
to select that option. 
Example @: http://www.povray.org/documentation/view/3.6.2/56/
You can concatenate sevaral .INI files
#
2--------------------------------------------------------------------------
Of course you can decide to not use .INI and put all options in command
line like: 
    $ povray +I input.pov +W80 +H60
There are more options for both command line and .INI files, just google
them or go to the official POV-Ray webpage www.povray.org
#
I ususally use:
    $ povray name.INI
or
    $ povray name.INI +Iinput.pov +D +X +A +FN
    --> +Iinput.pov understands the +I is a flag and input.pov is the file
    --> +D = display; +X = 

    --> +FN says that output is a PNG. +F says you want an output.
        Change the N by ___ for ___: 
                         C      (Compressed targa file)
                         P      (PPM file)
                         S      (Syst specific file, like Mac Pic or BMP)
                         T      (Uncompressed targa file)
        See: http://www.povray.org/documentation/view/3.6.1/219/
If you add +V (verbose) it will output the process in the terminal.
#
All +? entries are switches, which mark the kind of option, but have a plus
functionality in comparison with bash flags: all + signs can be changed 
to - signs, then you will be telling povray to not activate that 
option (that's why they are switches).
More info:
    http://www.povray.org/documentation/view/3.6.1/219/
    http://www.povray.org/documentation/view/3.6.1/55/
INSTALATION tutorial: http://www.povray.org/download/linux.php
"""
#----------------------------------------------------------------------------
def INIFile_creator(path,INIfileName,povFile_name,image_name): # used in ImagePOVRay
    """
    Generates a .INI file with some options, you can see them below.
    This funciton can be modified and improved depending on your necessities.
    Useful info: http://www.povray.org/documentation/view/3.6.1/219/
    """
    if last(list(path)) == '/': path = path[:len(path)-2]
    #inFILE_name = path+'/'+inFILE_name
    #outFILE_name = path+'/'+outFILE_name
    outFILE = open(INIfileName,'w')
    #### joan's selection    
    outFILE.write('Input_File_Name='+povFile_name+'; Input pov file name\n')
    outFILE.write('Output_File_Name='+image_name+'; Output image file name\n')
    outFILE.write('Output_File_Type=N ; output file type is PNG \n')
    # Change Output_File_Type=N to another format (N = PNG)
    outFILE.write('+W1600 +H1200; best resolution, slow computation\n')
    outFILE.write('Output_Alpha=On\n')
    outFILE.write('Antialias=On\n')
    outFILE.write('Antialias_Threshold=0.3 ; untill here 1600x1200 AA 0.3\n')
    outFILE.write('Display=Off ; not showing windows during rendering\n')
    #outFILE.write('Debug_Console=Off ; not showing text in terminal\n')
    #outFILE.write('Fatal_Console=Off ; not showing text in terminal\n')
    #outFILE.write('Statistic_Console=Off ; not showing text in terminal\n')
    #outFILE.write('Warning_Console=Off ; not showing text in terminal\n')
    #outFILE.write('Verbose=Off ; not showing text in terminal\n') 
    outFILE.write('All_Console=Off ; not showing text in terminal\n')
    outFILE.write('All_File=false ; text output in external file\n')  
    # Add more lines if necessary
    outFILE.close()
    return INIfileName
#----------------------------------------------------------------------------    
def ImagePOVRay(path,files,INI_flag,Ndig):
    """
    This will call povray in your system and will generate the figures
    from the .pov files.
        path --> tell where are placed your .pov files
        files --> a list with the names of your files
        INI --> 'y' or 'n': do you have a .INI file?
        INI_file --> if 'y' then type the name of this file (with its path)
                 --> if 'no' then just write ""
    """
    yes_posibilities = ['y','yes','Y','Yes','YES']
    if path[-1] == '/': 
        path = path[:len(path)-2]
    #raw_input('>> POVRay is about to start. Type ENTER to continue: ')
    for k, file in enumerate(files):
        name = file.split('.')[0]
        num = int(name.split('_')[1])
        if ' ' in name: name.replace (" ", "_") # povray doesn't understand whitespaces for output
        file = path+'/'+file
        #............................
        out = ('im_{:0{:d}d}.png'.format(num, Ndig))
        # images must have a leading zero for imagemagik to work
        #...........................
        if INI_flag in yes_posibilities:
            INI_file = INIFile_creator(path,'mypovray.INI',file,out)
	    # using INIFile_creator(path,INIfileName,povFile_name,image_name,out_type='N')
            os.system('povray {}'.format(INI_file))
            # If your .INI has options (advanced users only) please select them putting the 
            #  selection between squared bracket ([]) after INI_file
        else: # my standard
            os.system("povray +I -GA {} +O {} -D +X +A +FN".format(file,out))
            # -GA should avooid pov ray to show up in the console
#----------------------------------------------------------------------------
def videoGeneratorHQ(path,image_ext,flag,delay = 10):
    print('\n############# GENERATING THE VIDEO/GIF ################\n')
    #--------------------------------------------
    # 1st find image files
    dir_path, dirs, files = next(os.walk(path))
    list_file_names=[]
    for file in files:
        if image_ext in file:
            list_file_names.append(file)
    if  list_file_names == []: 
        print('No '+image_ext+' files found, try again.')
    Nfiles = len(list_file_names)
    Ndigit = len(str(Nfiles))
    images_id = "im_%0"+str(Ndigit)+"d.png"
    #--------------------------------------------
    video_posibilities = ['v','V','gv','vg','GV','VG']
    gif_posibilities = ['g', 'G', 'gv','vg','GV','VG']
    #--------------------------------------------
    #--------------------------------------------
    # 2nd the video is generated
    # Using ffmpeg for video generation
    #if flag in video_posibilities:
	#print('#### Making the video...')
        #os.system('ffmpeg -r 25 -qscale 2 -i '+images_id+' -vcodec png output.mov')
    # You can use <<... -vcodec png output.mov>>; <<... -vcodec png output.mov>>;
    # <<... -vcodec ffvhuff output.avi>>; <<... -vcodec huffyuv output.avi>>;
    # <<... output.mp4(.avi)(.mov)(...)>>>
    """"
    Is just a command line. You have to install the package previously
     in your Linux machine (check webpage). Below you can find a simple
     explanation & example from webpage:
     << http://www.itforeveryone.co.uk/image-to-video.html >>
    Ex: $ ffmpeg -r 25 -qscale 2 -i %05d.morph.jpg output.mp4
     ffmpeg can be used to stitch several images together into a video. 
     There are many options, but the following example should be enough 
     to get started. It takes all images that have filenames of 
     XXXXX.morph.jpg, where X is numerical, and creates a video 
     called "output.mp4". The qscale option specifies the picture 
     quality (1 is the highest, and 32 is the lowest), and the "-r" 
     option is used to specify the number of frames per second.
    """
    # 3rd a gif is built (preserves alpha channels = transparencies)
    #  install imagemagick:
    #   http://www.imagemagick.org/download/ImageMagick.tar.gz
    #   follow http://www.imagemagick.org/script/binary-releases.php
    #   except for the test, for that get into the folder opened
    #   when untaring and run the test you'll find in QuickStart.txt 
    #   then you are ready to run imagemagick (it makes gifs, softens 
    #   the image... (is computationally expensive).
    if flag in gif_posibilities:
	print('#### Making the GIF...')
        images_id = str(images_id.split('%')[0])+'*.png'
        os.system('convert -delay {:f} -loop 0 -dispose 3 -coalesce {} output.gif'.format(delay, images_id)) # loop forever is -loop 0
        print('Done!')
    #--------------------------------------------
    #--------------------------------------------
    # Code for making gifs with python 
    # From http://imageio.readthedocs.io/en/latest/installation.html
    # NOT WORKING FOR ME.... you will need the packages imageio, pillow (PIL)
    #  and having istalled the ffmpeg app in your Unix     
    #
    #import imageio 
    #with imageio.get_writer('movie.gif', mode='I', format='GIF-PIL') as writer:     
    #    for filename in list_file_names:
    #        image = imageio.imread(filename)
    #        writer.append_data(image) 

 
