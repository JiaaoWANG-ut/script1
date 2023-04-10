
#python3 get_packed_cif_from_pdb_pdb.py -inputzeo FAU.pdb -inputmol LiTFSI.pdb
# %%
import subprocess
import argparse
import os 
from ase.io import read
import sys, os

bound=3

global totaltime
totaltime=10


def get_lattice_from_pdb(input_file_zeo):
    import re
    
    f=open(input_file_zeo)
    lattice=re.split(r"[ ]+",f.readlines()[1])[1:4]
    cubic_lattice=" ".join([str(float(lattice[0])-bound),str(float(lattice[1])-bound),str(float(lattice[2])-bound)])
    print(cubic_lattice)
    return cubic_lattice

def packmol_to_zeo(input_file_zeo,input_file_ion,number):
    
    before_coor=['tolerance '+str(bound)+'\n','filetype pdb\n','output output.pdb\n','\n']

    coordinate_list=[\
       'structure '+input_file_zeo+'\n',\
            '    number 1\n',\
                '    fixed 0. 0. 0. 0. 0. 0.\n',\
                'end structure\n'\
                    ]
    
 #   after_coor=[\
 #       'structure '+input_file_mol+'\n',\
 #           '    number '+str(number)+'\n',\
 #               '    inside box '+str(bound)+' '+str(bound)+' '+str(bound)+' '+ get_lattice_from_pdb(input_file_zeo) +'\n',\
  #              'end structure\n']
    ions=[\
        'structure '+input_file_ion+'\n',\
            '    number '+str(number)+'\n',\
                '    inside box '+str(bound)+' '+str(bound)+' '+str(bound)+' '+ get_lattice_from_pdb(input_file_zeo) +'\n',\
                'end structure']
    
    f = open("mail.inp", "w")
    f.writelines(before_coor)
    f.writelines(coordinate_list)
  #  f.writelines(after_coor)
    f.writelines(ions)
    f.close()
    subprocess.call("cat mail.inp",shell=True)

    subprocess.call("packmol < mail.inp",shell=True)

    f=open(input_file_zeo)
    latticeinfo=f.readlines()[1]


    lines=[]
    if os.path.exists("output.pdb"):
        f=open("output.pdb",'r')  
    for line in f:
        lines.append(line)
    f.close()
    lines.insert(5,latticeinfo)         
    s=''.join(lines)
    f=open("output.pdb",'w+') 
    f.write(s)
    f.close()


    return 0
######################TIME OUT Control################
# %%




import numpy as np
def get_100_packing_number(input_file_zeo,input_file_ion):
    for i in np.arange(0,10000,5):
        import time
        start=time.time()
        packmol_to_zeo(input_file_zeo,input_file_ion,i)
        end=time.time()
        time=end-start
        print(time)
        if time > totaltime:
            print("TIME OUT , 100% reach! Full packing number is approximately "+str(i))
            break
    return i

















# %%
def main(fileinput):    

    input_file_zeo = fileinput.inputzeo
    #input_file_mol = fileinput.inputmol
    input_file_ion = fileinput.inpution

    if input_file_zeo :
        print(input_file_zeo)

        half_fill_number=int(get_100_packing_number(input_file_zeo,input_file_ion)/9*8)

        if os.path.exists("output.pdb"):
            os.remove("output.pdb")
        packmol_to_zeo(input_file_zeo,input_file_ion,half_fill_number)

       #   print("TIME OUT 30s, 100% reach! Full packing number is approximately "+str(get_100_packing_number(input_file_zeo,input_file_mol)))
        print("TIME OUT , 100% reach! Half Packing Number is "+str(half_fill_number))
        print("output.pdb generated!")
    
       # with open("add_mols_number", "a+") as f:
       #     f.truncate(0)
       #     f.writelines([str(half_fill_number)])
       # print("add_mols_number Generated!")


        with open("add_ions_number", "a+") as f:
            f.truncate(0)
            f.writelines([str(half_fill_number)])
        print("add_ions_number Generated!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="check cif lattice, if not reach value, supercell it until to get it")
    parser.add_argument("-inputzeo", help="ZEO File path, must be periodic .pdb file from Multiwfn")
    #parser.add_argument("-inputmol", help="mol File path, must be .pdb with bonds info")
    parser.add_argument("-inpution", help="mol File path, must be .pdb with bonds info")
    fileinput = parser.parse_args()
    
    main(fileinput)
# %%
