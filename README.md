## High throughput calculations of Group IV-VI, V, III-VII compounds
___
Basic description
___
The script can convieniently (1) generate structures of isoelectronic group V, IV-VI, and III-VII compounds; (2) creat their POTCAR files; (3) set up the INCAR file for VASP calculations; (4) initialize KPOINTS files. The submission of the jobs can be done by one-click. The supercomputer environments should be set up in related scripts.

The workflow is: first, execute the "POSCAR_generation.py" file, followed by "INCAR_set_up.py", "KPOINTS_set_up.py", and "submission_set_up.py". After the required files being prepared, you can execute "high_throughput_submission.py". Then, VASP is called to optimize all your created structures.

Three most stable phases of 2D P (black, blue P, and also monolayer cubic phase) are selected as the basis. On top of these three phases, the code can generate structures of other isoelectronic systems: (a) keep the fractional coordinates; (b) scale
the lattice parameter based on atomic radius.

Output POSCAR files and they are stored in different folders. You need to initialize the folder path "folder_dir = your path" 

POTCAR files are also set up automaticly by the code, saved in the same folder as the structures. You need to give the path that store your POTCAR files "POTCAR_dir = your path".
