import re
from bs4 import BeautifulSoup,Comment
import requests

def getcontentfromweb(src):
    obj = requests.get(src)
    return obj.text

def filter_tags(html_str):
    soup =BeautifulSoup(html_str,'lxml')
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    [comment.extract() for comment in comments]
    reg1 = re.compile("<[^>]*>")
    content = reg1.sub('', soup.prettify()).split('\n')
    return content

def getcontent(lst):
    lstlen = [len(x) for x in lst]
    threshold=50
    startindex = 0
    maxindex = lstlen.index(max(lstlen))
    endindex = 0
    for i,v in enumerate(lstlen[:maxindex-3]):
        if v> threshold and lstlen[i+1]>5 and lstlen[i+2]>5 and lstlen[i+3]>5:
            startindex = i
            break
    for i,v in enumerate(lstlen[maxindex:]):
        if v< threshold and lstlen[maxindex+i+1]<10 and lstlen[maxindex+i+2]<10 and lstlen[maxindex+i+3]<10:
            endindex = i
            break
    content =['<p>'+x.strip()+'</p>' for x in lst[startindex:endindex+maxindex] if len(x.strip())>0]
    return content

def run(url):
    ctthtml=getcontentfromweb(url)
    content =filter_tags(ctthtml)
    newcontent =getcontent(content)
    ctt =''.join(newcontent)
    return ctt

def process(text):
    regex=r"(?is)<.*?>"
    reobj = re.compile(regex)
    result, number = reobj.subn("", text)
    return result

def extractfun(url):
    ans=run(url)
    result=process(ans)
    return result

if __name__=='__main__':
    ans=run('http://www.sohu.com/a/58094870_121315')
    #print(ans)
    result=process(ans)
    print(result)