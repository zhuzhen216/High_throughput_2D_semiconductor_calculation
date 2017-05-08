
# coding: utf-8

# In[2]:

import os
import shutil
import atomic_info


# In[3]:

def oszicar_not_complete(file):
    file_open=open(file,'r')
    file_cont=file_open.readlines()
    if 'F=' not in file_cont[-1].split():
        return True
    else:
        return False


# In[4]:

folder_dir = '/home/zhuzhen/2D_structure'
util_path = '/home/zhuzhen/util'
macroave_path = util_path + '/macroave'
vasp2abi_path = util_path + '/locpot_vasp2abinit_z'
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
        lev_three_path = os.path.join(lev_two_path,lev_two_name+'/static/Align')
        if 'OSZICAR' not in os.listdir(lev_three_path):
            print('Alignment calculation not successful for {}'.format(lev_two_name))
            break
        oszicar_path = lev_three_path + '/OSZICAR'
        if oszicar_not_complete(oszicar_path):
            print('Alignment calculation not successful for {}'.format(lev_two_name))
            break
        elem_in_compound = atomic_info.count_elem(lev_one_name)
        # create input "compound.info" for locpot_vasp2abinit_z
        compound_info_open = open(lev_three_path+'/compound.info','w')
        for elem_name in elem_in_compound:
            compound_info_open.writelines(str(atomic_info.element.atomic_number[elem_name])+'\n')
        compound_info_open.writelines(str(1))
        compound_info_open.close()
        # create submit file for "vasp2abi"
        vasp2abi_sub_open = open(lev_three_path+'/vasp2abi_sub.sh','w')
        vasp2abi_sub_open.writelines('#!/bin/bash\n')
        vasp2abi_sub_open.writelines('cd '+lev_three_path+'\n')
        vasp2abi_sub_open.writelines(vasp2abi_path)
        vasp2abi_sub_open.close()
        os.system('qsub '+lev_three_path+'/vasp2abi_sub.sh')


# In[ ]:



