import json
import time

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

    def __init__(self, socket, room, query_params, print_progress=True):
        super(ImageRetriever, self).__init__()
        self.print_progress = print_progress

        self.socket = socket
        self.room = room

        query = query_params['query'].strip()
        self.query = query if query else None
        since = query_params['since_date'].strip()
        self.since = since if since else None
        until = query_params['until_date'].strip()
        self.until = until if until else None
        lang = query_params['language'].strip()
        self.lang = lang if lang else None

        self.geocode = None
        self.location = query_params['location'].strip()
        if self.location:
            geocoder_result = geocoder.osm(self.location)
            # to be concatenated with space when passed to api call
            self.location_params = [str(geocoder_result.lat), str(geocoder_result.lng), '50km']
            self.geocode = ','.join(self.location_params)

        self.sample_size = 0
        self.sentiments_mean = [0] * emotions.SENTIMENTS_NUM


    def search_api_request(self):
        # search allowed params:
        # 'q', 'lang', 'locale', 'since_id', 'geocode',
        # 'max_id', 'since', 'until', 'result_type', 'count',
        # 'include_entities', 'from', 'to', 'source']
        cursor = Cursor(api_client.search, q=self.query+" filter:images", lang=self.lang, geocode=self.geocode,
                        since=self.since, until=self.until)
        for tweet in cursor.items():
            update = self._process_tweet(tweet)
            if update and self.socket and self.room:
                self.socket.emit('update', json.dumps(update), room=self.room)
            time.sleep(0.5)

    def _process_tweet(self, status):
        """ Update mean sentiments vector upon seeing new image in a tweet. """

        tweet = status._json
        try:
            image_url = tweet['entities']['media'][0]['media_url']

            if self.print_progress:
                print(image_url)

            # make Emotion API call
            image_sentiments = emotions.process_request(image_url, headers)

            if image_sentiments:
                # process info about each face in image
                for face_analysis in image_sentiments:
                    # update sentiments mean
                    self.sample_size += 1
                    scores = list(face_analysis['scores'].values())
                    statistics.online_vectors_mean(self.sentiments_mean, scores, self.sample_size)

                    if self.print_progress:
                        print(image_sentiments)
                        print(self.sentiments_mean)

            result = dict()
            result['url'] = image_url
            result['mean'] = self.sentiments_mean
            return result

        except (KeyError, IndexError):
            return None


if __name__ == '__main__':

    init_params = {
        'query': 'puppy',
        'since_date': '',
        'until_date': '',
        'language': '',
        'location': ''
    }

    ir = ImageRetriever(None, None, init_params)
    ir.search_api_request()
