# %%
import subprocess
import argparse
import os 
from ase.io import read
import sys, os
import ase.io.vasp

min_lattice_len=15 #angs


def from_cif_get_lattice_list(input_file):
    from pymatgen.core import Structure
    s=Structure.from_file(input_file)
    return [s.lattice.lengths[0], s.lattice.lengths[1], s.lattice.lengths[2]]

# %%
def from_cif_get_supercell_cif(input_file,x,y,z,output_name):

    from pymatgen.core import Structure
    structure = Structure.from_file(input_file)
    structure.make_supercell(scaling_matrix=[x, y, z], to_unit_cell=False)
    structure.to(filename=output_name)
    return 
# %%

def main(file):    
    input_file = file.input
    
    #print(lattice)
    lattice=from_cif_get_lattice_list(input_file)
    from_cif_get_supercell_cif(input_file,1,1,1,"ready.cif")
    print("Current Lattice:")
    for i in range(100):  ##50 times loops to make sure enough check times
            if min(lattice) < min_lattice_len:
                if lattice.index(min(lattice))==0:
                    x=2;y=1;z=1
                if lattice.index(min(lattice))==1:
                    x=1;y=2;z=1
                if lattice.index(min(lattice))==2:
                    x=1;y=1;z=2
                if i > 0:
                    from_cif_get_supercell_cif("ready.cif",x,y,z,"ready.cif")
                lattice=from_cif_get_lattice_list("ready.cif")
                print(lattice)
            else:
                print("Finished, the "+str(input_file)+" min Lattice cell now is larger than "+str(min_lattice_len))
                print(lattice)
                print("ready.cif is generated!")
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="check cif lattice, if not reach value, supercell it until to get it")
    parser.add_argument("-input", help="File path")
    file = parser.parse_args()
    main(file)
# %%
