
# coding: utf-8

# In[140]:

import os
import shutil
import numpy
import matplotlib.pyplot as plt
import math
#get_ipython().magic('matplotlib inline')


# In[206]:

class element:
    GroupIII = ['B','Al','Ga','In']
    GroupIV = ['C','Si','Ge','Sn','Pb']
    GroupV = ['N','P','As','Sb','Bis']
    GroupVI = ['O','S','Se','Te']
    GroupVII = ['F','Cl','Br','I']
    atomic_mass={'B':10.811,'Al':26.5815,'Ga':69.723,'In':114.818,'C':12.0107,'Si':28.0855,'Ge':72.61,'Sn':118.710,'Pb':207.2,'N':14.0067,'P':30.9738,'As':74.9216,'Sb':121.76,'Bis':208.58,'O':15.9994,'S':32.066,'Se':78.96,'Te':127.60,'F':18.9984,'Cl':35.4527,'Br':79.504,'I':126.90447}
    atomic_radius = {'B':87,'Al':118,'Ga':138,'In':156,'C':67,'Si':111,'Ge':125,'Sn':145,'Pb':154,'N':56,'P':98,'As':114,'Sb':133,'Bis':143,'O':48,'S':88,'Se':103,'Te':123,'F':42,'Cl':79,'Br':94,'I':115}


# In[207]:

class structure_and_lattice:
    compare_radius = 98
    # black phosphorus, blue phosphorus, SiS structure
    frac=[[(0.75,0.5997,0.2229),(0.25,0.0997,0.0718),(0.25,0.014384,0.2094),(0.75,0.5144,0.0854)],[(0.0,0.0,0.0113),(0.333,0.333,-0.05132)],[(0.0,0.25,0.5785),(0.5,0.75,0.42152),(0.,0.25,0.41),(0.5,0.75,0.59)]]
    lattice = [[(3.348,0.,0.),(0.,4.623,0.),(0.,0.,20.)],[(2.881076913,-1.662861501,0.0),(2.881077039,1.662861720,0.0),(0.0,0.0,20.)],[(3.6,0,0),(0,3.6,0),(0,0,20)]]
    lattice_sites = [4,2,4]
    phase = [0,1,2]


# In[208]:

# initialize all the possible compounds
compound_III_VII = []
for char1 in element.GroupIII:
    for char2 in element.GroupVII:
        compound_III_VII.append(char1+char2)
compound_IV_VI = []
for char1 in element.GroupIV:
    for char2 in element.GroupVI:
        compound_IV_VI.append(char1+char2)
elem_V = element.GroupV
compound_all = elem_V+compound_III_VII+compound_IV_VI
compound_phase = {}
for compound in compound_all:
    compound_phase[compound]=[compound+'_'+str(structure_and_lattice.phase[i]) for i in range(len(structure_and_lattice.phase))]
#compound_phase


# In[209]:

# given a certain compound, count how many elements in this compound
# return the element name in a list
def count_elem(compound):
    num_upper = sum(1 for char in compound if char.isupper())
    if num_upper == 1:
        if compound in element.GroupV:
            return [compound]
        else:
            print('The compound is not correct! Please input V, IV-VI, or III-VII only!')
            return None
    i = 1
    while not compound[i].isupper():
        i = i + 1
    if (compound[0:i] in element.GroupIII and compound[i:] not in element.GroupVII) or (compound[0:i] in element.GroupVII and compound[i:] not in element.GroupIII):
        print('The compound is not correct! Please input V, IV-VI, or III-VII only!')
        return None
    elif (compound[0:i] in element.GroupIV and compound[i:] not in element.GroupVI) or (compound[0:i] in element.GroupVI and compound[i:] not in element.GroupIV):
        print('The compound is not correct! Please input V, IV-VI, or III-VII only!')
        return None
    return [compound[0:i], compound[i:]]
#count_elem('GeSe')


# In[210]:

# the lattice parameters are scaled by comparing the atomic radius
def scale(compound):
    seperate = count_elem(compound)
    scale_factor = 1.
    if len(seperate)==1:
        scale_factor = element.atomic_radius[seperate[0]]/structure_and_lattice.compare_radius
        return math.sqrt(scale_factor)
    else:
        scale_factor = sum(element.atomic_radius[chars] for chars in seperate)/structure_and_lattice.compare_radius/2
        return math.sqrt(scale_factor)
#scale('P')
#tuple(map(lambda i:i*2,(1,2)))


# In[211]:

# phase is integer right now
# phase = 0, 1, 2
def create_lattice(compound,phase):
    return [tuple(map(lambda x: x*scale(compound),structure_and_lattice.lattice[phase][i])) for i in range(len(structure_and_lattice.lattice[phase]))]
