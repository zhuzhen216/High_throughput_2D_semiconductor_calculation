
# coding: utf-8

# In[2]:
import math
import os
import shutil

class element:
    GroupIII = ['B','Al','Ga','In']
    GroupIV = ['C','Si','Ge','Sn','Pb']
    GroupV = ['N','P','As','Sb','Bis']
    GroupVI = ['O','S','Se','Te']
    GroupVII = ['F','Cl','Br','I']
    atomic_mass={'B':10.811,'Al':26.5815,'Ga':69.723,'In':114.818,'C':12.0107,'Si':28.0855,'Ge':72.61,'Sn':118.710,'Pb':207.2,'N':14.0067,'P':30.9738,'As':74.9216,'Sb':121.76,'Bis':208.58,'O':15.9994,'S':32.066,'Se':78.96,'Te':127.60,'F':18.9984,'Cl':35.4527,'Br':79.504,'I':126.90447}
    atomic_radius = {'B':87.,'Al':118.,'Ga':138.,'In':156.,'C':67.,'Si':111.,'Ge':125.,'Sn':145.,'Pb':154.,'N':56.,'P':98.,'As':114.,'Sb':133.,'Bis':143.,'O':48.,'S':88.,'Se':103.,'Te':123.,'F':42.,'Cl':79.,'Br':94.,'I':115.}
    atomic_elec_neg = {'B':2.,'Al':1.5,'Ga':1.6,'In':1.7,'C':2.5,'Si':1.8,'Ge':1.8,'Sn':1.8,'Pb':1.9,'N':3.0,'P':2.1,'As':2.0,'Sb':1.9,'Bis':1.9,'O':3.5,'S':2.5,'Se':2.4,'Te':2.1,'F':4.0,'Cl':3.0,'Br':2.8,'I':2.5}
    atomic_number = {'B':5,'Al':13,'Ga':31,'In':49,'C':6,'Si':14,'Ge':32,'Sn':50,'Pb':82,'N':7,'P':15,'As':33,'Sb':51,'Bis':83,'O':8,'S':16,'Se':34,'Te':52,'F':9,'Cl':17,'Br':35,'I':53}


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
        if compound in element.GroupV or compound=='Bi':
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
# write the generated structure to a poscar file for VASP
def write_POSCAR(compound,phase,show_screen=False,folder_path=os.curdir):
    seperate = count_elem(compound)
    num_seperate = [structure_and_lattice.lattice_sites[phase]//len(seperate) for i in range(len(seperate))]
    compound_phase = compound+'_'+str(phase)
    filename = os.path.join(folder_path,'POSCAR'+'_'+compound_phase)
    if show_screen == True:
        print(compound_phase+'\n')
        print(str(1.0)+'\n')
        for i in create_lattice(compound,phase):
            print(' '.join(str(j) for j in list(i)))
            print('\n')
        print(' '.join(seperate[i] for i in range(len(seperate))))
        print('\n')
        print(' '.join(str(num_seperate[i]) for i in range(len(seperate))))
        print('\n')
        print('Direct')
        for i in structure_and_lattice.frac[phase]:
            print('\n'+' '.join(str(j) for j in i))
    else:    
        file_w = open(filename, 'w')
        file_w.writelines(compound_phase+'\n')
        file_w.writelines(str(1.0)+'\n')
        file_w.writelines(' '.join(str(j) for j in i) + '\n' for i in create_lattice(compound,phase))
        #file_w.writelines('\n')
        file_w.writelines(' '.join(seperate[i] for i in range(len(seperate))))
        file_w.writelines('\n')
        file_w.writelines(' '.join(str(num_seperate[i]) for i in range(len(seperate))))
        file_w.writelines('\n')
        file_w.writelines('Direct')
        file_w.writelines(('\n'+' '.join(str(j) for j in i)) for i in structure_and_lattice.frac[phase])
        file_w.close()


# In[213]:

# this will generate all the possible structures in selected compound group
def write_POSCAR_group(group):
    for compound in group:
        for phase_struc in structure_and_lattice.phase:
            write_POSCAR(compound, phase_struc)


# In[4]:

#element.atomic_mass


# In[ ]:



