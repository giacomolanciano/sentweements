from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from secret_keys import emotion_api_key
from secret_keys import twitter_access_token
from secret_keys import twitter_access_token_secret
from secret_keys import twitter_consumer_key
from secret_keys import twitter_consumer_secret
import emotions
import json
import time

QUERY = ['people', 'image', 'images', 'face']


class ImagesListener(StreamListener):
    """ Perform sentiment analysis when a tweet is received. """

    # headers for Microsoft Emotion API request
    headers = dict()
    headers[emotions.API_SUBSCR_HEADER_KEY] = emotion_api_key
    headers[emotions.CONTENT_TYPE_HEADER_KEY] = emotions.CONTENT_TYPE_HEADER_VALUE

    def __init__(self):
        super(ImagesListener, self).__init__()

    def on_data(self, data):
        try:
            tweet = json.loads(data)  # refers to https://dev.twitter.com/overview/api/tweets for tweet JSON fields
            media_contents = tweet['entities']['media']  # list of images related to tweet

            for image in media_contents:
                image_url = image['media_url']
                print(image_url)

                image_sentiments = emotions.process_request(image_url, ImagesListener.headers)

                # process info about each face in image
                for res in image_sentiments:
                    print(res)

            print('')

        except KeyError as e:
            print('Missing %s key in json' % str(e), '\n')
        except BaseException as e:
            print('Error on_data: %s' % str(e), '\n')
            time.sleep(1)
        return True

    def on_error(self, status):
        print(status)
        return True


if __name__ == '__main__':
    listener = ImagesListener()
    auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=QUERY)
