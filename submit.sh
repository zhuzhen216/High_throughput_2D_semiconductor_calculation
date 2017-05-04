#!/bin/bash
# stampede.tacc.utexas.edu: PWD
#SBATCH -J job
#SBATCH -o job.o%j
#SBATCH -p normal
#SBATCH -n 16
#SBATCH -t 24:00:00
#SBATCH --mail-user=zhen_zhu@126.com
#SBATCH -A TG-DMR070072N
module swap intel intel/14.0.1.106
module swap mvapich2 impi/4.1.3.049
cd $SLURM_SUBMIT_DIR
ibrun $HOME/bin/vasp.541_p3.stampede
