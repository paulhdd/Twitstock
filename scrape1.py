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

class StdOutListener(StreamListener):
   
    def on_data(self, data):

        all_data=json.loads(data)
        tweet=all_data['text']
        username = all_data["user"]["screen_name"]

        #Improve it with lemmetizing from nltk.

        good=['winners','winner','upside','sales up','very nice','nice','outstanding','bought','trending','trend','great','big','stunning','highes','buy','long','bull','aggressive','holding','popular','fire','outperform','happy','thanks','right','top gainer']
        bad=['never buy','shortsqueeze','downside','loss','slide','risk','flop','sold','selling','bad','wierd','sell','stop','bubble','bear','odd','down','downtrend','pullback','downgraded','bad','short','no profit','fall','put','not very']
        
        query_test=("INSERT INTO %s (time,username,tweet,sentiment) VALUES " % table_name)
        query_test+="(curdate(),%s,%s,%s);"
        c.execute (query_test, (username,tweet,score(tweet,good,bad)))
        conn.commit()

        output = open('tweet_data_'+sys.argv[1]+'.txt','a')
        output.write(str(score(tweet,good,bad)))
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