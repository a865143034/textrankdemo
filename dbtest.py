#coding:utf-8
import pymysql
from robots import get_text
from zhengwenextract import extractfun
import re

def get_mp(num):
    db = pymysql.connect("*", "*", "*", "*")
    cursor = db.cursor()
    sql="select * from org_chart_origin where company_id='%s';"%(num,)
    cursor.execute(sql)
    datalist=cursor.fetchall()
    mp={}
    for data in datalist:
        mp[(data[3],data[4])]=1
    db.close()
    return mp

def getperson_mp(num):
    mp=get_mp(num)
    person_mp={}
    db = pymysql.connect("*", "*", "*", "*")
    cursor = db.cursor()
    for key,value in mp.items():
        strlist=[]
        sql="select * from org_chart_origin where company_id='%s' and person_name='%s' and title='%s';"%(num,key[0],key[1])
        cursor.execute(sql)
        datalist=cursor.fetchall()

        for data in datalist:
            from robots import getHTMLText
            tmp=getHTMLText(data[8])
            tmp=cleantxt(tmp)
            str=data[6]*4+ data[7]*2+ tmp
            str=cleantxt(str)
            if str=="": continue
            strlist.append(str)
            #print(str)
        person_mp[key]=strlist
    #print(person_mp)
    db.close()
    return person_mp

def cleantxt(raw):
    fil = re.compile(u'[^\u4e00-\u9fa5]+', re.UNICODE)
    return fil.sub(' ', raw)

'''
def cleantxt(raw):
    fil = re.compile(u'[\u4e00-\u9fa5]+', re.UNICODE)
    return fil.sub(' ', raw)
'''

if __name__=='__main__':
    ans=getperson_mp(12)
    num=0
    for key,value in ans.items():
        print(key)
        print(len(value))
        num+=len(value)
    print(num)
    #print(ans)