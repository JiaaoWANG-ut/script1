import argparse

#key_words="ENDMDL\n"
#key_words_head="REMARK    GENERATED BY TRJCONV\n"
#mol=open("md.pdb").readlines()
#keywords=key_words
#totalnumber=mol.count(keywords)

key_words="ENDMDL\n"
key_words_head="REMARK    GENERATED BY TRJCONV\n"

def get_pdb_from_pdb(framenumber):

    keywords=key_words
    if totalnumber >= framenumber:
        th=0
        pdb=[]
        srckey=key_words_head
        srckey1=key_words
        for i in range(len(mol)):
            if srckey1 not in mol[i]:
                th=th+1
            else:
                th=th+1
                break
        start=framenumber*th
        end=(framenumber+1)*th
        pdb=mol[start:end]
    return pdb

    pdb_all=[]

    for i in range(totalnumber):
        pdb=get_pdb_from_pdb(i)
        pdb_all.append(pdb)
        print("frame number: ",i)

    #print(pdb)



    sorted_a = sorted(pdb_all, key=len)

    fold_a=[]

    for i in sorted_a:
        for j in i:
            fold_a.append(j)

    for i in sorted_a:
        print(len(i))

    print("writting")
    with open("md_sorted.pdb", "w+") as t:
        t.writelines(fold_a)
    print("finished")


def main(file):
    global file_name
    file_name=file.input
 #   number=file.num
    #key_words="ENDMDL\n"
    #key_words_head="REMARK    GENERATED BY TRJCONV\n"
    global mol
    mol=open(file_name).readlines()
    keywords=key_words
    global totalnumber
    totalnumber=mol.count(keywords)

    pdb_all=[]

    for i in range(totalnumber):
        pdb=get_pdb_from_pdb(i)
        pdb_all.append(pdb)
        print("frame number: ",i)

    #print(pdb)



    sorted_a = sorted(pdb_all, key=len)

    fold_a=[]

    for i in sorted_a:
        for j in i:
            fold_a.append(j)

    for i in pdb_all:
        print("file size(atom number) (approxi)",len(i))

    print("writting")
    with open("md_sorted.pdb", "w+") as t:
        t.writelines(fold_a)
    print("finished")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="check cif lattice, if not reach value, supercell it until to get it")
    parser.add_argument("-input", help="input: filename in pdb file,relative")
    #parser.add_argument("-num", help="withdraw number, can be 'all' or a number")

    fileinput = parser.parse_args()

    main(fileinput)



