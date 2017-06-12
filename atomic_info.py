
# coding: utf-8

# In[27]:

import math


# In[71]:

class element:
    GroupIII = ['B','Al','Ga','In']
    GroupIV = ['C','Si','Ge','Sn','Pb']
    GroupV = ['N','P','As','Sb','Bis']
    GroupVI = ['O','S','Se','Te']
    GroupVII = ['F','Cl','Br','I']
    atomic_mass={'B':10.811,'Al':26.5815,'Ga':69.723,'In':114.818,'C':12.0107,'Si':28.0855,'Ge':72.61,
                 'Sn':118.710,'Pb':207.2,'N':14.0067,'P':30.9738,'As':74.9216,'Sb':121.76,'Bis':208.58,
                 'O':15.9994,'S':32.066,'Se':78.96,'Te':127.60,'F':18.9984,'Cl':35.4527,'Br':79.504,'I':126.90447}
    atomic_radius = {'B':87.,'Al':118.,'Ga':138.,'In':156.,'C':67.,'Si':111.,'Ge':125.,'Sn':145.,'Pb':154.,
                     'N':56.,'P':98.,'As':114.,'Sb':133.,'Bis':143.,'O':48.,'S':88.,'Se':103.,'Te':123.,'F':42.,
                     'Cl':79.,'Br':94.,'I':115.}
    # http://www.thecatalyst.org/electabl.html
    atomic_elec_neg = {'B':2.,'Al':1.5,'Ga':1.6,'In':1.7,'C':2.5,'Si':1.8,'Ge':1.8,'Sn':1.8,'Pb':1.9,'N':3.0,'P':2.1,
                       'As':2.0,'Sb':1.9,'Bis':1.9,'O':3.5,'S':2.5,'Se':2.4,'Te':2.1,'F':4.0,'Cl':3.0,'Br':2.8,'I':2.5}
    atomic_number = {'B':5,'Al':13,'Ga':31,'In':49,'C':6,'Si':14,'Ge':32,'Sn':50,'Pb':82,'N':7,'P':15,
                       'As':33,'Sb':51,'Bis':83,'O':8,'S':16,'Se':34,'Te':52,'F':9,'Cl':17,'Br':35,'I':53}

class structure_and_lattice:
    compare_radius = 98
    # black phosphorus, blue phosphorus, SiS structure
    frac=[[(0.75,0.5997,0.2229),(0.25,0.0997,0.0718),(0.25,0.014384,0.2094),(0.75,0.5144,0.0854)],[(0.0,0.0,0.0113),(0.333,0.333,-0.05132)],[(0.0,0.25,0.5785),(0.5,0.75,0.42152),(0.,0.25,0.41),(0.5,0.75,0.59)]]
    lattice = [[(3.348,0.,0.),(0.,4.623,0.),(0.,0.,20.)],[(2.881076913,-1.662861501,0.0),(2.881077039,1.662861720,0.0),(0.0,0.0,20.)],[(3.6,0,0),(0,3.6,0),(0,0,20)]]
    lattice_sites = [4,2,4]
    phase = [0,1,2]


# In[85]:

class ternary_structure:
    compare_radius = 120 # for GaSeCl
    frac = [[(0.747,0.685,0.103),(0.247,0.189,0.045),(0.247,-0.04,0.109),(0.747,0.464,0.039),(0.246,-0.024,-0.01),(0.746,0.467,0.158)],[(0,0,0.009),(0.333,0.333,0.95),(0,0,0.12)]]
    lattice = [[(3.9,0,0),(0,5.58,0),(0,0,30)],[(3.340,-1.929,0),(3.340,1.929,0),(0,0,20)]]
    lattice_sites = [6,4]
    phase = [0,1]


# In[86]:

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


# In[87]:

compound_III_VI_VII=[]
for char_iii in element.GroupIII:
    for char_vi in element.GroupVI:
        for char_vii in element.GroupVII:
            compound_III_VI_VII.append(char_iii+char_vi+char_vii)


# In[88]:

#str(compound_III_VI_VII)
#len(compound_III_VI_VII)


# In[89]:

# given a certain compound, count how many elements in this compound
# return the element name in a list
# can deal wi
#
def count_elem(compound):
    """
    input: compound name (string)
    output: element in compound (list)
    """
    num_upper = sum(1 for char in compound if char.isupper())
    ret = []
    if num_upper == 1:
        if compound in element.GroupV or compound=='Bi':
            ret.append(compound)
            return ret
        else:
            print('The compound is not correct! Please input V, IV-VI, or III-VII only!')
            return None
    if num_upper == 2:
        i = 1
        while not compound[i].isupper():
            i = i + 1
        if (compound[0:i] in element.GroupIII and compound[i:] not in element.GroupVII) or (compound[0:i] in element.GroupVII and compound[i:] not in element.GroupIII):
            print('The compound is not correct! Please input V, IV-VI, or III-VII only!')
            return None
        elif (compound[0:i] in element.GroupIV and compound[i:] not in element.GroupVI) or (compound[0:i] in element.GroupVI and compound[i:] not in element.GroupIV):
            print('The compound is not correct! Please input V, IV-VI, or III-VII only!')
            return None
        ret.append(compound[0:i])
        ret.append(compound[i:])
        return ret
    if num_upper == 3:
        #ret = []
        i = 0
        while i < len(compound):
            temp = ''
            if compound[i].isupper():
                temp += compound[i]
                i += 1
                while i<len(compound) and not compound[i].isupper():
                    temp += compound[i]
                    i += 1
                ret.append(temp)
        if ret[0] not in element.GroupIII or ret[1] not in element.GroupVI or ret[2] not in element.GroupVII:
            print('The compound is not correct! Please input III-VI-VII (order matters)!')
            return None
        else:
            return ret
