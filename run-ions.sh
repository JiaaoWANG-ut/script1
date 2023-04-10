SCRIPTS=/home1/08197/jiaao/test/workflow/test-ob/test_pre_run/scripts
#cp *cif ZEO.cif
#cp $SCRIPTS/Li.mol .
#python3 $SCRIPTS/get_bigger_5_cif_cif.py -input ZEO.cif

#echo -e "100 \n2 \n1 \n \n0 \n q\n   "|Multiwfn ready.cif
#obabel Li.mol -O Li.pdb
#sleep 10 ##释放内存，使得初始化正常进行


###建模
#python3 $SCRIPTS/get_full_packed_cif_from_pdb_pdb-2.py -inputzeo ready.pdb -inpution Li.pdb


###拓扑文件准备

#obabel Li.pdb -O Li.mol2;
#python3 $SCRIPTS/deletecharge.py -file Li.mol2
#sed -i 's/0.0000/0.5000/g' Li.mol2
#rm *itp *top
#sh $SCRIPTS/build_zeo_itp.sh
#sh $SCRIPTS/build_ion_itp.sh
#python3 $SCRIPTS/top_generate-1.py -zeoitp ready.itp  -ionitp Li.itp -top ready.top
#python3 $SCRIPTS/clean_itp.py -input ready.itp -keywords atomtypes
#python3 $SCRIPTS/clean_itp.py -input Li.itp -keywords atomtypes
#sed -i 's/2.183593E-01/1.533593E-01/g' ready_test.top

gmx grompp -f $SCRIPTS/md_PBC.mdp -c output.pdb -p ready_test.top -o md.tpr -maxwarn 1000

gmx mdrun -v -deffnm md

#####后处理


#gmx make_ndx -f md.tpr -o index.ndx<<EOF
#a LI
#q
#EOF


#gmx msd -f md.xtc -s md.tpr -n index.ndx -o msd_"$(basename `pwd`)".xvg -rmcomm -trestart 0.005>"$(basename `pwd`)".diff<<EOF
#LI
#0
#EOF

