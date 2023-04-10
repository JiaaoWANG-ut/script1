import subprocess
import os
import multiprocessing as mul
import time



global bashcommand

bashcommand='obabel *.smi -O .xyz -m --gen3d; echo -e "cp2k\n \n 3\n 1\n -1\n 3\n 4\n 0\n q\n   "|Multiwfn *.xyz'

def command(i):
    if os.path.isdir(i):
        os.chdir(i)
        print(i)
        subprocess.call(bashcommand,shell=True)
        os.chdir("../")


CORES=30
pool=mul.Pool(CORES)
arg=os.listdir("./")
start=time.time()
rel=pool.map(command,arg)
end=time.time()

print("total time: ", end-start, "s")
