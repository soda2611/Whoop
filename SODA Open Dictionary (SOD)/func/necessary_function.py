import socket
import ctypes

def get_scaling_factor():
    scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
    return scaleFactor

def get_config():
    with open("func/setting/setting.txt", "r", encoding="utf-8") as fi:
        setting=fi.readlines()
    settings={}
    for index in setting:
        option, properties=index.strip().split(": ")
        settings[option]=properties
    
    return settings

def check_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

def data():
    try:
        with open("data/word.txt", encoding="utf-8") as fi:
            word = [str(i) for i in fi.read().split()]
    except:
        with open("func/data/word.txt", encoding="utf-8") as fi:
            word = [str(i) for i in fi.read().split()]

    return word

def spelling_checker_for_SOD(you, word=data()):            
    you=you.lower()
    temp=[str(i) for i in you.split()]
    for x in temp:
        max=0
        replaces=''
        z=[]
        if x not in word:
            for y in word:
                t=0
                max=0
                if len(x)>=len(y):
                    for j in range(len(y)):
                        if x[j]==y[j]:
                            t+=1
                        elif x[j] in y:
                            l=y.find(x[j])
                            if j-l==1:
                                t+=1
                elif len(x)<=len(y):
                    for j in range(len(x)):
                        if x[j]==y[j]:
                            t+=1
                        elif x[j] in y:
                            l=y.find(x[j])
                            if l-j==1:
                                t+=1
                k=t/len(y)*100
                h=t/len(x)*100
                if (k>=50 and h>=50):
                    z.append(y)
            if len(z)!=0:
                for z1 in z:
                    t=0
                    if len(x)>len(z1):
                        for z2 in range(len(z1)):
                            if x[z2]==z1[z2]:
                                t+=2
                            elif x[j] in z1:
                                l=z1.find(x[j])
                                if j-l==1:
                                    t+=1
                            if x[0]==z1[0]:
                                t+=2
                            if x[-1]==z1[-1]:
                                t+=2
                    elif len(x)<len(z1):
                        for z2 in range(len(x)):
                            if x[z2]==z1[z2]:
                                t+=2
                            elif x[j] in z1:
                                l=z1.find(x[j])
                                if l-j==1:
                                    t+=1
                            if x[0]==z1[0]:
                                t+=2
                            if x[-1]==z1[-1]:
                                t+=2
                    elif len(x)==len(z1):
                        for z2 in range(len(z1)):
                            if x[z2]==z1[z2]:
                                t+=2
                            if x[0]==z1[0]:
                                t+=2
                            if x[-1]==z1[-1]:
                                t+=2
                    if len(x)==len(y):
                        t+=3
                    elif abs(len(x)-len(z1))==1:
                        t+=2
                    elif abs(len(x)-len(z1))==2:
                        t+=1
                    #k=t/len(z1)*100
                    if (x in z1) and (abs(len(x)-len(z1))==1):
                        replaces=z1
                        you=you.replace(x,replaces)
                        k=-1
                        break
                    if (k!=-1):
                        if (t>max):
                            max=t
                            replaces=z1
                if k==-1:
                    continue
                else:
                    you=you.replace(x,replaces)
    return you

if __name__=="__main__":
    pass