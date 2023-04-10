import subprocess
import os
import multiprocessing as mul
import time



global bashcommand

bashcommand='obabel *.smi -O .mol -m --gen3d'

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
