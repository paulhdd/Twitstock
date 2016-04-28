import json
import pandas as pd
import matplotlib.pyplot as plt

tweets_data_path = '/Users/phd/Documents/Cours/Columbia/Data_analysis_python/Project/output.txt'
tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append((tweet['text'],tweet['created_at']))
    except:
        continue

print(len(tweets_data))

#Removing duplicate tweets/RT

tweets_data=list(dict((x[0],x) for x in tweets_data).values())

df=pd.DataFrame(tweets_data, columns=['text','date'])
print(df['text'])