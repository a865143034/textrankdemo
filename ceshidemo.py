#coding:utf-8
import numpy
#from numpy import *
import collections
import sys
'''
lenth=3
M = mat([[0 for i in range(lenth)] for i in range(lenth)])
M[1,0]=M[2,0]=1
M[0,1]=M[0,2]=1
for i in range(lenth):
    num=0
    for j in range(lenth):
        num=(float)(num)+M[j,i]
    if num==0:
        continue
    for j in range(lenth):
        M[j,i]=(float)(M[j,i])/num
print(M)
'''
'''
graph = collections.defaultdict(list)
graph[3]=1
graph[2]=1
graph[5]=1
print(len(graph))
'''
#ans=(1 for i in range(10))
ans=sum((1 for i in range(9)), 0.0)
print(ans)
'''
for i in ans:
    print(i)
'''
print(sys.float_info)
print(sys.float_info[0], sys.float_info[3])


A=["213","457"]
print("".join(A))

print(len('以'))