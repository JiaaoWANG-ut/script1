import os
#file_name="ready.itp"

######从文件中获取信息########
def get_info_from_files(file_name,keywords):
    try:
        with open(file_name) as f:
            mol=f.readlines()
            print("\n\n\n\n"+str(file_name)+" read!\n\n\n")
    except:
        print("\n\n\n\nfilename invalid\n\n\n\n")

    ######读取完了文件为mol，目前获取文件中关键字区块信息
    def get_parts_info(keywords):
        list_info=[]
        for i in range(len(mol)):
            if keywords in mol[i]:
                for j in range(i,100000):
                    if "\n" !=  mol[j+1]:         #######区块选择标准######
                        list_info.append(mol[j+1])
                    else:
                        print(list_info)
                        break
        return list_info
    list_info=get_parts_info(keywords)
    print(file_name,list_info)
    return list_info



#######get ions number from "add_ions_number"########
if os.path.exists("add_ions_number"):
    print("add_ions_number READ!")
    with open("add_ions_number") as f:
        ions=f.readlines()
        ions=ions[0]
        print("ions number is: "+str(ions))

else:
    print("add_ions_number NOT EXIST!")
######################################################



#######get mols number from ""add_mols_number"########

if os.path.exists("add_mols_number"):
    print("add_mols_number READ!")
    with open("add_mols_number") as f:
        mols=f.readlines()
        mols=mols[0]
        print("mols number is: "+str(mols))

else:
    print("add_mols_number NOT EXIST!")

######################################################




def main(file):
    zeoitp=file.zeoitp
  #  molitp=file.molitp
    ionitp=file.ionitp
    top=file.top


##########Write##########
    defaults_label   = ['\n[ defaults ]\n\n']
    defaults         = get_info_from_files(top,"defa")

    atomtype_label   = ['\n[ atomtypes ]\n\n']

    atomtypes_ready  = get_info_from_files(zeoitp,"atomtypes")
   # atomtypes_mol    = get_info_from_files(molitp,"atomtypes")
    atomtypes_ion    = get_info_from_files(ionitp,"atomtypes")

    include          = ['\n#include "'+str(zeoitp)+'"\n','#include "'+str(ionitp)+'"\n','\n']

    system           = ['[ system ]\n'+'ready\n\n']

    molecules        = ['[ molecules ]\n'+str(zeoitp).split(".")[0]+'   1\n',str(ionitp).split(".")[0]+'    '+str(ions)+'\n']

    with open("ready_test.top","a+") as f:
        f.truncate(0)
        f.writelines(defaults_label)
        f.writelines(defaults)
        f.writelines(atomtype_label)
        f.writelines(atomtypes_ready)
       # f.writelines(atomtypes_mol)
        f.writelines(atomtypes_ion)
        f.writelines(include)
        f.writelines(system)
        f.writelines(molecules)

    import subprocess
    subprocess.call('cat ready_test.top',shell=True)
    print("\nready_test.top GENERATED!\n" )
    
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make a section to be noted/invalid for GROMACS itp!")
    parser.add_argument("-zeoitp", help="File path, MUST Be .itp File")
   # parser.add_argument("-molitp", help="File path, MUST Be .itp File")
    parser.add_argument("-ionitp", help="File path, MUST Be .itp File")
    parser.add_argument("-top", help="topfile must be sobtop generated ZEO.top {ready.top}")
    file = parser.parse_args()
    main(file)