#create_lattice('GeSe',0)


# In[212]:

# write the generated structure to a poscar file for VASP
def write_POSCAR(compound,phase):
    filename = 'POSCAR'+'_'+compound+'_'+str(phase)
    seperate = count_elem(compound)
    num_seperate = [structure_and_lattice.lattice_sites[phase]//len(seperate) for i in range(len(seperate))]
    file_w = open(filename, 'w')
    file_w.writelines(filename+'\n')
    file_w.writelines(str(1.0)+'\n')
    file_w.writelines('\t'.join(str(j) for j in i) + '\n' for i in create_lattice(compound,phase))
    #file_w.writelines('\n')
    file_w.writelines('\t'.join(seperate[i] for i in range(len(seperate))))
    file_w.writelines('\n')
    file_w.writelines('\t'.join(str(num_seperate[i]) for i in range(len(seperate))))
    file_w.writelines('\n')
    file_w.writelines('Direct')
    file_w.writelines(('\n'+'\t'.join(str(j) for j in i)) for i in structure_and_lattice.frac[phase])
    file_w.close()
#write_POSCAR('GeS',0)


# In[213]:

# this will generate all the possible structures in selected compound group
def write_POSCAR_group(group):
    for compound in group:
        for phase_struc in structure_and_lattice.phase:
            write_POSCAR(compound, phase_struc)


# In[214]:

write_POSCAR_group(elem_V)
write_POSCAR_group(compound_III_VII)
write_POSCAR_group(compound_IV_VI)
#compound_III_VII


# In[215]:

## set up folders and cp the POSCAR file to correct folder
# os.path module
# the idea is:
# - you will initialize a new path: new_folder=os.path.join(folder_path,folder_name)
# - then use os.makedirs(new_folder) to create the folder
def create_folder(folder_path,folder_name):
    new_folder=os.path.join(folder_path,folder_name)
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)


# In[216]:

#current_path = '/Users/zhenzhu/Project/calculcation/IV-VI/lots_of_struc'


# In[217]:

# create a lot of folders:
folder_path = '/Users/zhenzhu/Project/calculcation/IV-VI/lots_of_struc'
for folder_name in compound_all:
    for phase_name in compound_phase[folder_name]:
        combined_name = os.path.join(folder_name,phase_name)
        create_folder(folder_path,combined_name)   


# In[218]:

#
# os.listdir can show all the files or folders in current dir
# and store the name in a returned list
#
file_dir = os.getcwd()
folder_dir = '/Users/zhenzhu/Project/calculcation/IV-VI/lots_of_struc'
files=os.listdir(file_dir)
for file_name in files:
    if file_name[0]=='.' or file_name[-1]=='b':
        del files[files.index(file_name)]
for file_name in files:
    file_name_list = file_name.split('_')
    #if len(file_name_list)==1:
    #    continue
    shutil.copy2(os.path.join(file_dir,file_name),os.path.join(folder_dir,file_name_list[1],'_'.join(file_name_list[1:]),'POSCAR'))
# In[219]:
#
# create correct POTCAR files
#
#POTCAR_dir = '/Users/zhenzhu/Project/POTCAR'
#folder_dir = '/Users/zhenzhu/Project/calculcation/IV-VI/lots_of_struc'

def combine_file(filenames,outfile_path):
    with open(outfile_path,'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())


# In[220]:

# some test for debug
#
#file1='/Users/zhenzhu/Project/calculcation/NaMnO2/HSE/transition_level/Al_Na/test/file1.dat'
#file2='/Users/zhenzhu/Project/calculcation/NaMnO2/HSE/transition_level/Al_Na/test/file2.dat'
#filenames=[file1,file2]
#file3='/Users/zhenzhu/Project/calculcation/NaMnO2/HSE/transition_level/Al_Na/test/file3.dat'
#combine_file(filenames,file3)


# In[221]:

# POTCAR_dir: the folder you store all the POTCAR files
# folder_dir: the folder you will do calculations in the future
POTCAR_dir = '/Users/zhenzhu/Project/POTCAR'
folder_dir = '/Users/zhenzhu/Project/calculcation/IV-VI/lots_of_struc'
for compound in compound_all:
    elem_in_comp=count_elem(compound)
    if elem_in_comp[0]=='Bis':
        elem_in_comp[0]='Bi'
    filenames = [os.path.join(POTCAR_dir,elem_in_comp[i],'POTCAR') for i in range(len(elem_in_comp))]
    for phase_name in compound_phase[compound]:
        outfile_path = os.path.join(folder_dir,compound,phase_name,'POTCAR')
        combine_file(filenames,outfile_path)
