
# coding: utf-8

# In[1]:

import os
import shutil
import atomic_info


# ___
# ## Set up VASP inputs:
# ___

# In[24]:

def create_folder(folder_path,folder_name):
    """
    Create a folder to do the calculation
    """
    new_folder=os.path.join(folder_path,folder_name)
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)


# In[25]:

def set_INCAR(folder_path=os.curdir,ISIF=2,ENCUT=500,ISMEAR=-5):
    """
    set up a INCAR file for PBE calculation
    default: no lattice optimization
    """
    filename = folder_path+'/INCAR'
    f_incar = open(filename,'w')
    f_incar.writelines('System = PBE calc'+'\n')
    f_incar.writelines('ISMEAR = '+str(ISMEAR)+'\n')
    #f_incar.writelines('SIGMA = 0.1'+'\n')
    f_incar.writelines('ENCUT = '+str(ENCUT)+'\n')
    f_incar.writelines('IBRION=2; '+ 'ISIF='+str(ISIF)+'; NSW=100\n')
    f_incar.writelines('EDIFF  = 0.1E-05'+'\n')
    f_incar.writelines('EDIFFG = -0.01\n')
    f_incar.writelines('NEDOS = 3001')
    f_incar.close()
#set_INCAR('/Users/zhenzhu/GitHub/POSCAR_generation/test',ISMEAR=-5)


# In[26]:

def set_INCAR_HSE(folder_path=os.curdir,NSW=100,ISIF=2,ENCUT=400,ISMEAR=-5):
    """
    set up a INCAR file for HSE calculation
    default: not optimizing the lattice; energy cutoff: 400 eV
    """
    incar_open = open(folder_path+'/INCAR','w')
    incar_open.writelines('LREAL = .FALSE.\nENCUT = '+str(ENCUT)+'\nALGO = All\nEDIFF = 1e-5\n')
    incar_open.writelines('EDIFFG = -0.02\nLVHAR = .TRUE.\nIBRION = 2\nISIF = '+str(ISIF)+'\nNSW = '+str(NSW)+'\n')
    incar_open.writelines('GGA_COMPAT = F\nNELM = 100\nNELMIN = 5\nLASPH = .TRUE.\nISMEAR = '+str(ISMEAR)+'\n')
    incar_open.writelines('LHFCALC = .TRUE.\nAEXX = 0.25\nHFSCREEN = 0.2\nPRECFOCK = Fast\nLORBIT = 10\nISYM=2\n')
    incar_open.writelines('NEDOS = 3001')
    incar_open.close()
#set_INCAR_HSE()


# In[27]:

#
# set up POTCAR
# filenames: a list of elements
# POTCAR_path: the folder you store all your POTCAR files
#
def set_POTCAR(POTCAR_path,elem_list,combined_POTCAR_path):
    """
    set up POTCAR
    input: POTCAR_path, elem_list, combined_POTCAR_path
    filenames: a list of elements
    POTCAR_path: the folder you store all your POTCAR files
    """
    with open(combined_POTCAR_path,'w') as outfile:
        for elem_name in elem_list:
            with open(POTCAR_path+'/'+elem_name+'/'+'POTCAR') as infile:
                outfile.write(infile.read())


# In[28]:

#help(set_POTCAR)


# In[29]:

def set_KPOINTS(folder_path,kx,ky,kz,shifted=False):
    """
    set up a KPOINTS in a folder
    provide 'folder', kx, ky, kz as input
    """
    filename = folder_path+'/KPOINTS'
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


# In[47]:

#
# creat POSCAR file into the folder that put
#
# atomic_info.write_POSCAR(compound,phase_index,folder_path=os.curdir,show_screen=False)
def set_POSCAR(from_path,to_path,poscar='POSCAR'):
    """
    from_path: the folder contains POSCAR file or CONTCAR file
    to_path: the folder to do calculation
    poscar: by default = 'POSCAR'; can be changed to 'CONTCAR'
    """
    from_POSCAR = os.path.join(from_path,poscar)
    to_POSCAR=to_path+'/POSCAR'
    shutil.copy2(from_POSCAR,to_POSCAR)


# ___
# ## Set up submission file
# ___

# In[31]:

def set_submit_stampede(to_folder=os.getcwd()):
    """ 
    1. submit to stampede 
    2. this will create a submission  file in the folder to do calculations
    """
    submit_file=open(os.path.join(to_folder,'submit.sh'),'w')
    submit_file.writelines('#!/bin/bash'+'\n')
    submit_file.writelines('# stampede.tacc.utexas.edu: PWD'+'\n')
    submit_file.writelines('#SBATCH -J job'+'\n')
    submit_file.writelines('#SBATCH -o job.o%j'+'\n')
    submit_file.writelines('#SBATCH -p normal'+'\n')
    submit_file.writelines('#SBATCH -n 16'+'\n')
    submit_file.writelines('#SBATCH -t 24:00:00'+'\n')
    submit_file.writelines('#SBATCH --mail-user=zhen_zhu@126.com'+'\n')
    submit_file.writelines('#SBATCH -A TG-DMR070072N'+'\n')
    submit_file.writelines('module swap intel intel/14.0.1.106'+'\n')
    submit_file.writelines('module swap mvapich2 impi/4.1.3.049'+'\n')
    submit_file.writelines('cd '+to_folder+'\n')
    submit_file.writelines('ibrun $HOME/bin/vasp.541_p3.stampede'+'\n')
    submit_file.close()
#set_submit_stampede()


# In[32]:

