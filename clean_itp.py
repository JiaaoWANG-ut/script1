def clean_itp_files(file_name,keywords):
    try:
        with open(file_name) as f:
            mol=f.readlines()
            print("\n\n\n\n"+str(file_name)+" read!\n\n\n")
    except:
        print("\n\n\n\nfilename invalid\n\n\n\n")

    def get_parts_notified(keywords):
            list_info=[]
            for i in range(len(mol)):
                if keywords in mol[i]:
                    for j in range(i,100000):
                        if "\n" !=  mol[j]:         #######区块选择标准######
                           # print(mol[j])
                            mol[j]=";"+str(mol[j])
                           # print(mol[j])
                        else:
                            print(mol)
                            with open(file_name,"a+") as f:
                                f.truncate(0)
                                f.writelines(mol)
                                print(f.readlines())
                            break
    get_parts_notified(keywords)
    return 0


import argparse
def main(file):
    file_name=file.input   #########
    keywords=file.keywords #########

    clean_itp_files(file_name,keywords)  #######
    print("\nFILE CLEANED!\n")           ####### 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make a section to be noted/invalid for GROMACS itp!")
    parser.add_argument("-input", help="File path, MUST Be .itp File")
    parser.add_argument("-keywords", help="keywords")
    file = parser.parse_args()
    main(file)
