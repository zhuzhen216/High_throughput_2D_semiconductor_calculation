
# coding: utf-8

# ___
# This script is to setup the submission file for the high_throughput calculations.
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


# In[1]:

# set up submit.sh file
submit_file=open('submit.sh','w')
submit_file.writelines('#!/bin/bash'+'\n')
submit_file.writelines('# stampede.tacc.utexas.edu: PWD'+'\n')
submit_file.writelines('#PBS -N job'+'\n')
submit_file.writelines('#PBS -l nodes=1:ppn=8'+'\n')
submit_file.writelines('#PBS -l walltime=48:00:00'+'\n')
submit_file.writelines('#PBS -j oe'+'\n')
submit_file.writelines('#PBS -V'+'\n')
submit_file.writelines('\n')
submit_file.writelines('cd $PBS_O_WORKDIR'+'\n')
submit_file.writelines('source /usr/local/intel/composer_xe_2013.5.192/bin/compilervars.sh intel64'+'\n')
submit_file.writelines('source /usr/local/intel/composer_xe_2013.5.192/mkl/bin/mklvars.sh intel64'+'\n')
submit_file.writelines('export PATH=/usr/local/openmpi-1.6.4/bin:$PATH'+'\n')
submit_file.writelines('export LD_LIBRARY_PATH=/usr/local/openmpi-1.6.4/lib:$LD_LIBRARY_PATH'+'\n')
submit_file.writelines('ulimit -s unlimited'+'\n')
submit_file.writelines('/usr/local/openmpi-1.6.4/bin/mpirun -np 8 -machinefile $PBS_NODEFILE /home/vandewalle/codes/guild/VASP/vasp.541_p3.guild')
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



