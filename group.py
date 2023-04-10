import os
import shutil

path = '.'
folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
num_folders_per_group = 5000

for i in range(0, len(folders), num_folders_per_group):
    group_name = f'group_{i//num_folders_per_group+1}'
    os.makedirs(group_name)
    for folder in folders[i:i+num_folders_per_group]:
        shutil.move(os.path.join(path, folder), os.path.join(group_name, folder))
        print(f'Moved {folder} to {group_name}')
    print(f'Grouped {len(folders[i:i+num_folders_per_group])} folders into {group_name}')

print(f'Grouped {len(folders)} folders into {len(os.listdir())} groups')
