#cp /home1/08197/jiaao/software/sobtop_1.0/* .
cp $SCRIPTS/sobtop_1.0/* .
./sobtop <<EOF
Li.mol2
1
2
4


0
EOF

rm assign_AT.dat atomtype ATOMTYPE_AMBER.DEF atomtype.exe ATOMTYPE_GFF.DEF  bondcrit.dat  bonded_param.dat CORR_NAME_TYPE.DAT libiomp5md.dll LJ_param.dat sobtop sobtop.exe sobtop.ini
