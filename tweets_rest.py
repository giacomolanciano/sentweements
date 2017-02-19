import json
import time

import geocoder
from tweepy import OAuthHandler, Cursor
from tweepy.api import API

import emotions
from emotions import EmotionAnalysis
import statistics
from secret_keys import EMOTION_API_KEYS
from secret_keys import TWITTER_ACCESS_TOKENS, TWITTER_ACCESS_TOKEN_SECRETS
from secret_keys import TWITTER_CONSUMER_KEYS, TWITTER_CONSUMER_SECRETS

auth = OAuthHandler(TWITTER_CONSUMER_KEYS[0], TWITTER_CONSUMER_SECRETS[0])
auth.set_access_token(TWITTER_ACCESS_TOKENS[0], TWITTER_ACCESS_TOKEN_SECRETS[0])
api_client = API(auth)


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

        zeros = [0] * len(emotions.EMOTIONS)
        self.sentiments_mean = dict(zip(emotions.EMOTIONS, zeros))
        self.ea = EmotionAnalysis()

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
            time.sleep(1.5)

    def _process_tweet(self, status):
        """ Update mean sentiments vector upon seeing new image in a tweet. """

        tweet = status._json
        try:
            image_url = tweet['entities']['media'][0]['media_url']

            if self.print_progress:
                print(image_url)

            # make Emotion API call
            image_sentiments = self.ea.process_request(image_url)

            if image_sentiments:
                # process info about each face in image
                for face_analysis in image_sentiments:
                    # update sentiments mean
                    self.sample_size += 1
                    scores = face_analysis['scores']
                    statistics.online_sentiments_vectors_mean(self.sentiments_mean, scores, self.sample_size)

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
        'query': 'puppy filter:images',
        'since_date': '',
        'until_date': '',
        'language': '',
        'location': ''
    }

    ir = ImageRetriever(None, None, init_params)
    ir.search_api_request()
