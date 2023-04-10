SCRIPTS=/home1/08197/jiaao/test/workflow/test-ob/test_pre_run/scripts

#conda activate /home1/08197/jiaao/miniconda3/envs/my-rdkit-env
#conda create -c conda-forge -n my-rdkit-env rdkit
#conda install -c conda-forge openbabel
#conda activate my-rdkit-env
#conda install -c conda-forge ase
#pip install pymatgen


echo "执行的文件名：$0";
echo "ZEO.CIF为：$1";
echo ".mol(包含分子的)为：$2";
echo ".mol(包含离子的): $3"

cp $1 ZEO.cif
cp $2 RES.mol
cp $3 Li.mol

obabel RES.mol -O mol.pdb
python3 $SCRIPTS/get_bigger_20_cif_cif-1.py -input ZEO.cif
echo -e "100 \n2 \n1 \n \n0 \n q\n   "|Multiwfn ready.cif
obabel Li.mol -O Li.pdb
python3 $SCRIPTS/get_full_packed_cif_from_pdb_pdb-1.py -inputzeo ready.pdb -inputmol mol.pdb -inpution Li.pdb
obabel mol.pdb -O mol.mol2
python3 $SCRIPTS/deletecharge.py -file mol.mol2
obabel Li.pdb -O Li.mol2;
python $SCRIPTS/deletecharge.py -file Li.mol2
sh $SCRIPTS/build_mol_itp.sh
sh $SCRIPTS/build_zeo_itp.sh
sh $SCRIPTS/build_ion_itp.sh
python3 $SCRIPTS/top_generate.py -zeoitp ready.itp -molitp mol.itp -ionitp Li.itp -top ready.top
python $SCRIPTS/clean_itp.py -input mol.itp -keywords atomtypes
python $SCRIPTS/clean_itp.py -input ready.itp -keywords atomtypes
python $SCRIPTS/clean_itp.py -input Li.itp -keywords atomtypes
gmx grompp -f $SCRIPTS/md_PBC.mdp -c output.pdb -p ready_test.top -o md.tpr -maxwarn 1000

