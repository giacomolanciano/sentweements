import geocoder
from tweepy import OAuthHandler
from tweepy.api import API
from secret_keys import EMOTION_API_KEY
from secret_keys import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
from secret_keys import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET


if __name__ == '__main__':
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    search_api = API(auth)

    users = None
    query = 'trump clinton filter:images'
    language = 'en'
    location = geocoder.osm('New York')

    # to be concatenated with space when passed to api call
    location_params = [str(location.lat), str(location.lng), '1mi']

    # make Search API call
    result = search_api.search(q=query, lang=language)  # insert query params
    print(result)
