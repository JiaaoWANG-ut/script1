SCRIPTS=/home1/08197/jiaao/test/workflow/test-ob/test_pre_run/scripts

#conda activate /home1/08197/jiaao/miniconda3/envs/my-rdkit-env
#conda create -c conda-forge -n my-rdkit-env rdkit
#conda install -c conda-forge openbabel
#conda activate my-rdkit-env
#conda install -c conda-forge ase
#pip install pymatgen

cp $SCRIPTS/* .
echo "执行的文件名：$0";
echo "ZEO.CIF为：$1";
echo ".mol(包含Li离子的)为：$2";

#source ~/.bashrc
conda activate my-rdkit-env
cp $1 ZEO.cif
python3 get_bigger_20_cif_cif-1.py -input ZEO.cif
echo -e "100 \n2 \n1 \n \n0 \n q\n   "|Multiwfn ready.cif
sh build_zeo_itp.sh

###mol文件生成mol itp文件
cp $2 RES.mol
obabel RES.mol -O mol.pdb
python3 change_MOL_to_RES.py -input mol.pdb -original UNL -new RES
obabel mol.pdb -O mol.mol2
python deletecharge.py
sh build_mol_itp.sh

###生成分子筛——离子对填充物（50%的）模型
python3 get_packed_cif_from_pdb_pdb-1.py -inputzeo ready.pdb -inputmol mol.pdb
##这一步不仅预测分子，而且还给出晶胞信息
python3 change_MOL_to_RES.py -input output.pdb -original LI -new Li

###生成top文件
python3 top_generate.py -zeoitp ready.itp -molitp mol.itp -top ready.top
#这里不能反复运行，否则会把清洗之后的itp写进ready.top中。正确做法是重新生成itp文件

###清洗itp文件
python clean_itp.py -input mol.itp -keywords atomtypes
python clean_itp.py -input ready.itp -keywords atomtypes


###准备mdp 输入global文件模板
#from script already got input! If you wanna spicify please activate the following line:
#cp /home1/08197/jiaao/software/sobtop_1.0/examples/md_PBC.mdp .


###生成tpr文件
gmx grompp -f md_PBC.mdp -c output.pdb -p ready_test.top -o md.tpr -maxwarn 1000

##运行Gromacs
mpirun -np 5 gmx mdrun -v -deffnm md

##轨迹文件生成
gmx trjconv -s md.tpr -f md.xtc -o md.pdb <<EOF
0
EOF

zip -r mytraj.zip md.pdb
