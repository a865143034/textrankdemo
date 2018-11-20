#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###TODO: 日志
import sys
import collections
from operator import itemgetter
import jieba.posseg as pseg
from aip import AipNlp
from jieba import analyse
from dbtest import getperson_mp

APP_ID = '*'
API_KEY = '*'
SECRET_KEY = '*'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

#写的一个类
class UndirectWeightedGraph:
    d = 0.85
    def __init__(self):
        self.graph = collections.defaultdict(list)

    def addEdge(self, start, end, weight):
        # use a tuple (start, end, weight) instead of a Edge object
        self.graph[start].append((start, end, weight))
        self.graph[end].append((end, start, weight))



    #该函数需要后期执行
    def rank(self):
        #如下是建立字典
        ws = collections.defaultdict(float)#是一个映射
        outSum = collections.defaultdict(float)

        #总共有多少个点
        wsdef = 1.0 / len(self.graph)

        for n, out in self.graph.items():
            ws[n] = wsdef#????
            #ws[n]=1
            outSum[n] = sum((e[2] for e in out), 0.0)#某点发出的权重相加

        #ws就是结果向量？
        #矩阵相乘
        for x in range(10):  # 10 iters
            for n, inedges in self.graph.items():
                s = 0
                #矩阵相乘的操作
                for e in inedges:#入边
                    s += e[2] / outSum[e[1]] * ws[e[1]]

                ws[n] = (1 - self.d) + self.d * s

        (min_rank, max_rank) = (sys.float_info[0], sys.float_info[3])

        for w in ws.values():
            if w < min_rank:
                min_rank = w
            elif w > max_rank:
                max_rank = w

        for n, w in ws.items():
            #归一化一下
            # to unify the weights, don't *100.
            ws[n] = (w - min_rank / 10.0) / (max_rank - min_rank / 10.0)
        #这里是还未排序的
        #print(ws)
        return ws



#这里才是排序算法
def textrank(sentence, topK=10, withWeight=False):
    """
    Extract keywords from sentence using TextRank algorithm.
    Parameter:
        - topK: return how many top keywords. `None` for all possible words.
        - withWeight: if True, return a list of (word, weight);
                      if False, return a list of words.
    """
    #pos_filt = frozenset(('ns', 'n','v','vn','PER','LOC','ORG'))
    pos_filt = frozenset(('ns', 'n','nr','nt','nw','nz','f','s','vd','LOC'))
    #pos_filt = frozenset(('ns', 'n'))
    g = UndirectWeightedGraph()
    cm = collections.defaultdict(int) #还是个dict，字典
    span = 5#窗口大小

    vec=client.lexerCustom(sentence)
    words=[]
    for x in vec['items']:
        if(x['ne']):
            words.append(("".join(x['basic_words']),x['ne']))
        else:
            words.append((x['basic_words'][0],x['pos']))


    ###这里是建图
    for i in range(len(words)):
        if words[i][1] in pos_filt:
            for j in range(i + 1, i + span):
                if j >= len(words):
                    break
                if words[j][1] not in pos_filt:
                    continue
                if(len(words[j][0])<=1):
                    continue
                cm[(words[i][0], words[j][0])] += 1

    for terms, w in cm.items():
        g.addEdge(terms[0], terms[1], w)

    nodes_rank = g.rank()#node_rank是一个字典

    if withWeight:
        tags = sorted(nodes_rank.items(), key=itemgetter(1), reverse=True)#reverse由大到小排序
    else:
        tags = sorted(nodes_rank, key=nodes_rank.__getitem__, reverse=True)

    if topK:
        return tags[:topK]
    else:
        return tags


###TODO:1、建立一张表把常见的词用表给过滤掉，手动看数据过滤； 2、最后的相邻词合并，代码在demostart.py中，还未来得及合并 3、以上是对textrank算法的重写 4、46号公司有问题，为什么跑不出来而且效率那么低

def diy():
    for i in range(1,101):##这里是company_id的编号
        f = open("/Volumes/Transcend/data2/text%s.txt"%(i), 'w')
        try:
            person_mp=getperson_mp(i)
            for key,value in person_mp.items():
                f.write(key[0]+" "+key[1]+":\n")
                wordlist=[]
                for sentence in value:
                    word = textrank(sentence, topK=20)
                    wordlist.extend(word)
                import collections
                obj=collections.Counter(wordlist)
                wlist=[]
                tmpwlist=obj.most_common(20)
                for i in tmpwlist:
                    wlist.append(i[0])
                ans="/".join(wlist)
                f.write(ans+"\n")
                f.flush()
        except:
            f.close()
            continue
        f.close()

if __name__ == '__main__':
    diy()