## submit to guild
def set_submit_guild(to_folder=os.getcwd()):
    """ 
    1. submit to guild 
    2. this will create a submission  file in the folder to do calculations
    3. the submission file is well-prepared. No need to modify it.
    """
    submit_file=open(os.path.join(to_folder,'submit.sh'),'w')
    submit_file.writelines('#!/bin/bash'+'\n')
    submit_file.writelines('# stampede.tacc.utexas.edu: PWD'+'\n')
    submit_file.writelines('#PBS -N job'+'\n')
    submit_file.writelines('#PBS -l nodes=1:ppn=8'+'\n')
    submit_file.writelines('#PBS -l walltime=48:00:00'+'\n')
    submit_file.writelines('#PBS -j oe'+'\n')
    submit_file.writelines('#PBS -V'+'\n')
    submit_file.writelines('cd '+to_folder+'\n')
    submit_file.writelines('source /usr/local/intel/composer_xe_2013.5.192/bin/compilervars.sh intel64'+'\n')
    submit_file.writelines('source /usr/local/intel/composer_xe_2013.5.192/mkl/bin/mklvars.sh intel64'+'\n')
    submit_file.writelines('export PATH=/usr/local/openmpi-1.6.4/bin:$PATH'+'\n')
    submit_file.writelines('export LD_LIBRARY_PATH=/usr/local/openmpi-1.6.4/lib:$LD_LIBRARY_PATH'+'\n')
    submit_file.writelines('ulimit -s unlimited'+'\n')
    submit_file.writelines('/usr/local/openmpi-1.6.4/bin/mpirun -np 8 -machinefile $PBS_NODEFILE /home/vandewalle/codes/guild/VASP/vasp.541_p3.guild')
    submit_file.close()
#set_submit_guild()


# ___
# ## Check whether a VASP calculation is completed
# ___

# In[36]:

def oszicar_complete(file):
    """
    check whether OSZICAR is completed
    """
    if not os.path.exists(file):
        return False
    file_open=open(file,'r+')
    file_cont=file_open.readlines()
    if len(file_cont)<5:
        return False
    if 'F=' not in file_cont[-1].split():
        return False
    else:
        return True


# In[38]:

#oszicar_complete('OSZICAR')


# In[35]:

def file_empty(file):
    """
    check whether a file is empty
    first check whether it exists: if not, return True
    then check whther the file is empty or not completed: if yes, return True.
    """
    if not os.path.exists(file):
        return True
    file_open=open(file,'r+')
    file_cont=file_open.readlines()
    if len(file_cont)<5:
        return True
    else:
        return False


# ___
# ## Obtain useful results:
# ___

# In[40]:

def obt_TotEnergy(oszicar_file):
    """
    read total energy from a completed oszicar
    """
    oszicar = open(oszicar_file,'r')
    oszicar_cont = oszicar.readlines()
    oszicar.close()
    return float(oszicar_cont[-1].split()[4])


# In[41]:

def obt_NumOfAtoms(poscar_file):
    """
    read how many atoms in each cell
    """
    poscar = open(poscar_file,'r')
    poscar_cont = oszicar.readlines()
    poscar.close()
    num_of_atom=poscar_cont[6].split()
    if len(num_of_atom)==1:
        return int(num_of_atom[0])
    else:
        return sum([int(char) for char in num_of_atom])


# In[17]:

#
# normalize the total energy of a system
#
def energy_per_atom(oszicar_file,poscar_file):
    return obt_TotEnergy(oszicar_file)/obt_NumOfAtoms(poscar_file)


# In[42]:

def obt_FermiLev(vasprun_xml):
    """
    read Fermi level of the system
    """
    vasprun_out = open(vasprun_xml,'r+')
    for line in vasprun_out:
        if 'efermi' in line:
            return float(line.split()[2])
            break
    vasprun_out.close()


# In[43]:

#
# read DOSCAR file and output band gap value, VBM, and CBM
#
def obt_bandgap(doscar,fermi_level):
    """
    read DOSCAR file and output a list: [band gap value, VBM, CBM]
    """
    doscar_out = open(doscar,'r')
    count = 0
    small_number = 0.000001
    gap_value = 0.
    VBM = fermi_level
    CBM = fermi_level
    conti_zero = []
    for line in doscar_out:
        count =  count + 1
        if count > 6:
            val_list = [float(line.split()[i]) for i in range(3)]
            #print(val_list)
            if val_list[1]<small_number:
                conti_zero.append(val_list[0])
                #print(val_list)
                #break
            else:
                if len(conti_zero)>=2 and conti_zero[0]<=fermi_level+0.05 and conti_zero[-1]>fermi_level:
                    gap_value = (conti_zero[-1]-conti_zero[0])/(len(conti_zero)-1)*(len(conti_zero)+1)
                    #print(conti_zero)
                    VBM = conti_zero[0]-(conti_zero[-1]-conti_zero[0])/len(conti_zero)
                    CBM = conti_zero[-1]+(conti_zero[-1]-conti_zero[0])/len(conti_zero)
                    break
                #elif conti_zero[0]>fermi_level:
                #    break
                else:
                    conti_zero=[]
    doscar_out.close()
    return [gap_value,VBM,CBM]


# ___
# ## Band alignment calculation
# ___

# In[44]:

def MAV_empty(file):
    file_open=open(file,'r+')
    file_cont=file_open.readlines()
    if len(file_cont)<5:
        return True
    else:
        return False


# In[45]:

def dan_empty(file):
    file_open=open(file,'r+')
    file_cont=file_open.readlines()
    if len(file_cont)<5:
        return True
    else:
        return False


# In[46]:

# to obtain the average potential of VACUUM level
def ave_n_val(energy_list,n):
    list_ave_n = []
    if len(energy_list)<n:
        return sum(energy_list)/n
    for i in range(len(energy_list)-n+1):
        list_ave_n.append(sum(energy_list[i:i+n])/n)
    return max(list_ave_n)


# In[ ]:



