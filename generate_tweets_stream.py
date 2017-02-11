from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
from secret_keys import EMOTION_API_KEY
from secret_keys import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
from secret_keys import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
import emotions
import json
import time

QUERY = ['people', 'image', 'images', 'face']


class ImageListener(StreamListener):
    """ Perform sentiment analysis when a tweet is received. """

    # headers for Microsoft Emotion API request
    headers = dict()
    headers[emotions.API_SUBSCR_HEADER_KEY] = EMOTION_API_KEY
    headers[emotions.CONTENT_TYPE_HEADER_KEY] = emotions.CONTENT_TYPE_HEADER_VALUE

    def __init__(self, print_progress=True):
        super(ImageListener, self).__init__()
        self.print_progress = print_progress

    def on_data(self, data):
        try:
            tweet = json.loads(data)  # refer to https://dev.twitter.com/overview/api/tweets for tweet fields
            media_contents = tweet['entities']['media']  # list of images related to tweet

            for image in media_contents:
                image_url = image['media_url']

                image_sentiments = emotions.process_request(image_url, ImageListener.headers)

                # process info about each face in image
                for face_analysis in image_sentiments:
                    pass

            if self.print_progress and image_sentiments:
                print(image_url)
                print(image_sentiments)
                print('')

        except KeyError as e:
            # print('Missing %s key in json.' % str(e), '\n')
            pass
        # except BaseException as e:
        #     print('Error on_data: %s.' % str(e), '\n')
        #     time.sleep(1)
        return True

    def on_error(self, status):
        if self.print_progress:
            print(status)
        return True


if __name__ == '__main__':
    listener = ImageListener()
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    stream.filter(track=QUERY)
