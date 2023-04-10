#!/bin/bash
#SBATCH -p development
#SBATCH -n 40
#SBATCH -N 1
#SBATCH -t 02:00:00
#SBATCH -J chouzhen
#SBATCH -V
#SBATCH -o ll_out-chouzhen
#SBATCH -A OTH21011

#source /home1/08197/jiaao/account/app/gromacs/bin/GMXRC
#module load gromacs/2022.1 
#module load impi/19.0.9
#module load intel/19.1.1
#export PATH=~/account/app/gromacs/bin/

python3 chouzhen.py -input md.pdb -num all

#mpirun -np 40 gmx_mpi mdrun -v -deffnm md
#gmx_mpi mdrun -v -deffnm md #-pme gpu -nb gpu -bonded gpu
