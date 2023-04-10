SCRIPTS=/home1/08197/jiaao/test/workflow/test-ob/test_pre_run/scripts
cp *cif ZEO.cif
cp $SCRIPTS/Li.mol .
python3 $SCRIPTS/get_bigger_5_cif_cif.py -input ZEO.cif
echo -e "100 \n2 \n1 \n \n0 \n q\n   "|Multiwfn ready.cif
obabel Li.mol -O Li.pdb
python3 $SCRIPTS/get_full_packed_cif_from_pdb_pdb-2.py -inputzeo ready.pdb -inpution Li.pdb
obabel Li.pdb -O Li.mol2;
python $SCRIPTS/deletecharge.py -file Li.mol2
sh $SCRIPTS/build_zeo_itp.sh
sh $SCRIPTS/build_ion_itp.sh
python3 $SCRIPTS/top_generate-1.py -zeoitp ready.itp  -ionitp Li.itp -top ready.top
python $SCRIPTS/clean_itp.py -input ready.itp -keywords atomtypes
python $SCRIPTS/clean_itp.py -input Li.itp -keywords atomtypes
sed -i 's/2.183593E-01/1.183593E-01/g' ready_test.top


gmx grompp -f $SCRIPTS/md_PBC.mdp -c output.pdb -p ready_test.top -o md.tpr -maxwarn 1000
gmx mdrun -v -deffnm md
gmx trjconv -s md.tpr -f md.xtc -o md.pdb <<EOF
0
EOF
