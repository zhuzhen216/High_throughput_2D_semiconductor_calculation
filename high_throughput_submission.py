#!/usr/bin/env python
import os
import shutil


# In[4]:

# file1 as CONTCAR
# file2 as POSCAR
# if CONTCAR is a complete file, it usually has longer (or equal)
# length than POSCAR
def compare_file_len(file1,file2):
    f1 = open(file1,'r+')
    f1_content = f1.readlines()
    f2 = open(file2,'r+')
    f2_content = f2.readlines()
    if len(f1_content) >= len(f2_content):
        return True
    else:
        return False


# In[ ]:

#
# copy file1 to file2
#


# In[6]:

folder_dir = '/work/03566/zhuzhen/project/2D_structure'
#folder_lev_one = os.listdir(folder_dir)
folder_lev_one = 'AlBr'
for lev_one_name in folder_lev_one:
    path_lev_one = os.path.join(folder_dir,lev_one_name)
    folder_lev_two = os.listdir(path_lev_one)
    for lev_two_name in folder_lev_two:
        submit_folder = os.path.join(path_lev_one,lev_two_name)
        if ('POSCAR' not in os.listdir(submit_folder)) and ('CONTCAR' not in os.listdir(submit_folder)):
            print('POSCAR does not exist for %s'.format(lev_two_name))
            break
        if ('KPOINTS' not in os.listdir(submit_folder)):
            print('KPOINTS does not exist for %s'.format(lev_two_name))
            break
        if ('POTCAR' not in os.listdir(submit_folder)):
            print('POTCAR does not exist for %s'.format(lev_two_name))
            break
        if ('INCAR' not in os.listdir(submit_folder)):
            print('INCAR does not exist for %s'.format(lev_two_name))
            break
        if 'submit.sh' not in os.listdir(submit_folder):
            print('submit.sh does not exist for %s'.format(lev_two_name))
            break
        if 'CONTCAR' in os.listdir(submit_folder):
            if compare_file_len('CONTCAR','POSCAR'):
                shutil.copy2(os.path.join(submit_folder,'CONTCAR'),os.path.join(submit_folder,'POSCAR'))
        os.system('sbatch '+os.path.join(submit_folder,'submit.sh'))
