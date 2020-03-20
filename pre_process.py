#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymongo
import enchant
import re
import contractions
'''
WORDS ="joy"
COLLECTION_NAME='twitterdb_happy' #344

WORDS ="fear"
COLLECTION_NAME='twitterdb_fear'  #245

WORDS ="anger"
COLLECTION_NAME='twitterdb_angry'       #

WORDS ="surprise"                        
COLLECTION_NAME='twitterdb_surprise' #133

WORDS ="anticipation"
COLLECTION_NAME='twitterdb_excitement'   #
'''
WORDS ="trust"
COLLECTION_NAME='twitterdb_pleasant'  #


MONGO_HOST = 'mongodb://localhost:27017/'  # mongodb host path
client = pymongo.MongoClient(MONGO_HOST)
db = client['twitterdb_emoticonprocess']
db1 = client['twitterdb_preprocess']
db1[COLLECTION_NAME].drop()
results=db[COLLECTION_NAME].find()
d = enchant.Dict("en_US")

for result in results:
        print("===============================")
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
        #info that will be stored into final csv
        _id=result['id']
        created_at=result['created_at']
        rawtext=text
      
        #remove url
        url_reg  = r'[a-z]*[:]+\S+'
        result   = re.sub(url_reg, '', text)
        #remove @
        ate_remove=re.sub(r"@(\w+)",'',result)
        #remove emoji
        RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
        emoji_remove = RE_EMOJI.sub(r'', ate_remove)
        
        #split text into words
        wordlist=emoji_remove.split()
        for i in range(0,len(wordlist)):
            word=wordlist[i]
            #remove loooove-duplicate letters into correct words
            r=re.sub(r'(.)\1{2,}', r'\1',word)
            if (d.check(r)==True):
                word =r
            else:
                word=re.sub(r'(.)\1{2,}',  r'\1'r'\1',word)
            #remove abbreviation into normal expression
            word=contractions.fix(word)
            wordlist[i]=word
            
        #reshape into text
        text=' '.join(wordlist)
        #remove hashtags which is accumulated in the end
        text = re.sub("( #[^# ]+?)+$"," ", text);
        #remove "#" notation for hasgtahs inside the text
        text = re.sub(r"#",'',text)
        print(rawtext)
        print("-------------------------------------------")
        print(text)
        #save into final mongodb
        db1[COLLECTION_NAME].insert_one({ "Tweet_id":_id,"created_at" :created_at,"rawtext":rawtext, "text" : text})
        
print(db1[COLLECTION_NAME].count())

