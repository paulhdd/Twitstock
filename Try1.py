import time
import json
import sys
import re
import urllib.request as ul
from bs4 import BeautifulSoup
def liveprice(ticker):
    #date format    07 29 15 for 2015
    #ticker format with '   '

    #date format    07 29 15 for 2015
    month=int(time.strftime('%m'))
    day=int(time.strftime('%d'))
    year=int(time.strftime('%Y'))
    ticker=ticker.lower()
    url='http://finance.yahoo.com/q/hp?s='+ str(ticker) +'&a='+str(month-1)+'&b='+str(day)+'&c='+str(year)+'&d='+str(month-1)+'&e='+str(day)+'&f='+str(year)+'&g=d'
    url_response=ul.urlopen(url,timeout=5)
    yahoo_data = BeautifulSoup(url_response)
    data=yahoo_data.findAll('td',{"class":"yfnc_tabledata1" })
    pattern='yfnc_tabledata1">(.+?)</td>'
    regex = re.compile(pattern)
    before=regex.findall(str(data[1]))
    after=regex.findall(str(data[2]))
    data1=yahoo_data.findAll('span')
    pattern1='84_'+ticker+'">(.+?)</span>'
    regex1=re.compile(pattern1)
    live=regex1.findall(str(data1))
    
    
    pattern2='yfs_p43_'+ticker+'">\((.+?)\)</span>'
    regex2=re.compile(pattern2)
    down=regex2.findall(str(data1))
    return live[0]

liveprice('amzn')