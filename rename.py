import os

path = '.'
folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

for i, folder in enumerate(sorted(folders)):
    new_foldername = f'rmd_{i+1}'
    os.rename(os.path.join(path, folder), os.path.join(path, new_foldername))
    print(f'Renamed {folder} to {new_foldername}')

print(f'Renamed {len(folders)} folders')

