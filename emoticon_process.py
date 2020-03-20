#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import emoji
import pymongo
#print(emoji.demojize("He is 😳 !"))
#create emoji lexicon
joy=["U+1F600","U+1F602", "U+1F603", "U+1F604", "U+1F606", "U+1F607", "U+1F609", "U+1F60A"
    "U+1F60B", "U+1F60C", "U+1F60D", "U+1F60E", "U+1F60F", "U+1F31E", "U+263A", "U+1F618",
    "U+1F61C", "U+1F61D", "U+1F61B", "U+1F63A", "U+1F638", "U+1F639", "U+1F389","U+1F63B", "U+2764","U+1F63C"
    "U+2764", "U+1F496", "U+1F495", "U+1F601","U+1F497", "U+2665","U+1F970","U+1F923","U+1F60B","U+1F917","U+1F92A"]
anger=["U+1F62C", "U+1F620","U+1F92C", "U+1F610", "U+1F611", "U+1F620", "U+1F621", "U+1F616", "U+1F624",
       "U+1F63E","U+1F644","U+1F629"]
fear=["U+1F605", "U+1F626","U+1F928","U+1F92C", "U+1F611","U+1F627", "U+1F631", "U+1F628", "U+1F630", "U+1F640","U+1F4A9","U+1F97A","U+1F494"]
surprise=["U+1F633","U+1F44D" ,"U+1F62F", "U+1F635", "U+1F632","U+1F614", "U+1F615", "U+2639", "U+1F62B", "U+1F629","U+1F622", "U+1F625", "U+1F62A","U+1F613", "U+1F62D", "U+1F63F","U+2639", "U+1F494"]
'''
WORDS ="joy"
COLLECTION_NAME='twitterdb_happy'

WORDS ="fear"
COLLECTION_NAME='twitterdb_fear'
'''
WORDS ="anger"
COLLECTION_NAME='twitterdb_angry'       
'''
WORDS ="surprise"                        
COLLECTION_NAME='twitterdb_surprise'

WORDS ="joy"
COLLECTION_NAME='twitterdb_excitement'   

WORDS ="joy"
COLLECTION_NAME='twitterdb_pleasant'  
'''
MONGO_HOST = 'mongodb://localhost:27017/'  # mongodb host path
client = pymongo.MongoClient(MONGO_HOST)
db = client['twitterdb_hashtagprocess']
db1 = client['twitterdb_emoticonprocess']

db1[COLLECTION_NAME].drop()
results=db[COLLECTION_NAME].find()

i=0
for result in results:
    emotionlist=["joy","fear","surprise","anger"]
    score=[0,0,0,0]
    i=i+1
    print("----------------------------------------")
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
    #get the emoji from text
    allchars = [str for str in text]
    emojilist = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    print(text)
    print(emojilist)
    print(i)
    #identify the emotion of emoji and accumulate relational score
    for e in emojilist:
        print('U+{:X}'.format(ord(e)))
        
        if 'U+{:X}'.format(ord(e)) in joy:
            score[0]=score[0]+1      
        if 'U+{:X}'.format(ord(e)) in fear:
            score[1]=score[1]+1
        if 'U+{:X}'.format(ord(e)) in surprise:
            score[2]=score[2]+1
        if 'U+{:X}'.format(ord(e)) in anger:
            score[3]=score[3]+1

    print(score)
    #if the emotion(max_score)!=class label,drop it
    if max(score)!=0:
        print(emotionlist[score.index(max(score))])      
    if(emotionlist[score.index(max(score))]==WORDS or max(score)==0):
        db1[COLLECTION_NAME].insert_one(result)
        print("insert****************************************")
            
print(db[COLLECTION_NAME].count())
print(db1[COLLECTION_NAME].count())








         
            
            
            
                   
