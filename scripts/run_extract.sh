#!/bin/bash
#SBATCH --account=def-wadsley
#SBATCH --job-name=run_python_ext
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --cpus-per-task=1
#SBATCH --mem=256G
#SBATCH --output=plot_extract%j.out

module load gcc openmpi python/3.11 scipy-stack mpi4py

srun python extract.py