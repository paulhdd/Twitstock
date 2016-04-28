from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymysql
import time
import json
import sys
import re
import urllib.request as ul
from bs4 import BeautifulSoup

conn = pymysql.connect(host="localhost",port=3306,user="root",passwd="",charset='utf8')
c = conn.cursor()

c.execute('CREATE DATABASE if not exists tweet_data')
c.execute('USE tweet_data')
c.execute('SET NAMES utf8;')
c.execute('SET CHARACTER SET utf8;')
c.execute('SET character_set_connection=utf8;')

table_name=sys.argv[1].replace (" ", "_")
query='CREATE TABLE if not exists %s (time varchar(30),username varchar(40), tweet varchar(300),sentiment varchar(10));' % table_name

c.execute(query)

consumer_key = "oWwj4n238NZ8Y7EvuaEDxy1sa"
consumer_secret = "eKZQnTjKxRh1ZMjueF7excNwBHMuqkQpbxvKtUj2Y2UXHFUbd0"
access_token= "3397148596-udefnWb7gUddt6ADanLCNV6opCXhglJfVMV5Kai"
access_token_secret = "lVfKlGnd9SK0HdJ6giGDFbzz3dO3LU96Uk7ili4mUoXVB"

def score(text, wgood,wbad):
    count=0
    for oneWord in wgood:
        if oneWord in text.lower():
            count+=1
    for oneWord in wbad:
        if oneWord in text.lower():
            count-=1
    if count>0:
        return 1
    elif count<0:
        return -1
    elif count==0:
        return 0

def liveprice(ticker):
    #date format    07 29 15 for 2015
    #ticker format with '   '

    #date format    07 29 15 for 2015
    month=int(time.strftime('%m'))+1
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

class StdOutListener(StreamListener):
   
    def on_data(self, data):

        all_data=json.loads(data)
        tweet=all_data['text']
        username = all_data["user"]["screen_name"]

        #Improve it with lemmetizing from nltk.

        good=['building', 'reaffirmed', 'profits', 'trending', 'top', 'gains', 'bounce', 'high', 'oversold','winners','winner','upside','sales up','very nice','nice','outstanding','bought','trending','trend','great','big','stunning','highes','buy','long','bull','aggressive','holding','popular','fire','outperform','happy','thanks','right','top gainer']
        bad=['bumpy', 'ugly', 'danger', 'risky', 'troubles', 'never buy', 'low', 'bottom', 'selloff', 'sell-off', 'worthless', 'downgrade', 'ugly', 'ugliest','shortsqueeze','downside','loss','slide','risk','flop','sold','selling','bad','wierd','sell','stop','bubble','bear','odd','down','downtrend','pullback','downgraded','bad','short','no profit','fall','put','not very']
        
        query_test=("INSERT INTO %s (time,username,tweet,sentiment) VALUES " % table_name)
        query_test+="(curdate(),%s,%s,%s);"
        c.execute (query_test, (username,tweet,score(tweet,good,bad)))
        conn.commit()

        output = open('tweet_data_'+sys.argv[1]+'.txt','a')
        output.write(str(score(tweet,good,bad))+' '+str(liveprice(sys.argv[1][1:])))
        output.write('\n')
        output.close()
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=[sys.argv[1]])