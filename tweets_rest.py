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

    def __init__(self, socket, room, query_params, print_progress=False):
        super(ImageRetriever, self).__init__()
        self.print_progress = print_progress
        self.socket = socket
        self.room = room
        self.query = query_params['query']
        self.since_date = query_params['since_date']
        self.until_date = query_params['until_date']
        self.language = query_params['language']

        self.location_params = None
        location = query_params['location']
        if location:
            geocoder_result = geocoder.osm(location)
            # to be concatenated with space when passed to api call
            self.location_params = [str(geocoder_result.lat), str(geocoder_result.lng), '1mi']

        self.sample_size = 0
        self.sentiments_mean = [0] * emotions.SENTIMENTS_NUM

    def search_api_request(self):

        geocode = None

        if self.since_date:
            self.query = self.query + ' since:' + self.since_date
        if self.until_date:
            self.query = self.query + ' until:' + self.until_date
        if self.location_params:
            geocode = ','.join(self.location_params)

        cursor = Cursor(api_client.search, q=self.query, lang=self.language, geocode=geocode)
        for page in cursor.pages(1):
            for tweet in page:
                update = self._process_tweet(tweet)
                if update and self.socket and self.room:
                    self.socket.emit('update', json.dumps(update), room=self.room)

    def _process_tweet(self, status):
        """ Update mean sentiments vector upon seeing new image in a tweet. """

        tweet = status._json

        try:
            media_contents = tweet['entities']['media']  # list of images related to tweet
            urls = []

            for image in media_contents:
                image_url = image['media_url']

                # make Emotion API call
                image_sentiments = emotions.process_request(image_url, headers)

                if image_sentiments:
                    if self.print_progress:
                        print(image_url)
                        print(image_sentiments)
                        print('')

                    # the image contains faces, append to result
                    urls.append(image_url)

                    # process info about each face in image
                    for face_analysis in image_sentiments:
                        # update sentiments mean
                        self.sample_size += 1
                        scores = list(face_analysis['scores'].values())
                        statistics.online_vectors_mean(self.sentiments_mean, scores, self.sample_size)

                        if self.print_progress:
                            print(self.sentiments_mean)

            if urls:
                result = dict()
                result['urls'] = urls
                result['mean'] = self.sentiments_mean
                return result

            return None

        except KeyError as e:
            # print('Missing %s key in json.' % str(e), '\n')
            pass

        return None


if __name__ == '__main__':

    init_params = {
        'query': 'people images',
        'since_date': '',
        'until_date': '',
        'language': '',
        'location': ''
    }

    ir = ImageRetriever(None, None, init_params)
    ir.search_api_request()
