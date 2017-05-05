
# coding: utf-8

# In[1]:

import os
import shutil


# In[2]:

# This script can manage the submission of static calculations:
# there are two things to modify:
#
# 1. folder_dir: this is the folder you do high-throughput calculations
#    the folder set-up is: /AlBr/AlBr_0/
#    then, first-step calculation folder: lattice parameters optimized
#    then, static folder: structures optimized with constrained lattice parameters
# 2. the submission file would depend on your own submission system
#    
folder_dir = '/Users/zhenzhu/Project/calculcation/IV-VI/lots_of_struc'


# In[13]:

folder_lev_one = os.listdir(folder_dir)
k_grid = '12 12 1'
for lev_one_name in folder_lev_one:
    lev_two_path=os.path.join(folder_dir,lev_one_name)
    folder_lev_two = os.listdir(lev_two_path)
    for lev_two_name in folder_lev_two:
        lev_three_path = os.path.join(lev_two_path,lev_two_name)
        #os.removedirs(os.path.join(lev_three_path,'static'))
        if 'static' not in os.listdir(lev_three_path):
            os.mkdir(os.path.join(lev_three_path,'static'))
        #
        # copy POSCAR to the new folder 'static'
        #
        POSCAR_path = os.path.join(lev_three_path,'static/POSCAR')
        if 'CONTCAR' in os.listdir(lev_three_path):
            shutil.copy2(os.path.join(lev_three_path,'CONTCAR'),POSCAR_path)
        else:
            shutil.copy2(os.path.join(lev_three_path,'POSCAR'),POSCAR_path)
        shutil.copy2(os.path.join(lev_three_path,'POTCAR'),os.path.join(lev_three_path,'static/POTCAR'))
        ##
        # below, the code will copy the submit.sh file from original folder to the static folder
        # the line containing the submission path in the file is modified.
        # careful, for stampede and guild, it is different
        ##
        submit_path = os.path.join(lev_three_path,'static/submit.sh')
        shutil.copy2(os.path.join(lev_three_path,'submit.sh'),submit_path)
        f_submit = open(submit_path,'r+')
        sub_cont = f_submit.readlines()
        # for guild:
        sub_cont[7]='cd '+lev_three_path+'/static'+'\n'
        # for stampede:
        #sub_cont[-2]='cd '+lev_three_path+'/static'+'\n'
        f_submit.seek(0)
        f_submit.truncate()
        f_submit.write(''.join(sub_cont))
        f_submit.close()
        ##
        # copy KPOINTS to the new folder; increase the k-grid sampling to 12 x 12 x 1
        ##
        KPOINTS_path = os.path.join(lev_three_path,'static/KPOINTS')
        shutil.copy2(os.path.join(lev_three_path,'KPOINTS'),KPOINTS_path)
        f_kpoints = open(KPOINTS_path,'r+')
        kpoints_cont = f_kpoints.readlines()
        kpoints_cont[3]=k_grid+'\n'
        f_kpoints.seek(0)
        f_kpoints.truncate()
        f_kpoints.write(''.join(kpoints_cont))
        f_kpoints.close()
        ##
        # copy INCAR file and modify it.
        ##
        INCAR_path = os.path.join(lev_three_path,'static/INCAR')
        shutil.copy2(os.path.join(lev_three_path,'INCAR'),INCAR_path)
        f_incar = open(INCAR_path,'r+')
        incar_cont = f_incar.readlines()
        # for guild:
        #f_lines[7]='cd '+lev_three_path+'/static'+'\n'
        # for stampede:
        incar_cont[4]='IBRION=2; ISIF=2; NSW=100'+'\n'
        incar_cont.append('\nNEDOS = 3001')
        f_incar.seek(0)
        f_incar.truncate()
        f_incar.write(''.join(incar_cont))
        f_incar.close()


# In[ ]:



