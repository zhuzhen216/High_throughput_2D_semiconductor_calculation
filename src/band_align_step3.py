
# coding: utf-8

# In[1]:

import os
import shutil
import atomic_info


# In[2]:

def oszicar_not_complete(file):
    file_open=open(file,'r')
    file_cont=file_open.readlines()
    if len(file_cont)<5:
        return True
    if 'F=' not in file_cont[-1].split():
        return True
    else:
        return False


# In[3]:

def MAV_empty(file):
    file_open=open(file,'r+')
    file_cont=file_open.readlines()
    if len(file_cont)<5:
        return True
    else:
        return False


# In[5]:

def dan_empty(file):
    file_open=open(file,'r')
    file_cont=file_open.readlines()
    if len(file_cont)<5:
        return True
    else:
        return False

def ave_n_val(energy_list,n):
    list_ave_n = []
    if len(energy_list)<n:
        return sum(energy_list)/n
    for i in range(len(energy_list)-n+1):
        list_ave_n.append(sum(energy_list[i:i+n])/n)
    return max(list_ave_n)

# In[4]:

folder_dir = '/home/zhuzhen/2D_structure'
vac_level = open('VAC_lev.dat','w')


# In[5]:

folder_lev_one = os.listdir(folder_dir)
for lev_one_name in folder_lev_one:
    lev_two_path = os.path.join(folder_dir,lev_one_name)
    folder_lev_two = os.listdir(lev_two_path)
    for lev_two_name in folder_lev_two:
        MAV_z = []
        MAV_energy = []
        if 'static' not in os.listdir(lev_two_path+'/'+lev_two_name):
            print(lev_two_name + ' static calc not completed')
            break
        static_path = lev_two_path+'/'+lev_two_name+'/static'
        if 'Align' not in os.listdir(static_path):
            print(lev_two_name+' alignment not completed')
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
        MAV_path = lev_three_path + '/txo_VASP_POT.MAV'
        # check align_step2
        #
        if MAV_empty(MAV_path):
            print('Alignment step 2 not successful for '+lev_two_name)
            break
        # start read MAV_file:
        MAV_open = open(MAV_path,'r')
        MAV_cont = MAV_open.readlines()
        for line in MAV_cont:
            MAV_z.append(float(line.split()[0]))
            MAV_energy.append(float(line.split()[0]))
        if MAV_z[-1]<15:
            print('Z distance too small for '+lev_two_name)
            break
        #vac_level.writelines(lev_two_name + ' ' + str(max(MAV_energy)) + '\n')
        vac_level.writelines(lev_two_name + ' ' + str(max(MAV_energy)) + ' ' + str(ave_n_val(MAV_energy,20))+'\n')
vac_level.close()


# In[ ]:



