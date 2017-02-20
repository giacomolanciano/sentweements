import json
import os

import geocoder
import time

import sqlite3
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from datetime import datetime

import emotions
import statistics
from emotions import EmotionAnalysis, CognitiveAPIError
from secret_keys import *
from constants import DATA_FOLDER
from constants import DATABASE
from text_sentiments import SentimentAnalysis

TWITTER_DATETIME_FORMAT = '%a %b %d %H:%M:%S %z %Y'
SQLITE_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.000'
THREADS_PER_TWITTER_KEY = 2
ITALIAN_REGIONS = ["Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia Romagna", "Friuli Venezia Giulia",
                   "Lazio", "Liguria", "Lombardia", "Marche", "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia",
                   "Toscana", "Trentino Alto Adige", "Umbria", "Valle d'Aosta", "Veneto"]
ITALIAN_NATION = ', Italy'


class ImageListener(StreamListener):
    """ Perform sentiment analysis when a tweet is received. """

    def __init__(self, print_progress=False, debug=True):
        super(ImageListener, self).__init__()
        self.print_progress = print_progress
        self.debug = debug
        self.sample_size = 0
        self.sentiments_mean = [0] * len(emotions.EMOTIONS)
        self.ea = EmotionAnalysis()

    def on_data(self, data):
        try:
            tweet = json.loads(data)  # refer to https://dev.twitter.com/overview/api/tweets for tweet fields
            media_contents = tweet['entities']['media']  # list of images related to tweet
            image_sentiments = None
            image_url = ''

            for image in media_contents:
                image_url = image['media_url']

                image_sentiments = self.ea.process_request(image_url)

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

        except KeyError:
            # print('Missing %s key in json.' % str(e), '\n')
            pass

        return True

    def on_error(self, status):
        if self.debug:
            print(status)
        return True


class RegionListener(StreamListener):
    """ Store a stream of tweets coming from given city. """

    zeros = [0] * len(emotions.EMOTIONS)

    def __init__(self, region_name, print_progress=False, debug=True):
        super(RegionListener, self).__init__()
        self.print_progress = print_progress
        self.debug = debug

        # filter out spaces and commas from region name
        self.region_name = region_name

        # create sentiment analysis instance
        self.sa = SentimentAnalysis()
        self.ea = EmotionAnalysis()

    def on_data(self, data):

        # to reuse method both with Twitter API and standalone
        if isinstance(data, str):
            tweet = json.loads(data)
        else:
            tweet = json.load(data)

        id_str = tweet['id_str']
        text = tweet['text']
        lang = tweet['lang']

        date_time = tweet['created_at']
        dto = datetime.strptime(date_time, TWITTER_DATETIME_FORMAT)
        date_time = dto.strftime(SQLITE_DATETIME_FORMAT)

        try:
            image_url = tweet['entities']['media'][0]['media_url']
            image_scores = dict(zip(emotions.EMOTIONS, RegionListener.zeros))

            image_sentiments = self.ea.process_request(image_url)

            if image_sentiments:
                sample_size = 0

                # process info about each face in image, compute mean vector
                for face_analysis in image_sentiments:
                    # update sentiments mean
                    sample_size += 1
                    scores = face_analysis['scores']
                    statistics.online_sentiments_vectors_mean(image_scores, scores, sample_size)

                    if self.print_progress:
                        print(image_sentiments)
                        print(image_scores)
            else:
                for key in image_scores.keys():
                    image_scores[key] = None

        except (KeyError, IndexError, CognitiveAPIError):
            image_url = None
            image_scores = None

        # compute sentiment score
        text_score = self.sa.get_sentiment_score(text)
        if not text_score:
            text_score = None

        conn = sqlite3.connect(DATABASE)
        try:
            # create database connection
            cursor = conn.cursor()

            # Insert a row of data in db
            cursor.execute("INSERT INTO tweets VALUES (?,?,?,?,?,?)",
                           (id_str, self.region_name, date_time, text, lang, text_score))

            if image_url:
                cursor.execute("INSERT INTO images VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                               (self.region_name, image_url, date_time, image_scores['anger'],
                                image_scores['contempt'], image_scores['disgust'], image_scores['fear'],
                                image_scores['happiness'], image_scores['neutral'], image_scores['sadness'],
                                image_scores['surprise']))

            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            conn.close()
            return True

        if self.print_progress:
            print(json.dumps(tweet, indent=4))

        return True

    def on_error(self, status):
        if self.debug:
            print(status)
        return True


def get_region_stream(region, nation, twitter_consumer_key, twitter_consumer_secret, twitter_access_token,
                      twitter_access_token_secret):
    listener = RegionListener(region)
    auth = OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    stream = Stream(auth, listener)

    location = geocoder.google(region + nation)
    location_bbox = location.geojson['bbox']
    # print('{} bbox: {}'.format(region, str(location_bbox)));

    print('### {} thread is running ###'.format(region, str(location_bbox)));

    # Twitter Streaming APIs let us filter tweets according to users, text, location, and languages.
    # The track, follow, and locations fields should be considered to be combined with an OR operator.
    stream.filter(locations=location_bbox)


def start_regions_streaming():
    import threading

    # create destination directory if not exists
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    i, regions, end = 0, len(ITALIAN_REGIONS), False
    for ck, cs, at, ats in zip(TWITTER_CONSUMER_KEYS, TWITTER_CONSUMER_SECRETS, TWITTER_ACCESS_TOKENS,
                               TWITTER_ACCESS_TOKEN_SECRETS):

        for r in range(i, i + THREADS_PER_TWITTER_KEY):
            if r >= regions:
                end = True
                break
            t = threading.Thread(target=get_region_stream, args=(ITALIAN_REGIONS[r], ITALIAN_NATION, ck, cs, at, ats))
            t.start()
            time.sleep(1)  # delay threads using the same key to prevent api error

        if end:
            break

        i += THREADS_PER_TWITTER_KEY


if __name__ == '__main__':
    start_regions_streaming()

    # to use RegionListener standalone
    # r = RegionListener('abruzzo, italy')
    # with open('data/abruzzo_italy.txt', 'r') as input:
    #     line = input.readline()
    #     for i in range(5):
    #         r.on_data(line[:len(line)-2])
    #         line = input.readline()

    # to read json from file
    # with open(os.path.join(DEST, 'rome_italy.txt'), 'r') as json_data:
    #     d = json.load(json_data)
    #     print(d)
