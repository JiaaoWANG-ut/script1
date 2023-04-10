import argparse
import numpy as np
import time
def readfile(file_name):  ##readfile get list
    try:
        with open(file_name) as f:
            mol=f.readlines()
            keywords="ENDMDL\n"
            totalnumber=mol.count(keywords)
            print("\n\n\n\n"+str(file_name)+" read!\n\n\n")
    except:
        print("\n\n\n\nfilename invalid\n\n\n\n")
    return mol


def countkeywords(mol,keywords):
    x=mol.count(keywords)
    return x

def getforce(mol):

    indexcollection=[]
    startindex=[]
    endindex=[]
    startrow=0
    endrow=0
    startkeyword="ATOMIC FORCES in [a.u.]"
    endkeyword="SUM OF ATOMIC FORCES"
    

    ####write startrow into a list
    
    for i in range(len(mol)):
        if startkeyword not in mol[i]:
            startrow+=1
        else:
            startrow+=1
            print(startrow)
            startindex.append(startrow)
    
    print("Write Start row")
    ###write endrow into a list

    for i in range(len(mol)):
        if endkeyword not in mol[i]:
            endrow+=1
        else:
            endrow+=1
            print(endrow)
            endindex.append(endrow)
    print("Write End row")


    for i in range(len(endindex)):
        indexcollection.append([startindex[i],endindex[i]])

    forcenpy=[]
    for i in range(len(indexcollection)):
        start=indexcollection[i][0]
        end=indexcollection[i][1]
        #print(mol[start:end],"\n")
        forcematrix=mol[start+2:end-1]

        forcelist=[]
        for j in range(len(forcematrix)):
            force=forcematrix[j].split()[3:6]
            forcelist.append(float(force[0]))
            forcelist.append(float(force[1]))
            forcelist.append(float(force[2]))
        forcenpy.append(forcelist)

    forcenpy=np.array(forcenpy)
    print(np.shape(forcenpy))
    print(forcenpy)
    return forcenpy


def main(file):
    time0=time.time()
    global file_name
    file_name=file.input
    mol=readfile(file_name)
    
    try:
        np.save("./force.npy",getforce(mol))
        print("force.npy Generated!")
    except:
        print("check the inputfile")
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert cp2k force and energy to dpmd readble format")
    parser.add_argument("-input", help="input")
    fileinput = parser.parse_args()
    main(fileinput)



