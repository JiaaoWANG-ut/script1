import os
import random
import subprocess
import glob

print("make sure this folder contains pdb file from a same md.pdb output.")
input()
# 获取当前路径
current_dir = os.getcwd()

# 获取当前路径下所有子目录
subdirs = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]

# 随机选择一个子目录
random_dir = random.choice(subdirs)

# 进入该子目录并执行pwd命令
os.chdir(random_dir)

filename=glob.glob("*.pdb")[0]

subprocess.call('echo -e "cp2k\ninptemp.inp\n0\nq"|Multiwfn '+filename, shell=True)

subprocess.call('mv *inp ..', shell=True)


# 返回到当前路径
os.chdir(current_dir)
