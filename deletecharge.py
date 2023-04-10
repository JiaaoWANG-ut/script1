import os
import argparse

def main(fileinput):

    input_file = fileinput.file

    if os.path.exists(input_file):
        print("Read "+str(input_file)+" Successfully")
        with open(input_file) as f:
            mol=f.readlines()
    else:
        print("Cannot find "+str(input_file)+" file! Check it !")

#print(mol)

    newmol=[]

    for i in range(len(mol)):
        if  "@<TRIPOS>UNITY_ATOM_ATTR" not in mol[i]:
            newmol.append(mol[i])
        else:
            break

    for i in range(len(mol)):
        if "@<TRIPOS>BOND" in mol[i]:
            start=i
            break

    for i in range(start,len(mol)):
        newmol.append(mol[i])

    if os.path.exists(input_file):
        f=open(input_file,"w+")
        f.truncate(0)
        f.writelines(newmol)
        f.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="check cif lattice, if not reach value, supercell it until to get it")
    parser.add_argument("-file", help="ZEO File path, must be periodic .pdb file from Multiwfn")
#    parser.add_argument("-inputmol", help="mol File path, must be .pdb with bonds info")
#    parser.add_argument("-inpution", help="mol File path, must be .pdb with bonds info")
    fileinput = parser.parse_args()

    main(fileinput)

#print(newmol)
