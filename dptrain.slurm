#!/bin/bash
#SBATCH -J trywithCSVR
#SBATCH -N 1
#SBATCH -n 64
#SBATCH -p gpu-a100
#SBATCH -t 48:00:00
#SBATCH -o ll_out
##SBATCH -A OTH21011

touch Started
#conda activate deepmd-gpu

dp train input.json


touch Finished
