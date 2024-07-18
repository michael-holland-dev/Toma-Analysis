#!/bin/bash

#SBATCH --time=00:15:00
#SBATCH --ntasks=100
#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --mem=50G
#SBATCH --mail-user=mwh1998@byu.edu
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --qos=cs

# some helpful debugging options
# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
module load miniconda3
eval "$(conda shell.bash hook)"
conda activate "craters"

TOMOGRAPH_FPATH="/home/mwh1998/fsl_groups/grp_tomo_db1_d3/compute/TomoDB1_d3/Hneptunium_secretin/aba2006-11-01-6/Hyphomonas_10bin_full.rec"

python train.py 

