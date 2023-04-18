###from cif to cp2k readable structure file.
###After structure_cp2k.xyz will be generateed.
###in cp2k inp file, remember to write

##&SUBSYS
##@INCLUDE structure_cp2k.xyz

import os
from ase.io import read

# Search for CIF files in directory
cif_files = [filename for filename in os.listdir('.') if filename.endswith('.cif')]

# Raise error if no CIF files found
if not cif_files:
    raise ValueError('No CIF files found in directory')

# Prompt user to choose a CIF file
if len(cif_files) == 1:
    cif_file = cif_files[0]
else:
    print('Multiple CIF files found in directory:')
    for i, filename in enumerate(cif_files):
        print('{}) {}'.format(i+1, filename))
    choice = int(input('Enter the number of the CIF file to use: '))
    cif_file = cif_files[choice-1]

# Read the CIF file
atoms = read(cif_file)

# Extract the crystal cell matrix and atomic coordinates
cell = atoms.cell[:3, :3]
symbols = atoms.get_chemical_symbols()
coords = atoms.get_positions()

# Generate output file name based on input file name
output_name = 'structure_cp2k.xyz'

# Write out the cell matrix and atomic coordinates to output file
with open(output_name, 'w') as f:
    f.write('&CELL\n')
    f.write('   A {:12.8f} {:12.8f} {:12.8f}\n'.format(*cell[0]))
    f.write('   B {:12.8f} {:12.8f} {:12.8f}\n'.format(*cell[1]))
    f.write('   C {:12.8f} {:12.8f} {:12.8f}\n'.format(*cell[2]))
    f.write('   PERIODIC XYZ #Direction of applied PBC (geometry aspect)\n')
    f.write('&END CELL\n\n')
    
    f.write('&COORD\n')
    for i in range(len(symbols)):
        f.write('   {:2} {:12.8f} {:12.8f} {:12.8f}\n'.format(symbols[i], coords[i,0], coords[i,1], coords[i,2]))
    f.write('&END COORD\n')
