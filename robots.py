#coding:utf-8
import requests
from bs4 import BeautifulSoup
import bs4
from newspaper import Article
headers = {
    'User-Agent':'Chrome/68.0.3440.106'
}

def getHTMLText(url):
    try:
        r=requests.get(url,headers=headers)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ''

def process(html):
    soup=BeautifulSoup(html,'lxml')
    text=soup.get_text()
    #print(soup.prettify())
    return text


def get_text(url):
    #url="https://blog.csdn.net/J1angLei/article/details/78344068?locationNum=5&fps=1"
    try:
        news = Article(url)
        news.download()
        news.parse()
        return news.text
    except:
        return ""

#ans=get_text(111)
#print(ans)