#count_elem('GaSeI')


# In[99]:

#count_elem('GaSeI')


# In[90]:

# the lattice parameters are scaled by comparing the atomic radius
def scale(compound):
    """
    scale the structure based on atomic radius
    """
    seperate = count_elem(compound)
    scale_factor = 1.
    if len(seperate)==1:
        scale_factor = element.atomic_radius[seperate[0]]/structure_and_lattice.compare_radius
        return math.sqrt(scale_factor)
    elif len(seperate) == 2:
        scale_factor = sum(element.atomic_radius[chars] for chars in seperate[0:2])/structure_and_lattice.compare_radius/2
        return math.sqrt(scale_factor)
    else:
        scale_factor = sum(element.atomic_radius[chars] for chars in seperate[0:2])/ternary_structure.compare_radius/2
        return math.sqrt(scale_factor)
scale('AlSeCl')
#tuple(map(lambda i:i*2,(1,2)))


# In[91]:

def create_lattice_elem(compound,phase):
    """
    create lattice for elementary structures : N, P, As, Sb, Bi
    """
    return [tuple(map(lambda x: x*scale(compound),structure_and_lattice.lattice[phase][i])) for i in range(len(structure_and_lattice.lattice[phase]))]


# In[92]:

def create_lattice_binary(compound,phase):
    """
    create lattice for binary IV-VI compounds
    """
    return [tuple(map(lambda x: x*scale(compound),structure_and_lattice.lattice[phase][i])) for i in range(len(structure_and_lattice.lattice[phase]))]
#create_lattice('GeSe',0)


# In[93]:

def create_lattice_ternary(compound,phase):
    """
    create lattice for ternary III-VI-VII compounds
    """
    return [tuple(map(lambda x: x*scale(compound),ternary_structure.lattice[phase][i])) for i in range(len(ternary_structure.lattice[phase]))]
#create_lattice('GeSe',0)


# In[94]:

# this will generate all the possible structures in selected compound group
def write_POSCAR_group(group,group_type):
    """
    group_type: 1 for V, 2 for IV-VI, 3 for III-VI-VII
    """
    if group_type == 3:
        group_class = ternary_structure()
    elif group_type == 1 or group_type == 2:
        group_class = structure_and_lattice()
    else:
        print('Wrong group type: group_type: 1 for V, 2 for IV-VI, 3 for III-VI-VII!')
        return
    for compound in group:
        for phase_id in group_class.phase:
            write_POSCAR(compound, phase_id, group_type)


# In[95]:

# write the generated structure to a poscar file for VASP
def write_POSCAR(compound, phase, group_type):
    """
    compound: the compound you want to generate
    phase: the specific structural phase
    group_type: elem, binary, or ternary
    """
    filename = 'POSCAR'+'_'+compound+'_'+str(phase)
    seperate = count_elem(compound)
    if group_type == 1:
        create_lattice = create_lattice_elem
        group_class = structure_and_lattice()
    elif group_type == 2:
        create_lattice = create_lattice_binary
        group_class = structure_and_lattice()
    elif group_type == 3:
        create_lattice = create_lattice_ternary
        group_class = ternary_structure()
    #num_seperate = [structure_and_lattice.lattice_sites[phase]//len(seperate) for i in range(len(seperate))]
    num_seperate = [group_class.lattice_sites[phase]//len(seperate) for i in range(len(seperate))]
    file_w = open(filename, 'w')
    file_w.writelines(filename+'\n')
    file_w.writelines(str(1.0)+'\n')
    file_w.writelines(' '.join(str(j) for j in i) + '\n' for i in create_lattice(compound,phase))
    #file_w.writelines('\n')
    file_w.writelines(' '.join(seperate[i] for i in range(len(seperate))))
    file_w.writelines('\n')
    file_w.writelines(' '.join(str(num_seperate[i]) for i in range(len(seperate))))
    file_w.writelines('\n')
    file_w.writelines('Direct')
    file_w.writelines(('\n'+' '.join(str(j) for j in i)) for i in group_class.frac[phase])
    file_w.close()


# In[97]:

#write_POSCAR('GaSeI',0,3)


# In[ ]:




# In[ ]:



