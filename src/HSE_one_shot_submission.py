
# coding: utf-8

# In[1]:

import os
import numpy
import shutil


# In[2]:

# KPOINTS: 12 by 12 by 1
# different INCAR file
#
# rules: first copy, then modify the files, then submit all the jobs


# In[12]:

# modify INCAR file:
# "the path of submission folder + INCAR" should be given as the input
# INCAR file will be created in the submit_folder
def create_INCAR(submit_folder):
    incar_open = open(submit_folder+'/INCAR','w')
    incar_open.writelines('LREAL = .FALSE.\nENCUT = 400\nALGO = All\nEDIFF = 1e-5\n')
    incar_open.writelines('EDIFFG = -0.02\nLVHAR = .TRUE.\nIBRION = 2\nISIF = 2\nNSW = 0\n')
    incar_open.writelines('GGA_COMPAT = F\nNELM = 200\nNELMIN = 5\nLASPH = .TRUE.\nISMEAR = -5\n')
    incar_open.writelines('LHFCALC = .TRUE.\nAEXX = 0.25\nHFSCREEN = 0.2\nPRECFOCK = Fast\nLORBIT = 10\nISYM=2')
    incar_open.close()
#modify_INCAR('/Users/zhenzhu/GitHub/POSCAR_generation/test_incar')


# In[8]:

# copy CHGCAR or INCAR or POSCAR or KPOINT or submit file:
# from_path: /path/CHGCAR
# to_folder: the folder to do calculations
def copy_FILE(from_path,to_folder):
    shutil.copy2(from_path,to_folder)


# In[9]:

def modify_submit(submit_folder):
    f_submit = open(submit_folder+'/submit.sh','r+')
    sub_cont = f_submit.readlines()
    # for guild:
    sub_cont[7]='cd '+submit_folder+'\n'
    # for stampede:
    #sub_cont[-2]='cd '+lev_three_path+'/static'+'\n'
    f_submit.seek(0)
    f_submit.truncate()
    f_submit.write(''.join(sub_cont))
    f_submit.close()


# In[10]:

def file_empty(file):
    file_open=open(file,'r')
    file_cont=file_open.readlines()
    if len(file_cont)<5:
        return True
    else:
        return False


# In[11]:

#
# the home folder to conduct all the calculations
#
folder_dir = '/home/zhuzhen/2D_structure'


# In[ ]:

# HSE_path is the submission folder
folder_lev_one = os.listdir(folder_dir)
for lev_one_name in folder_lev_one:
    lev_two_path=os.path.join(folder_dir,lev_one_name)
    folder_lev_two = os.listdir(lev_two_path)
    for lev_two_name in folder_lev_two:
        lev_three_path = os.path.join(lev_two_path,lev_two_name)
        if 'static' not in os.listdir(lev_three_path):
            print('Static calculation first for %s!'.format(lev_two_name))
            break
        # create folder for HSE calculation under 'static' folder
        static_path = lev_three_path+'/static'
        HSE_path = static_path+'/HSE'
        os.makedir(HSE_path)
        #
        # create INCAR file in HSE_path
        #
        #
        create_INCAR(HSE_path)
        #
        # copy POTCAR file
        #
        copy_FILE(static_path+'/POTCAR',HSE_path)
        #
        # copy KPOINTS file, KPOINTS kept as the same as static
        #
        copy_FILE(static_path+'/KPOINTS',HSE_path)
        #
        # cp CONTCAR file to POSCAR file
        #
        if file_empty(static_path+'/CONTCAR'):
            print('Static calculation not performed correctly for %s!'.format(lev_two_name))
            break
        copy_FILE(static_path+'/CONTCAR',HSE_path+'/POSCAR')
        #
        # copy submit.sh
        #
        copy_FILE(static_path+'/submit.sh',HSE_path)
        modify_submit(HSE_path)
        #
        # no need to copy CHGCAR file for HSE calculation
        #
        os.system('qsub '+HSE_path+'/submit.sh')

