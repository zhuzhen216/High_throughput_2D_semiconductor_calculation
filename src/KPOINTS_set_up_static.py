
# coding: utf-8

# In[7]:

import os
import numpy as np
import shutil


# In[2]:

# obtain the path of current folder
# also give the destination folder
current_dir = os.getcwd()
folder_dir = '/Users/zhenzhu/Project/calculcation/IV-VI/lots_of_struc'


# In[4]:

# set up KPOINTS file in current folder
# k-points
# 0
# M
# 12  12  1
# 0  0  0
# this KPOINTS are selected for 2D structure calculations
#
def set_KPOINTS(kx,ky,kz,shifted=False):
    filename = 'KPOINTS'
    kx_ky_kz = '\t'.join([str(kx),str(ky),str(kz)])
    if shifted:
        shift = '\t'.join([str(0.5),str(0.5),str(0.5)])
    else:
        shift = '\t'.join([str(0),str(0),str(0)])
    f_kpoints = open(filename,'w')
    f_kpoints.writelines('k-points')
    f_kpoints.writelines('\n')
    f_kpoints.writelines('0\n')
    f_kpoints.writelines('M\n')
    f_kpoints.writelines(kx_ky_kz+'\n')
    f_kpoints.writelines(shift)
    f_kpoints.close()
set_KPOINTS(12,12,1)


# In[8]:

# KPOINTS file is generated
# copy the KPOINTS file to destination folder: folder_dir
folder_lev_one = os.listdir(folder_dir)
for lev_one_name in folder_lev_one:
    lev_two_path=os.path.join(folder_dir,lev_one_name)
    folder_lev_two = os.listdir(lev_two_path)
    for lev_two_name in folder_lev_two:
        lev_three_path = os.path.join(lev_two_path,lev_two_name)
        #os.removedirs(os.path.join(lev_three_path,'static'))
        if 'static' not in os.listdir(lev_three_path):
            os.mkdir(os.path.join(lev_three_path,'static'))
        shutil.copy2(os.path.join(current_dir,'KPOINTS'),os.path.join(lev_three_path,'static'))

