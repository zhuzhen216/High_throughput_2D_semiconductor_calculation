## High throughput calculations of Group IV-VI, V, III-VII compounds
___
### Basic description
___
The code can convieniently (1) generate structures of isoelectronic group V, IV-VI, and III-VII compounds; (2) creat their POTCAR files; (3) set up the INCAR file for VASP calculations; (4) initialize KPOINTS files. The submission of the jobs can be done by one-click. The supercomputer environments should be set up in related scripts.

The workflow is: first, execute the "POSCAR_generation.py" file, followed by "INCAR_set_up.py", "KPOINTS_set_up.py", and "submission_set_up.py". After the required files being prepared, you can execute "high_throughput_submission.py". Then, VASP is called to optimize all your created structures.

Updates (2017-06-11): "POSCAR_generation.py" is now converted to "atomic_info.py" module. To generate structures of group IV-VI compounds, for example, you can type in:
import atomic_info
atomic_info.write_POSCAR_group(atomic_info.compound_IV_VI,2)
Then, you will see the structures in your folder.

Updates (2017-06-11): "INCAR_set_up.py" and "KPOINTS_set_up.py" are now part of "vasp_manager.py", which contains frequently used functions related to VASP calculations.

Basicly, structure generation now can be achieved by calling "atomic_info.py"; then with "vasp_manager.py", computation folders are prepared with required VASP input files; "hight_throughput_submission.py" interfaces with the supercomputer to initialize the calculations. 

___
### Detailed information about each scripts
___

#### POSCAR_generation.py:

Three most stable phases of 2D P (black, blue P, and also monolayer cubic phase) are selected as the basis. On top of these three phases, the code can generate structures of other isoelectronic systems: (a) keep the fractional coordinates; (b) scale
the lattice parameter based on atomic radius. Output POSCAR files and they are stored in different folders. You need to initialize the folder path "folder_dir = your path" 

POTCAR files are also set up automaticly by the code, saved in the same folder as the structures. You need to give the path that store your POTCAR files "POTCAR_dir = your path".

#### INCAR_set_up.py and KPOINTS_set_up.py

These two scripts are used to set up standard DFT calculations: structure optimization. You need also change the folder path to your own. The path is the folder that contain all your created structures in the previous step.

#### submission_set_up.py

This script creates "submit.sh" file and copy it to each working folder. Later, this file is used to start the calculation.

#### high_throughput_submission.py

This script can submit all the calculations at one time.
