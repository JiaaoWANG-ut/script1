####INPUT 打分类型 打分阈值
####OUTPUT filtered_pdb files
import argparse
import os
import shutil
import multiprocessing as mul
import time


def readfile(file_name):  ##readfile get list
    try:
        with open(file_name) as f:
            mol=f.readlines()
            #print("\n\n\n\n"+str(file_name)+" read!\n\n\n")
    except:
        print("\n\n\n\nfilename invalid\n\n\n\n")
    ######读取完了文件为mol，目前获取文件中关键字区块信息
    return mol


def distance(x1,y1,z1,x2,y2,z2):
    x1,y1,z1,x2,y2,z2=float(x1),float(y1),float(z1)\
        ,float(x2),float(y2),float(z2)
    dis=float(((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**0.5)
    #print(dis)
    return round(dis,2)

def get_s1(mol): 
    #s1 score,  determined by [Li-anyelement] * Guassian
    neiborlist_collection=[]
    #cutoff=6 #Angs
    print("s1, Cutoff: ", str(cutoff))
    keyword="LI"
    keywordlist=[]
    total=[]
    for i in range(len(mol)):
        if keyword in mol[i]:
            keywordlist.append(keyword)
            #print(keyword+" "+str(len(keywordlist))+" found\n")
            neighbor_list=[]
            total_score=[]
            for j in range(len(mol)):
                if "MOL" in mol[j]:    ###此处的1是pdb文件读取格式控制
                    #print(mol[j])
                    dist=distance(\
                        mol[i].split()[6],\
                        mol[i].split()[7],\
                        mol[i].split()[8],\
                        mol[j].split()[6],\
                        mol[j].split()[7],\
                        mol[j].split()[8])
                    if dist<=cutoff and dist>0.5 :
                        #print(dist)
                        
                        #score=cutoff**2*math.exp(-(dist/2.5)**2)
                        score=1/(((dist-0.5)/5)**3)
                           ###打分函数###需要调
                        #print(score)
                        total_score.append(score)
                        
                        #print("\n")
            #print(sum(total_score))
            total.append(sum(total_score)**2)
    return sum(total)

def get_s2(mol):
    ###OUTPUT s2 score,  determined by [Li-O] RDF * Guassian
    neiborlist_collection=[]
    #cutoff=4 #Angs
    #print("s2, Cutoff: ", str(cutoff))
    keyword="LI"
    keywordlist=[]
    total=[]
    for i in range(len(mol)):
        if keyword in mol[i]:
            keywordlist.append(keyword)
            #print(keyword+" "+str(len(keywordlist))+" found\n")
            neighbor_list=[]
            total_score=[]
            for j in range(len(mol)):
                
                if "MOL" in mol[j] and mol[j].split()[2]=="O":    ###此处的1是pdb文件读取格式控制
                    #print(mol[j].split()[2])
                    dist=distance(\
                        mol[i].split()[6],\
                        mol[i].split()[7],\
                        mol[i].split()[8],\
                        mol[j].split()[6],\
                        mol[j].split()[7],\
                        mol[j].split()[8])
                    if dist<=cutoff and dist>0.5:
                        #print(dist)
                        
                        #score=cutoff**2*math.exp(-(dist/2.5)**2)
                        score=1/(((dist-0.5)/5)**3)
                           ###打分函数###需要调
                        #print(score)
                        total_score.append(score)
                        
                        #print("\n")
            #print(sum(total_score))
            total.append(sum(total_score)**2)
    return sum(total)


def get_s3(mol):
    #OUTPUT s3 score,  Cutoff内，其中的Li-O平均配位数
    neiborlist_collection=[]
    #global cutoff
    cutoff=2.5 #Angs
   # print("s3, Cutoff: ", str(cutoff))
    keyword="LI"
    keywordlist=[]
    total=[]
    for i in range(len(mol)):
        if keyword in mol[i]:
            keywordlist.append(keyword)
            #print(keyword+" "+str(len(keywordlist))+" found\n")
            neighbor_list=[]
            total_score=[]
            for j in range(len(mol)):
                
                if "MOL" in mol[j] and mol[j].split()[2]=="O":    ###此处的1是pdb文件读取格式控制
                    #print(mol[j].split()[2])
                    dist=distance(\
                        mol[i].split()[6],\
                        mol[i].split()[7],\
                        mol[i].split()[8],\
                        mol[j].split()[6],\
                        mol[j].split()[7],\
                        mol[j].split()[8])
                    if dist<=cutoff and dist>0.5:
                        #print(dist)
                        
                        #score=cutoff**2*math.exp(-(dist/2.5)**2)
                        score=1
                           ###打分函数###需要调
                        #print(score)
                        total_score.append(score)
                        
                        #print("\n")
            #print(sum(total_score))
            total.append(sum(total_score)**2)
            #print(sum(total))
            #print(len(total))
    return sum(total)/len(total)

def build_docu(filename):
    filename=filename
    if os.path.exists(filename):
        shutil.rmtree(filename)
        print(str(filename)+" exists, remove it and rebuild it!")
        os.mkdir(filename)
    else:
        os.mkdir(filename)
        print(str(filename)+" built!\n")


def get_score(i):
    # new_file_name=str(scoring_type)+".dat"
    new_file_name="s3.dat"
    cutoff=2.5
    if ".pdb" in i: 
            file_name=i
            print(i,"READ!")
            mol=readfile(file_name)   
            if mol: 
                #print("s3")
                with open(new_file_name,"a+") as f:
                    f.writelines(file_name+"\n")
                    f.writelines(str(get_s3(mol))+"\n")
                        
                # elif scoring_type=="s2":
                #     #print("s2")
                #     with open(new_file_name,"a+") as f:
                #         f.writelines(file_name+"\n")
                #         f.writelines(str(get_s2(mol))+"\n")
                # elif scoring_type=="s1":
                #     #print("s1")
                #     with open(new_file_name,"a+") as f:
                #         f.writelines(file_name+"\n")
                #         f.writelines(str(get_s1(mol))+"\n")
                

def get_scoring_file(file):
    scoring_type=file.scoring
    new_file_name=str(scoring_type)+".dat"

    if new_file_name in os.listdir("./"):
        #print("yes")
        os.remove(new_file_name)

    # for i in os.listdir("./"):
    #     get_score(i)
    start=time.time()

    pool=mul.Pool(128)
    arg=os.listdir("./")
    rel = pool.map(get_score,arg)

    end=time.time()
    print("\nTime:",end-start,"\n")
        #print(str(scoring_type)+" generated!")
    count=readfile(new_file_name)
    #print(count)
    count_num=[]
    for i in range(len(count)):
        if "pdb" not in count[i]:
            if float(count[i].split('\n')[0]):
                count_num.append(float(count[i]))
    print("Min Value: "+str(min(count_num)))
    print("Max Value: "+str(max(count_num)))
        


def get_filtered(threshold):
    file_name=scoring_file_name
    mol=readfile(file_name)
    threshold=float(threshold)
    transferfile="filtered_"+file_name.split(".")[0]+"_"+str(threshold)
    build_docu(transferfile)

    for i in range(len(mol)):
        if "pdb" not in mol[i]:
            if float(mol[i].split('\n')[0]):
                #print(mol[i].split('\n')[0]," Read!")
                if float(mol[i].split('\n')[0])>threshold: ###scoring筛选条件
                    
                    #print(mol[i-1].split('\n')[0]+" has been transfered to "+transferfile+" !")
                    shutil.copy(str(mol[i-1].split('\n')[0]),transferfile)
                    #print(float(mol[i].split('\n')[0]))
    screened_pdb_num=float(len(os.listdir(transferfile)))
    original_pdb_num=float(len(mol))
    print("")
    print(str(screened_pdb_num/original_pdb_num*100)+"% frames have been screened out! \n Set Cutoff can result in more selctions")
    
    



def main(file):
    scoring_type=file.scoring
    print(scoring_type)
    global cutoff
    cutoff=2.5 #Angs

    get_scoring_file(file)


    new_file_name=str(file.scoring)+".dat"
    global scoring_file_name
    scoring_file_name=new_file_name
    threshold=file.threshold
    #print("CUTOFF: "+str(cutoff))
    get_filtered(threshold)
    
    print("Method: ", scoring_type)
    print("Threshold: ", threshold)
    print("CUTOFF: ", cutoff)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="must put this script into as same class as the pdb file")
    parser.add_argument("-scoring", help="scoring type")
    parser.add_argument("-threshold", help="scoring type")
    fileinput = parser.parse_args()
    main(fileinput)
