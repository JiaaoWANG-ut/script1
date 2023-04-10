import os
import shutil

# Set the path to the directories containing the md.pdb files
path = os.getcwd()

# Create the "order" directory to store the aliases
order_dir = os.path.join(path, "order")
if not os.path.exists(order_dir):
    os.makedirs(order_dir)

# Get a list of all the directories in the specified path
dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

# Get a list of tuples containing the size and directory path for each md.pdb file
pdb_sizes = []
for d in dirs:
    pdb_path = os.path.join(path, d, "md.pdb")
    if os.path.exists(pdb_path):
        size = os.path.getsize(pdb_path)
        pdb_sizes.append((size, pdb_path))

# Sort the list of tuples by size
sorted_pdb_sizes = sorted(pdb_sizes, key=lambda x: x[0])

# Create an alias for each md.pdb file in the "order" directory with the size rank order as part of the name
for i, pdb_info in enumerate(sorted_pdb_sizes):
    size = pdb_info[0]
    pdb_path = pdb_info[1]
    alias_name = os.path.join(order_dir, "md_pdb_size_rank_" + str(i) + "_size_" + str(size) + ".alias")
    if not os.path.exists(alias_name):
        os.symlink(pdb_path, alias_name)

