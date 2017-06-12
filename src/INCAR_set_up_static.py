
# coding: utf-8

# In[3]:

import os
import shutil
import numpy as np


# In[4]:

current_dir = os.getcwd()
folder_dir = '/Users/zhenzhu/Project/calculcation/IV-VI/lots_of_struc'


# In[9]:

#
# INCAR file as following
#
#System = blackp
#ISMEAR = 0
#SIGMA = 0.1;
#ENCUT = 500
#IBRION=2; ISIF=3 ; NSW=100
#NELM = 200
#EDIFF  = 0.1E-05
#EDIFFG = -0.01
#NEDOS = 3001
# the folder to do static calculations are created to be static
def set_INCAR():
    filename = 'INCAR'
    f_incar = open(filename,'w')
    f_incar.writelines('System = 2D Structure'+'\n')
    f_incar.writelines('ISMEAR = 0'+'\n')
    f_incar.writelines('SIGMA = 0.1'+'\n')
    f_incar.writelines('ENCUT = 500'+'\n')
    f_incar.writelines('IBRION=2; ISIF=2; NSW=100'+'\n')
    f_incar.writelines('EDIFF  = 0.1E-05'+'\n')
    f_incar.writelines('EDIFFG = -0.01'+'\n')
    f_incar.writelines('NEDOS = 3001')
    f_incar.close()
set_INCAR()


# In[13]:

folder_lev_one = os.listdir(folder_dir)
for lev_one_name in folder_lev_one:
    lev_two_path=os.path.join(folder_dir,lev_one_name)
    folder_lev_two = os.listdir(lev_two_path)
    for lev_two_name in folder_lev_two:
        lev_three_path = os.path.join(lev_two_path,lev_two_name)
        #os.removedirs(os.path.join(lev_three_path,'static'))
        if 'static' not in os.listdir(lev_three_path):
            os.mkdir(os.path.join(lev_three_path,'static'))
        shutil.copy2(os.path.join(current_dir,'INCAR'),os.path.join(lev_three_path,'static'))


# In[ ]:



