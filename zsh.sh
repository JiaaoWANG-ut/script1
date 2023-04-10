#!/bin/bash
#SBATCH -J trywithCSVR
#SBATCH -N 1
#SBATCH -n 64
#SBATCH -p development
#SBATCH -t 02:00:00
#SBATCH -o ll_out
#SBATCH -A CHE23004
ml reset
ml intel/19.1.1
ml mvapich2/2.3.7
ml python3/3.9.7
ml boost/1.72
ml cmake
#export OMP_NUM_THREADS=4
#export INSTALL_DIR=/home1/08197/jiaao/account/app/ls6-cp2k/1.cpu/cp2k-8.2.0/
SCRIPTS=/home1/08197/jiaao/test/workflow/test-ob/test_pre_run/scripts

time for i in `ls -F | grep '/$'`
do
    cd $i
    python3 $SCRIPTS/build-inp-2.py -input *pdb
    cd ../
done


#touch Started

#/usr/local/bin/ibrun $INSTALL_DIR/exe/Linux-x86-64-intel/cp2k.psmp  *.inp


#touch Finished
