import subprocess
import os
import multiprocessing as mul
import time

import smtplib
from email.header import Header
from email.mime.text import MIMEText
###Jiaao WANG@Henkelman Group

###A Coding for sbatching High-throughput submitting TASKS in slurm.
###PUT THIS FILE TO the filelist, and python3 sbatch.py
###The command will be automatically execuated.
###Run 1 time, sbatch all file, if the file is in LIST,RUNNING, or Finished
###The submit would be skipped!
CORES=20
global command 
global get_squeue
command="cp ~/scripts/cp2k.slurm .;. /etc/profile > /dev/null 2>&1;sbatch cp2k.slurm >sbatchinfo.dat 2>&1"
get_squeue="squeue -u jiaao>>1.dat"
#for i in os.listdir("./"):
def get_workdir():
    subprocess.call(get_squeue,shell=True)
    dir=[]
    with open("1.dat") as f:
        line=f.readlines()
        #print(line)
        for i in line:
            if "PD" in i.split() or "R" in i.split() or "CG" in i.split():
                #print(i.split()[0])
                dir.append(i.split()[0])
            else:
                sub=1
#print(dir)
###遍历列表得到工作目录
    workdir=[]
    for i in dir:
        sub="scontrol show job "+str(i)+"|grep WorkDir>>2.dat"
        T=subprocess.call(sub,shell=True)
    if os.path.exists("2.dat"):
        with open("2.dat") as f:
            line=f.readlines()
            for i in line:
                    workdir.append(i.split("=")[1].split("\n")[0])
    #print(workdir)
    if os.path.exists("2.dat"):
        subprocess.call("rm 2.dat",shell=True)
    
    subprocess.call("rm 1.dat",shell=True)
    #print(workdir,'111')
    return workdir

global workdir
workdir=get_workdir()
#print(workdir)#########################################################################



def get_complete(i): ###检查单个文件中是否完成计算，如果没有，则重新提交，
    if os.path.exists(i):
        if os.path.exists(i+"/ll_out"):
            os.chdir(i)
            subprocess.call('rm complete',shell=True)
            subprocess.call('grep "PROGRAM ENDED AT" ll_out>complete',shell=True)
            #subprocess.call("pwd;cat complete",shell=True)
            if os.path.getsize("complete")==0:
                #subprocess.call("cat complete",shell=True)
                #print(str(i)+" sbatched, but not compelte, tried resubmitted")
                #time0=time.time()
                subprocess.call(command,shell=True)
                #time1=time.time()
                #print(time1-time0)
                with open("sbatchinfo.dat") as f:
                    info=f.readlines()
                    for j in info:
                        if j.find("Submitted") == -1:
                            sub=1
                            #print(str(i)+"SKIP DUE TO QUEUE LIMIT")
                        else:
                            print(str(i)+" Failed, Task RESubmitted")
                            sub=1
                            break
            os.chdir("..")
        else:
                #print(str(i)+" has no ll_out, try to resubmit")
            os.chdir(i)
            sub=1
            subprocess.call(command,shell=True)
            with open("sbatchinfo.dat") as f:
                info=f.readlines()
                for j in info:
                    if j.find("Submitted") == -1:
                        sub=1
                            #print(str(i)+"SKIP DUE TO QUEUE LIMIT")
                    else:
                        print(str(i)+" Failed, Task RESubmitted")
                        sub=1
                        break

                #subprocess.call("cat complete",shell=True)
                #print(str(i)+"complete")
            os.chdir("../")
