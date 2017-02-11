from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from secret_keys import EMOTION_API_KEY
from secret_keys import TWITTER_ACCESS_TOKEN
from secret_keys import TWITTER_ACCESS_TOKEN_SECRET
from secret_keys import TWITTER_CONSUMER_KEY
from secret_keys import TWITTER_CONSUMER_SECRET
import emotions
import json
import time

QUERY = ['people', 'image', 'images', 'face']


class ImagesListener(StreamListener):
    """ Perform sentiment analysis when a tweet is received. """

    # headers for Microsoft Emotion API request
    headers = dict()
    headers[emotions.API_SUBSCR_HEADER_KEY] = EMOTION_API_KEY
    headers[emotions.CONTENT_TYPE_HEADER_KEY] = emotions.CONTENT_TYPE_HEADER_VALUE

    def __init__(self, progress=True):
        super(ImagesListener, self).__init__()
        self.progress = progress

    def on_data(self, data):
        try:
            tweet = json.loads(data)  # refer to https://dev.twitter.com/overview/api/tweets for tweet JSON fields
            media_contents = tweet['entities']['media']  # list of images related to tweet

            for image in media_contents:
                image_url = image['media_url']
                if self.progress:
                    print(image_url)

                image_sentiments = emotions.process_request(image_url, ImagesListener.headers)

                # process info about each face in image
                for res in image_sentiments:
                    if self.progress:
                        print(res)

            if self.progress:
                print('')

        except KeyError as e:
            print('Missing %s key in json.' % str(e), '\n')
        except BaseException as e:
            print('Error on_data: %s.' % str(e), '\n')
            time.sleep(1)
        return True

    def on_error(self, status):
        if self.progress:
            print(status)
        return True


if __name__ == '__main__':
    listener = ImagesListener()
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    stream.filter(track=QUERY)
