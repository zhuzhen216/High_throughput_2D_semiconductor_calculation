
# coding: utf-8

# In[2]:

import os
import shutil
import atomic_info


# In[3]:

def oszicar_not_complete(file):
    file_open=open(file,'r')
    file_cont=file_open.readlines()
    if len(file_cont)<5:
        return True
    if 'F=' not in file_cont[-1].split():
        return True
    else:
        return False


# In[1]:

def dan_empty(file):
    file_open=open(file,'r')
    file_cont=file_open.readlines()
    if len(file_cont)<5:
        return True
    else:
        return False


# In[4]:

folder_dir = '/home/zhuzhen/2D_structure'
util_path = '/home/zhuzhen/util'
macroave_path = util_path + '/macroave'
#vasp2abi_path = util_path + '/locpot_vasp2abinit_z'
macroave_in_path = util_path + '/macroave.in'
#lev_two_name='a'
#print('Alignment calculation not successful for {}'.format(lev_two_name))
#atomic_info.count_elem('Bi')


# In[5]:

folder_lev_one = os.listdir(folder_dir)
for lev_one_name in folder_lev_one:
    lev_two_path = os.path.join(folder_dir,lev_one_name)
    folder_lev_two = os.listdir(lev_two_path)
    for lev_two_name in folder_lev_two:
        if 'static' not in os.listdir(lev_two_path+'/'+lev_two_name):
            print(lev_two_name + ' not completed')
            break
        static_path = lev_two_path+'/'+lev_two_name+'/static'
        if 'Align' not in os.listdir(static_path):
            print(lev_two_name+' not completed')
            break
        lev_three_path = os.path.join(lev_two_path,lev_two_name+'/static/Align')
        if 'OSZICAR' not in os.listdir(lev_three_path):
            print('Alignment calculation not successful for '+lev_two_name)
            break
        oszicar_path = lev_three_path + '/OSZICAR'
        if oszicar_not_complete(oszicar_path):
            print('Alignment calculation not successful for '+lev_two_name)
            break
        dan_path = lev_three_path + '/dan.out'
        if dan_empty(dan_path):
            print('Alignment step 1 not successful for '+lev_two_name)
            break
        # copy "macroave.in" to the folder
        #
        shutil.copy2(macroave_in_path,lev_three_path)
        # create submit file for "macroave"
        #
        macroave_sub_open = open(lev_three_path+'/macroave_sub.sh','w')
        macroave_sub_open.writelines('#!/bin/bash\n')
        macroave_sub_open.writelines('cd '+lev_three_path+'\n')
        macroave_sub_open.writelines(macroave_path)
        macroave_sub_open.close()
        os.system('qsub '+lev_three_path+'/macroave_sub.sh')


# In[ ]:



