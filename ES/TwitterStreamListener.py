import tweepy
import json
import Tweet2ES, Config

#override tweepy.StreamListener to add logic to on_status
class TwitterStreamListener(tweepy.StreamListener):
    def on_error(self, status_code):
        print status_code
    def on_status(self, status):
        print(status.text)

    def on_data(self, raw_data):
        decoded = json.loads(raw_data)
        try:
            if ('coordinates' in decoded and decoded['coordinates'] == None):
                return True
        except:
            print 'cannot find coordinates key'
        if not ('user' in decoded) :
            return True
        try:
            Tweet2ES.addTweets(raw_data)
        except:
            print 'Tweet2ES error'
        #print decoded['coordinates']
        #print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        # print ''
        return True



#listener = TwitterStreamListener()
#auth = tweepy.OAuthHandler(Config.twitter_consumer_key, Config.consumer_secret)
#auth.set_access_token(Config.access_token, Config.access_token_secret)
#stream = tweepy.Stream(auth, listener)
#stream.filter(locations=[-180.0,-90.0,180.0,90.0], async=True)
#myStream.filter(locations=[-127.33,23.34,-55.52,49.56])
