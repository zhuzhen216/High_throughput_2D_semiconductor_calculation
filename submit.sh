#!/bin/bash
# stampede.tacc.utexas.edu: PWD
#PBS -N job
#PBS -l nodes=1:ppn=8
#PBS -l walltime=48:00:00
#PBS -j oe
#PBS -V

cd $PBS_O_WORKDIR
source /usr/local/intel/composer_xe_2013.5.192/bin/compilervars.sh intel64
source /usr/local/intel/composer_xe_2013.5.192/mkl/bin/mklvars.sh intel64
export PATH=/usr/local/openmpi-1.6.4/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/openmpi-1.6.4/lib:$LD_LIBRARY_PATH
ulimit -s unlimited
/usr/local/openmpi-1.6.4/bin/mpirun -np 8 -machinefile $PBS_NODEFILE /home/vandewalle/codes/guild/VASP/vasp.541_p3.guild