from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
from secret_keys import EMOTION_API_KEY
from secret_keys import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
from secret_keys import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from requests.exceptions import HTTPError
import emotions
import statistics
import json

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
        self.sample_size = 0
        self.sentiments_mean = [0] * emotions.SENTIMENTS_NUM

    def on_data(self, data):
        try:
            tweet = json.loads(data)  # refer to https://dev.twitter.com/overview/api/tweets for tweet fields
            media_contents = tweet['entities']['media']  # list of images related to tweet
            image_sentiments = None
            image_url = ''

            for image in media_contents:
                image_url = image['media_url']

                image_sentiments = emotions.process_request(image_url, ImageListener.headers)

                # process info about each face in image
                for face_analysis in image_sentiments:
                    # update sentiments mean
                    self.sample_size += 1
                    scores = list(face_analysis['scores'].values())
                    statistics.online_vectors_mean(self.sentiments_mean, scores, self.sample_size)

                    if self.print_progress:
                        print(self.sentiments_mean)

            if self.print_progress and image_sentiments:
                print(image_url)
                print(image_sentiments)
                print('')

        except KeyError as e:
            # print('Missing %s key in json.' % str(e), '\n')
            pass

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

    while True:
        try:
            stream.filter(track=QUERY)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print('ERROR: %s.' % str(e), '\n')
            pass
