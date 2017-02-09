from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from secret_keys import twitter_access_token
from secret_keys import twitter_access_token_secret
from secret_keys import twitter_consumer_key
from secret_keys import twitter_consumer_secret
import json
import time


QUERY = ['python', 'datamining', 'hashing']


class ImagesListener(StreamListener):
    """ Estimate stream frequency moments when a tweet is received. """
    def __init__(self, progress=False):
        super(ImagesListener, self).__init__()
        self.progress = progress

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            print(tweet)
            print('')
        except BaseException as e:
            print('Error on_data: %s' % str(e), '\n')
            time.sleep(1)
        return True

    def on_error(self, status):
        print(status)
        return True


if __name__ == '__main__':
    listener = ImagesListener(True)
    auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=QUERY)
