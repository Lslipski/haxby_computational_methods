#!/bin/bash -l
#PBS -m bea
#PBS -M torwa.gr@dartmouth.edu
#PBS -N subj24_all
#PBS -l nodes=1:ppn=2
#PBS -l walltime=24:00:00
#PBS -o /dartfs-hpc/scratch/psyc164/mvpaces/log/${PBS_JOBID}.o
#PBS -e /dartfs-hpc/scratch/psyc164/mvpaces/log/${PBS_JOBID}.e
#PBS -t 1-8
module load python/anaconda2
source /optnfs/common/miniconda3/etc/profile.d/conda.sh
conda activate comp_meth_env

postfix=$(cat /dartfs-hpc/scratch/psyc164/mvpaces/code/run_sl_svm_clf_24_31.script | head -n ${PBS_ARRAYID} | tail -n 1 | awk '{print $1" "$2" "$3}')

/dartfs-hpc/scratch/psyc164/mvpaces/code/sl_svm_clf.py $postfix


