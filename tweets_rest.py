import datetime
import json

import geocoder
from tweepy import OAuthHandler, Cursor
from tweepy.api import API

import emotions
import statistics
from secret_keys import EMOTION_API_KEY
from secret_keys import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
from secret_keys import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET

auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api_client = API(auth)

# headers for Microsoft Emotion API request
headers = dict()
headers[emotions.API_SUBSCR_HEADER_KEY] = EMOTION_API_KEY
headers[emotions.CONTENT_TYPE_HEADER_KEY] = emotions.CONTENT_TYPE_HEADER_VALUE


class ImageRetriever(object):
    """ Perform sentiment analysis of tweets matching a given query. """

    def __init__(self, query, since_date=None, until_date=None, language=None, location=None, print_progress=True):
        super(ImageRetriever, self).__init__()
        self.print_progress = print_progress
        self.query = query
        self.since_date = since_date
        self.until_date = until_date
        self.language = language

        self.location_params = None
        if location:
            geocoder_result = geocoder.osm(location)
            # to be concatenated with space when passed to api call
            self.location_params = [str(geocoder_result.lat), str(geocoder_result.lng), '1mi']

        self.sample_size = 0
        self.sentiments_mean = [0] * emotions.SENTIMENTS_NUM

    def search_api_request(self):

        geocode = None

        if self.since_date:
            # TODO extract date and add since operator to query
            since = datetime.strptime()
        if self.until_date:
            # TODO extract date and add until operator to query
            until = datetime.strptime()
        if self.location_params:
            geocode = ','.join(self.location_params)

        cursor = Cursor(api_client.search, q=query, lang=language, geocode=geocode)
        for page in cursor.pages():
            for tweet in page:
                print(tweet)
                # self._process_tweet(tweet)

    def _process_tweet(self, status):
        """ Update mean sentiments vector upon seeing new image in a tweet. """

        tweet = json.load(status._json)

        try:
            media_contents = tweet['entities']['media']  # list of images related to tweet
            image_sentiments = None
            image_url = ''

            for image in media_contents:
                image_url = image['media_url']

                image_sentiments = emotions.process_request(image_url, headers)

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


if __name__ == '__main__':

    users = None
    query = 'trump clinton filter:images'
    language = 'en'
    location = geocoder.osm('New York')

    # to be concatenated with space when passed to api call
    location_params = [str(location.lat), str(location.lng), '1mi']

    # # make Search API call
    # result = search_api.search(q=query, lang=language)
    # print(result)

    ir = ImageRetriever(query)
    ir.search_api_request()
