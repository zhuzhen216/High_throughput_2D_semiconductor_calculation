
# coding: utf-8

# ___
# This script is to setup the submission file for the high_throughput calculations.
# The first part is related to the submission file. It depends on the set-up of your own computers.
# Here the example is given using the Stampede supercomputer. The system is slurm.
# folder_dir: this is the folder to run your calculations.
# ___

# In[1]:

import os
import shutil
import numpy


# In[7]:

current_dir = os.getcwd()
#
# folder_dir is your folder to store all your calculations
#
folder_dir = '/Users/zhenzhu/Project/calculcation/IV-VI/lots_of_struc'


# In[12]:

# set up submit.sh file
submit_file=open('submit.sh','w')
submit_file.writelines('#!/bin/bash'+'\n')
submit_file.writelines('# stampede.tacc.utexas.edu: PWD'+'\n')
submit_file.writelines('#SBATCH -J job'+'\n')
submit_file.writelines('#SBATCH -o job.o%j'+'\n')
submit_file.writelines('#SBATCH -p normal'+'\n')
submit_file.writelines('#SBATCH -n 16'+'\n')
submit_file.writelines('#SBATCH -t 24:00:00'+'\n')
submit_file.writelines('#SBATCH --mail-user=zhen_zhu@126.com'+'\n')
submit_file.writelines('#SBATCH -A TG-DMR070072N'+'\n')
submit_file.writelines('module swap intel intel/14.0.1.106'+'\n')
submit_file.writelines('module swap mvapich2 impi/4.1.3.049'+'\n')
submit_file.writelines('cd $SLURM_SUBMIT_DIR'+'\n')
submit_file.writelines('ibrun $HOME/bin/vasp.541_p3.stampede'+'\n')
submit_file.close()


# In[15]:

# copy the submit.sh file to each foler
folder_lev_one = os.listdir(folder_dir)
for lev_one_name in folder_lev_one:
    lev_two_path=os.path.join(folder_dir,lev_one_name)
    folder_lev_two = os.listdir(lev_two_path)
    for lev_two_name in folder_lev_two:
        to_folder = os.path.join(lev_two_path,lev_two_name)
        shutil.copy2(os.path.join(current_dir,'submit.sh'), to_folder)
        submit_file=open(os.path.join(to_folder,'submit.sh'),'r+')
        f_content = submit_file.readlines()
        #print(f_content)
        #change = '#SBATCH -J '+lev_two_name+'\n'
        f_content[2]= '#SBATCH -J '+lev_two_name+'\n'
        submit_file.seek(0)
        submit_file.truncate()
        submit_file.write(''.join(f_content))
        submit_file.close()


# In[ ]:



