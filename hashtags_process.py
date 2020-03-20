#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
import re
import pandas as pd

filepath = "NRC-Hashtag-Emotion-Lexicon-v0.2.txt"
emolex_df = pd.read_csv(filepath,  names=["emotion", "hashtags", "association"], skiprows=45, sep='\t')
emolex_df.head(12)
'''
WORDS =["joy"]
COLLECTION_NAME='twitterdb_happy'  #350

WORDS =["fear"]
COLLECTION_NAME='twitterdb_fear'  #258
'''
WORDS =["anger"]
COLLECTION_NAME='twitterdb_angry'       #271
'''
WORDS =["surprise","sadness"]                   #319
COLLECTION_NAME='twitterdb_surprise'

WORDS =["anticipation","joy"]
COLLECTION_NAME='twitterdb_excitement'   #546

WORDS =["trust"]
COLLECTION_NAME='twitterdb_pleasant'  #511
'''



MONGO_HOST = 'mongodb://localhost:27017/'  # mongodb host path
client = pymongo.MongoClient(MONGO_HOST)
db = client['twitterdb']
db1 = client['twitterdb_hashtagprocess']

db1[COLLECTION_NAME].drop()
results=db[COLLECTION_NAME].find()
i=0
for result in results:
    score=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]#corresponding to emotionlist
    emotionlist =['anticipation','fear','anger','trust','surprise','sadness','joy','disgust']
    if 'retweeted_status' in result:
        if 'extended_tweet' in result['retweeted_status']:
            text=result['retweeted_status']['extended_tweet']['full_text']
        else:
            text=result['retweeted_status']['text']
    else:
        if 'extended_tweet' in result:
            text = result['extended_tweet']['full_text']
        else:
            text = result["text"]
    i=i+1
    print(text)
    print(i)
    print("-------------------------------")
    #collecting hashtags and add "#" notation
    hashtags=re.findall(r"#(\w+)", text)
    for j in range(0,len(hashtags)):
           hashtags[j] = "#" + hashtags[j]
           hashtags[j]=hashtags[j].lower()
    print (hashtags)
    print("=================================")
    
    
    for m in hashtags:   
       # print("++++++++++++++++++++++")
        hash_emotion=emolex_df[(emolex_df.hashtags == m)].emotion.values
        if len(hash_emotion)!=0:
            print(m)
            print(hash_emotion)
            for n in range(0,len(hash_emotion)):
                #get the emotion association for each hashtags
                hash_emotion_asso=emolex_df[(emolex_df.hashtags==m)&(emolex_df.emotion==hash_emotion[n])].association.values
      
                print(hash_emotion_asso)
                #accumulate the hashtag emotion association into final score list
                for o in range (0,8):
                    if emotionlist[o]==hash_emotion[n]:
                        score[o]+=hash_emotion_asso[0]
    print(score)
    print(emotionlist[score.index(max(score))])
    #if the emotion(max_score)!=class label,drop it
    if (emotionlist[score.index(max(score))] in WORDS):
        db1[COLLECTION_NAME].insert_one(result)
        print("insert****************************************")
    print(db[COLLECTION_NAME].count())
    print(db1[COLLECTION_NAME].count())
    
    
    
