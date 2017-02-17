import json
import os

import geocoder
import time
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

import emotions
import statistics
from secret_keys import *

DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
THREADS_PER_TWITTER_KEY = 2


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


class RegionListener(StreamListener):
    """ Store a stream of tweets coming from given city. """

    def __init__(self, region_name, print_progress=True):
        super(RegionListener, self).__init__()
        self.print_progress = print_progress

        # filter out spaces and commas from region name
        self.region_name = str.lower(str.replace(str.replace(region_name, ' ', '_'), ',', ''))

        # create region-related file
        self.dest_file_name = os.path.join(DEST, self.region_name + '.txt')

    def on_data(self, data):
        with open(self.dest_file_name, 'a') as dest:
            dest.write(data.strip() + ',\n')

        if self.print_progress:
            print(data)

        return True

    def on_error(self, status):
        if self.print_progress:
            print(status)
        return True


def get_region_stream(region, twitter_consumer_key, twitter_consumer_secret, twitter_access_token,
                      twitter_access_token_secret):
    listener = RegionListener(region)
    auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    stream = Stream(auth, listener)

    location = geocoder.osm(region)
    location_bbox = location.geojson['bbox']
    print('bbox: ' + str(location_bbox))

    # Twitter Streaming APIs let us filter tweets according to users, text, location, and languages.
    # The track, follow, and locations fields should be considered to be combined with an OR operator.
    stream.filter(locations=location_bbox)

    # to read json from file
    # with open(os.path.join(DEST, 'rome_italy.txt'), 'r') as json_data:
    #     d = json.load(json_data)
    #     print(d)


if __name__ == '__main__':

    import threading

    ITALIAN_REGIONS = ["Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia Romagna", "Friuli Venezia Giulia",
                       "Lazio", "Liguria", "Lombardia", "Marche", "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia",
                       "Toscana", "Trentino Alto Adige", "Umbria", "Valle d'Aosta", "Veneto"]

    # create destination directory if not exists
    if not os.path.exists(DEST):
        os.makedirs(DEST)

    credentials = zip(TWITTER_CONSUMER_KEYS, TWITTER_CONSUMER_SECRETS, TWITTER_ACCESS_TOKENS,
                      TWITTER_ACCESS_TOKEN_SECRETS)

    i = 0
    for ck, cs, at, ats in zip(TWITTER_CONSUMER_KEYS, TWITTER_CONSUMER_SECRETS, TWITTER_ACCESS_TOKENS,
                               TWITTER_ACCESS_TOKEN_SECRETS):

        for r in range(i, i + THREADS_PER_TWITTER_KEY):
            region = ITALIAN_REGIONS[r] + ", Italy"
            t = threading.Thread(target=get_region_stream, args=(region, ck, cs, at, ats))
            t.start()
            time.sleep(1)  # delay threads using the same key to prevent api error

        i += THREADS_PER_TWITTER_KEY
