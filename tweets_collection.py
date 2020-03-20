#  -*- coding: utf-8 -*-
import tweepy
import json
from tweepy import OAuthHandler
from pymongo import MongoClient


MONGO_HOST = 'mongodb://localhost:27017/'  # mongodb host path/
COLLECTION_NAME="twitterdb_excitement"
#pleasant
#WORDS = ["#sad","#frustration","#amazing","#amazed","#dreary","#upset","#sorrowful"]  #surprise
#WORDS = ["#happy","#joy","#love"] #happy 
WORDS = ["#expectation","#excitement","#expecting","#excited","#tooexcited","#soexcited"
         ,"#anticipation","#interesting","#interested","#anticipated"]  #Excitement
#WORDS = ["#disgust","#depression","#rushing","#shy",
   #     "#apprehensive","#socialanxiety","#feared","#biggestfear","#fear"]   #fear		   
#WORDS = ["#angry","#mad","#roar","#furious","#annoying","#anger",
     #   "#disapointment","#imangry","#veryangry","#fuckedoff","#dontmess"]  #angry

#WORDS = ["#admiring","#admiration","#trusted","#trusty","#admired","#maturity","#trust","#pleasant","#pleased"]  #pleasant

consumer_key = 'o8FVivGo7I9W82U7mOtpvbf3Q'
consumer_secret = 'mMHEl2C9sJBLD0Nnwg1gNn5TO3g8q9d9PPcpjmsEIsg3t8GOdf'
access_token = '1232366055323992064-lEpFvfQ4Y5oeBoJziujl7JR790DwjP'
access_secret = '2uIXM4HXIf5aivJIS5BDxXRxsWArH6X3diX9sBI6t9MUW'
i=0
class StreamListener(tweepy.StreamListener):

      
    # This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # if connect the streamer will print something
        print("You are now connected to the streaming API.")
        '''
        client = MongoClient(MONGO_HOST)  # connect mongodb
        db = client.twitterdb
        db[COLLECTION_NAME].drop()
        '''

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        global i
        # When receiving data from twitter will call this method
        try:
            
            client = MongoClient(MONGO_HOST)  # connect mongodb
            db = client['twitterdb']
            data_json = json.loads(data)  # Decode the JSON from Twitter
            i+=1
            if 'retweeted_status' in data_json:
                if 'extended_tweet' in data_json['retweeted_status']:
                    text=data_json['retweeted_status']['extended_tweet']['full_text']
                else:
                    text=data_json['retweeted_status']['text']
            else:
                if 'extended_tweet' in data_json:
                    text = data_json['extended_tweet']['full_text']
                else:
                    text = data_json["text"]
                    
            print(str(text))
        
            print("--------------------------------------")
            print(i)
            db[COLLECTION_NAME].insert_one(data_json)
            if i>=500: 
                return False


        except Exception as e:
            print(e)
            
            
    

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)
listener = StreamListener()
streamer = tweepy.Stream(auth=auth, listener=listener)

print("Searching keywords are: " + str(WORDS))  # filter keywords
streamer.filter(track=WORDS,languages=["en"])
