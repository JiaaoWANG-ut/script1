#import dpdata
#import random

#data=dpdata.LabeledSystem('./cp2k.log',fmt='cp2k/output')
#print(data)
#print(len(data))


from dpdata import LabeledSystem,MultiSystems
from glob import glob
import shutil
import os
from random import sample
import subprocess

testratio=0.13
"""
process multi systems
"""




fs=glob('./*/ll_out')  # remeber to change here !!!
#print(fs)
tt=MultiSystems()
for f in fs:
    try:
        #print(f)
        ls=LabeledSystem(f,fmt='cp2k/output')
        #print(ls)
    except:
        print(f,"cannot convert into dpmd format")
        os.remove(f)
    if len(ls)>0:
        try:
            tt.append(ls)
        except:
            print("ERROR",f)
            os.remove(f)


fs=glob('./*/ll_out')  # remeber to change here !!!

testfs=sample(fs,int(len(fs)*testratio))
trainfs=[]
for i in fs:
    if i in testfs:
        sub=1
        #print("skip")
    else:
        trainfs.append(i)

print("Train-number/Test-number",len(trainfs),len(testfs))

#print(fs)
ms=MultiSystems()
for f in trainfs:
    try:
        #print(f) 
        ls=LabeledSystem(f,fmt='cp2k/output')
        #print(ls)
    except:
        print(f,"cannot convert into dpmd format")
    if len(ls)>0:
        try:
            ms.append(ls)
        except:
            print("ERROR",f)

try:
    ms.to_deepmd_raw('deepmd/trainraw')
    print("DUMP TRAIN RAW SUCCESSFULLY")
except:
    print("ERROR DUMP RAW")

try:
    #print(ms[1:3])
    ms.to_deepmd_npy('deepmd/trainnpy')
    print("DUMP TRAIN RAW SUCCESSFULLY")
except:
    print("ERROR DUMP NPY")









ms=MultiSystems()
for f in testfs:
    try:
        #print(f)
        ls=LabeledSystem(f,fmt='cp2k/output')
        #print(ls)
    except:
        print(f,"cannot convert into dpmd format")
    if len(ls)>0:
        try:
            ms.append(ls)
        except:
            print("ERROR",f)

try:
    ms.to_deepmd_raw('deepmd/testraw')
    print("DUMP TEST RAW SUCCESSFULLY")
except:
    print("ERROR DUMP RAW")

try:
    #print(ms[1:3])
    ms.to_deepmd_npy('deepmd/testnpy')
    print("DUMP TEST RAW SUCCESSFULLY")
except:
    print("ERROR DUMP NPY")



