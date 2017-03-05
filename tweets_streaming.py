import json

import geocoder
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

import emotions
import statistics
from secret_keys import EMOTION_API_KEYS
from secret_keys import TWITTER_ACCESS_TOKENS, TWITTER_ACCESS_TOKEN_SECRETS
from secret_keys import TWITTER_CONSUMER_KEYS, TWITTER_CONSUMER_SECRETS


class ImageListener(StreamListener):
    """ Perform sentiment analysis when a tweet is received. """

    # headers for Microsoft Emotion API request
    headers = dict()
    headers[emotions.API_SUBSCR_HEADER_KEY] = EMOTION_API_KEYS[0]
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
                    statistics.online_sentiments_vectors_mean(self.sentiments_mean, scores, self.sample_size)

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
    auth = OAuthHandler(TWITTER_CONSUMER_KEYS[0], TWITTER_CONSUMER_SECRETS[0])
    auth.set_access_token(TWITTER_ACCESS_TOKENS[0], TWITTER_ACCESS_TOKEN_SECRETS[0])
    stream = Stream(auth, listener)

    # Twitter Streaming APIs let us filter tweets according to users, text, location, and languages.
    # The track, follow, and locations fields should be considered to be combined with an OR operator.

    users = None
    keywords = None
    location = geocoder.osm('Italy')
    location_bbox = location.geojson['bbox']
    languages = None

    while True:
        try:
            stream.filter(follow=users, track=keywords, locations=location_bbox, languages=languages)
        except KeyboardInterrupt:
            break
        except Exception as e:
            # print('ERROR: %s.' % str(e), '\n')
            pass
