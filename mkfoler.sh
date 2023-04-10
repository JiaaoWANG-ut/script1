for inf in *.pdb
do
mkdir "${inf}"exmp
cd "${inf}"exmp
mv ../${inf} .
cd ..
done
for file in `find . -name "*.pdbexmp"`
do
    mv $file ${file%.*}
done