global sub
sub=0
def sbatch(i):
    #print(os.path.abspath(i))
    if os.path.isdir(i):
        if "Finished" in os.listdir(i):
            #print(str(i)+"Finished file EXIST")
            sub=1
            if os.path.exists(i+"/ll_out"):
                #print(os.path.abspath(i))
                #print(workdir)################################################################
                if os.path.abspath(i) in workdir:
                    sub=1
                    #print("FOUND Finished, but in working, skip")
                else:
                    get_complete(i)
                    #print("FOUND Finished, but not working, skip")
                #os.chdir(i)
                #subprocess.call('grep "PROGRAM ENDED AT" ll_out>complete',shell=True)
                #subprocess.call("pwd;cat complete",shell=True)
                #if os.path.getsize("complete")==0:
                 #   get_complete("..")
                #os.chdir("../")
            #print("SKIP SUBMIT,"+str(i)+" DUE TO JOB FINSHED!")

        elif "Started" in os.listdir(i):
            if os.path.exists(i+"/ll_out"):
                if os.path.abspath(i) in workdir:
                    sub=1
                else:
                    get_complete(i)
            else:
                #print(i,"START file EXIST, but no ll_out")
                if os.path.abspath(i) in workdir:
                    sub=1
                else:
                    get_complete(i)

        elif os.path.abspath(i) in workdir:
            #print("SKIP SUBMIT,"+str(i)+" DUE TO PD")
            sub=1
            #print(workdir)
        else:
            os.chdir(i)
            
            subprocess.call(command,shell=True)
            #subprocess.call("cp ~/scripts/cp2k.slurm .;sbatch cp2k.slurm >sbatchinfo.dat 2>&1",shell=True)
            #subprocess.call("pwd",shell=True)
            #os.chdir("../")
            with open("sbatchinfo.dat") as f:
                info=f.readlines()
                for j in info:
                    if j.find("Submitted") == -1:
                        #print(j.find("Submitted"))
                        sub=1
                        #print(str(i)+"SKIP DUE TO QUEUE LIMIT")
                        #break
                    else:
                        print(str(i)+" Submitted")
                        #print(j.find("Submitted"))
                        sub=1
                        #print("SKIP DUE TO QUEUE LIMIT")
                        break
            os.chdir("../")

pool=mul.Pool(CORES)
arg=os.listdir("./")
start=time.time()
rel=pool.map(sbatch,arg)

end=time.time()
print("Total Time:",end-start)
print("Try to Change CORES to accelerate the process, Current:",CORES)
total=0
finished=0
for i in os.listdir("./"):
    if os.path.isdir(i):
        os.chdir(i)
        total+=1
        if os.path.exists("Finished"):
            #total+=1
            sub=1
            subprocess.call('grep "PROGRAM ENDED AT" ll_out>complete',shell=True)
            if os.path.exists("complete"):
                if os.path.getsize("complete")!=0:
                    finished+=1
        else:
            if os.path.isdir(i):
                sub=1
                #total+=1
        os.chdir("../")

print("Finished/Total",finished,"/",total)
if finished==total:
    print("Congradulations, High-Throughout Series Finished!")

subprocess.call(get_squeue,shell=True)
ttask=0
pdtask=0
rtask=0
with open("1.dat") as f:
    line=f.readlines()
    for i in line:
        if "PD" in i.split():
            pdtask+=1
            ttask+=1
        elif "R" in i.split():
            rtask+=1
            ttask+=1
        else:
            ttask+=1
ttask=ttask-1
#print("QUEUE STATE")
print("PENDING/TOTAL:",pdtask,"/",ttask)
print("RUNNING/TOTAL:",rtask,"/",ttask)
subprocess.call("rm 1.dat",shell=True)
#print(sub)
###How many skipped



def email(text):
    # 发送方设置
    mail_host = "smtp.exmail.qq.com"
    mail_user = "shenglin@aleeqaq.cc"
    mail_pass = "89JZCRp6XA4RQsBz"
    # 接收方账号
    receiver_mail = 'wangjiaao0720@utexas.edu'
    # 从msg文件读取内容：只读取第一行！！！
    raw_text = text
    # 邮件内容设置
    msg = MIMEText(raw_text, 'plain', 'utf-8')
    msg['From'] = Header('Shenglin,Xu')
    msg['To'] = Header('Xu,Shenglin')
    msg['Subject'] = Header('Longstar6 Service')
    # 建立连接并发送
    server = smtplib.SMTP_SSL(mail_host)
    server.connect(mail_host, 465)
    server.login(mail_user, mail_pass)
    server.sendmail(mail_user, receiver_mail, msg.as_string())
    server.quit()

email("PENDING/TOTAL:"+str(pdtask)+"/"+str(ttask)+"\nRUNNING/TOTAL:"+str(rtask)+"/"+str(ttask)+"\nFinished/Total:"+str(finished)+"/"+str(total))

###QUEUE STATE[/Total Jobs]

###Highthroughput Filelist
###[Finished/Total jobs]


    #os.remove("output.txt")
