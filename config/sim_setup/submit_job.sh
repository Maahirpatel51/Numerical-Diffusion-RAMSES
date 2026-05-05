#!/bin/bash
#SBATCH --account=def-wadsley
#SBATCH --job-name=vgal_test
#SBATCH --time=4:00:00
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=64
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=8G
#SBATCH --output=vgal_test%j.out

# Go to the working directory
cd $SLURM_SUBMIT_DIR

module load gcc openmpi hdf5 

PARAM_FILE=$HOME/analysis/vgal_sims/params.nml
RUN_DIR=$HOME/links/scratch/vgal_sims/$SLURM_JOB_ID

mkdir -p $RUN_DIR
cd $RUN_DIR || exit 1

export C_INCLUDE_PATH=/home/robinh4/local/include
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/robinh4/grackle/src/clib/.libs

# Run RAMSES with MPI
srun /home/maahir/ramses_mcmaster/bin/ramses.vgal3d $PARAM_FILE