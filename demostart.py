#coding:utf-8
import re
from aip import AipNlp
from numpy import *
import numpy as np
from robots import get_text
from dbtest import getstr
K=5
T=10

APP_ID = '*'
API_KEY = '*'
SECRET_KEY = '8'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

#sentence作为输入变量
sentence=getstr()
vec=[]
s=set()
ans=client.lexerCustom(sentence)
for i in ans['items']:
    if i['ne'] or i['pos']=="n":
        tmp=i['basic_words'][0]
        vec.append(tmp)
        s.add(tmp)

lenth=len(s)

map1={}
map2={}
num=0
for i in s:
    map1[i]=num
    map2[num]=i
    num+=1

#a1=zeros((3,3))

#建立图矩阵
M = mat([[0 for i in range(lenth)] for i in range(lenth)])
if lenth<K:
    for i in range(lenth):
        for j in range(lenth):
            M[map1[vec[i]],map1[vec[j]]]=M[map1[vec[j]],map1[vec[i]]]=1
else:
    for i in range(K):
        for j in range(K):
            M[map1[vec[i]],map1[vec[j]]]=M[map1[vec[j]],map1[vec[i]]]=1
    for i in range(K,lenth):
        for j in range(K-1):
            M[map1[vec[i-j]],map1[vec[i]]]=M[map1[vec[i]],map1[vec[i-j]]]=1
print(M)
'''
for i in range(lenth):
    num=0
    for j in range(lenth):
        num=num+M[j,i]
    if num==0:
        continue
    for j in range(lenth):
        M[j,i]=M[j,i]/num
'''

#print(M)
PR=mat([1 for i in range(lenth)]).T

for iter in range(10):
    PR=0.15+0.85*M*PR

PR=PR.tolist()
for i in range(len(PR)):
    PR[i].append(i)
PR=sorted(PR,reverse=True)
print(PR)
A=[0 for i in range(lenth)]
for i in range(T):
    A[PR[i][1]]=1

ansA=[]
flag=False
tmpstr=""
for i in range(lenth):
    if A[i]==1:
       tmpstr+=map2[PR[i][1]]
       flag=True
    else:
        if flag==True:
            flag=False
            ansA.append(tmpstr)
            tmpstr=""
        else:
            tmpstr=""
            flag=False
            continue
if tmpstr!="":
    ansA.append(tmpstr)
#print(A)
print(ansA)
###呈现结果

'''
ans=[]
for i in range(10):
    ans.append(map2[PR[i][1]])
    #print(map2[PR[i][1]],end=" ")
#for i in range(10):

print(ans)
'''


###TODO：先实现出来，然后再进行优化