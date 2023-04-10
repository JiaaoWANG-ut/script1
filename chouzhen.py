import os
import multiprocessing as mul
import random
import shutil
import argparse
import subprocess
import time
#file_name="ready.itp"

file_container_name="pdb2multi/"
CORES=10
key_words="ENDMDL\n"
key_words_head="REMARK    GENERATED BY TRJCONV\n"




#import random
import string

def generate_random_string(length):
    # Define the possible characters for the string
    chars = string.ascii_letters + string.digits

    # Generate a random string of the specified length
    random_string = ''.join(random.choice(chars) for _ in range(length))

    return random_string


###

######从文件中获取信息########
def readfile(file_name):  ##readfile get list
    try:
        with open(file_name) as f:
            mol=f.readlines()
            keywords=key_words
            totalnumber=mol.count(keywords)
            print("\n\n\n\n"+str(file_name)+" read!\n\n\n")
    except:
        print("\n\n\n\nfilename invalid\n\n\n\n")
    ######读取完了文件为mol，目前获取文件中关键字区块信息
    return [mol,totalnumber]


def countkeywords(file_name,keywords):
    x=readfile(file_name).count(keywords)
    return x



def get_pdb_from_pdb(file_name,framenumber):
    
    keywords=key_words
    if totalnumber >= framenumber:   
        th=0
        pdb=[]
        srckey=key_words_head
        srckey1=key_words
        for i in range(len(x)):
            if srckey1 not in x[i]:
                th=th+1
            else:
                th=th+1
                break
        start=framenumber*th 
        end=(framenumber+1)*th 
        pdb=x[start:end]
        with open(file_container_name+str(file_name.split(".")[0])+"_"+str(framenumber)+generate_random_string(8)+".pdb","a+") as f:
            f.writelines(pdb)
            print(str(file_name.split(".")[0])+"_"+str(framenumber)+generate_random_string(8)+".pdb"+" Generated!")
def getpdb(t):
    get_pdb_from_pdb(file_name,t)
    return 0



def main(file):
    time0=time.time()
    global file_name
    file_name=file.input
    global x
    y=readfile(file_name)
    x=y[0]

    global totalnumber
    keywords=key_words
    totalnumber=y[1]

    if file.num == "all":
        keywords=key_words
        number = totalnumber
    else:
        number=int(file.num)

    if number == 0:
        print("please input a larger number")
    else:
        keywords=key_words
        print("\n\nREAD\n"+str(file_name)+"  "+str(keywords)+"INPUT FILE Total Frame Number is "+str(totalnumber)+"\n\n")
        if number > totalnumber:
            print("please input a smaller number")
        else:
            samples=random.sample(range(totalnumber),number)
            if os.path.exists(file_container_name):
                shutil.rmtree(file_container_name)
                print(file_container_name+" exists, remove it and rebuild it!")
                os.mkdir(file_container_name)
            else:
                os.mkdir(file_container_name)
            arg=[]
            pool = mul.Pool(CORES)
            arg=samples
            rel  = pool.map(getpdb,arg)
            if file_container_name in os.listdir("./"):
                print("yes")
                os.chdir(file_container_name)
                subprocess.call('pwd',shell=True)
                os.chdir("../")
                print("files OK!")
    time1=time.time()
    print("Total time is "+str(time1-time0)+" s")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="check cif lattice, if not reach value, supercell it until to get it")
    parser.add_argument("-input", help="input: filename in pdb file,relative")
    parser.add_argument("-num", help="withdraw number, can be 'all' or a number")

    fileinput = parser.parse_args()
    
    main(fileinput)
    

