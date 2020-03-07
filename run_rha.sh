#!/bin/bash -l
#PBS  -m bea
#PBS -M torwa.gr@dartmouth.edu
#PBS -N run_cha
#PBS -l nodes=1:ppn=2
#PBS -l walltime=48:00:00
#PBS -o /dartfs-hpc/scratch/psyc164/tcat/log/${PBS_JOBID}.o
#PBS -e /dartfs-hpc/scratch/psyc164/tcat/log/${PBS_JOBID}.e

module load python/anaconda2
source /optnfs/common/miniconda3/etc/profile.d/conda.sh
conda activate comp_meth_env

python /dartfs-hpc/scratch/psyc164/tcat/code/run_rha.py


