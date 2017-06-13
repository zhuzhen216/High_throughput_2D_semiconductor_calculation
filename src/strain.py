
# coding: utf-8

# In[6]:

import atomic_info
import vasp_manager
import os


# In[24]:

def apply_strain(poscar_file,direction=1,strain=0):
    """
    poscar: file path
    direction: 1 (a1), 2(a2), 3(a3), 12(a1+a2), 13(a1+a3), 23(a2+a3), 123(a1+a2+a3)
    strain: can be positive (stretching) or negative (compressing)
    apply_strain modifies poscar_file in place
    """
    poscar = open(poscar_file,'r+')
    poscar_cont = poscar.readlines()
    scale_a1 = 1.0
    scale_a2 = 1.0
    scale_a3 = 1.0
    if direction == 1:
        scale_a1 = 1 + strain
    elif direction == 2:
        scale_a2 = 1 + strain
    elif direction == 3:
        scale_a3 = 1 + strain
    elif direction == 12:
        scale_a1 = 1 + strain
        scale_a2 = 1 + strain
    elif direction == 13:
        scale_a1 = 1 + strain
        scale_a3 = 1 + strain
    elif direction == 23:
        scale_a2 = 1 + strain
        scale_a3 = 1 + strain
    elif direction == 123:
        scale_a1 = 1 + strain
        scale_a2 = 1 + strain
        scale_a3 = 1 + strain
    a1 = [float(poscar_cont[2].split()[i])*scale_a1 for i in range(3)]
    a2 = [float(poscar_cont[3].split()[i])*scale_a2 for i in range(3)]
    a3 = [float(poscar_cont[4].split()[i])*scale_a3 for i in range(3)]
    poscar_cont[0]=str(direction)+' '+str(strain) + ' '+poscar_cont[0]
    poscar_cont[2]= ' '.join(map(str,a1)) + '\n'
    poscar_cont[3]= ' '.join(map(str,a2)) + '\n'
    poscar_cont[4]= ' '.join(map(str,a3)) + '\n'
    poscar.seek(0)
    poscar.truncate()
    poscar.write(''.join(poscar_cont))
    poscar.close()


# In[25]:

' '.join(map(str,[1,2,3]))


# In[27]:

apply_strain('/Users/zhenzhu/GitHub/POSCAR_generation/Notebook/POSCAR_GeS_0',2,0.02)


# In[ ]:




# In[ ]:




# In[ ]:



