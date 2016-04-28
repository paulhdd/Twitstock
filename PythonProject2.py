
# coding: utf-8

# In[51]:

def evolution(month,day,year,ticker):
    #date format    07 29 15 for 2015
    #ticker format with '   '
    import re
    import urllib.request as ul
    from bs4 import BeautifulSoup
    #date format    07 29 15 for 2015 
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
    print('The live price of '+ticker.upper() +' is at $'+live[0])

evolution(13,7,15,'amzn')

