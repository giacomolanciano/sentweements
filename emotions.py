import requests
import time
from secret_keys import EMOTION_API_KEYS

EMOTION_API_URL = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
API_SUBSCR_HEADER_KEY = 'Ocp-Apim-Subscription-Key'
CONTENT_TYPE_HEADER_KEY = 'Content-Type'
CONTENT_TYPE_HEADER_VALUE = 'application/json'
MAX_NUM_RETRIES = 60
EMOTIONS = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']


class CognitiveAPIError(Exception):
    def __init__(self, message, http_status):
        super(CognitiveAPIError, self).__init__(message)

        self.http_status = http_status


class EmotionAnalysis(object):

    max_key = len(EMOTION_API_KEYS) - 1

    def __init__(self):
        self.key = 0

    def process_request(self, url_image, data=None, params=None):
        """
        Helper function to process the request to Microsoft's APIs.

        Parameters:
        url_image: URL of image to be processed.
        headers: Used to pass the key information and the data type request.
        data: Used when processing image read from disk.
        params: Query string parameters (not used).
        """

        retries = 0
        result = None
        json = {'url': url_image}

        while True:

            # headers for Microsoft Emotion API request
            headers = dict()
            headers[API_SUBSCR_HEADER_KEY] = EMOTION_API_KEYS[self.key]
            headers[CONTENT_TYPE_HEADER_KEY] = CONTENT_TYPE_HEADER_VALUE

            # print('REQUEST: {}'.format(url_image))

            response = requests.request('post', EMOTION_API_URL, json=json, data=data, headers=headers, params=params)

            if response.status_code == 429:  # Too many requests (rate limiting)
                # print("Message: %s" % (response.json()['error']['message']))

                if retries <= MAX_NUM_RETRIES:
                    time.sleep(1)
                    retries += 1
                    continue
                elif self.key <= EmotionAnalysis.max_key:  # api key carousel
                    self.key += 1
                    retries = 0
                    continue
                else:
                    self.key = 0
                    raise CognitiveAPIError("Too many requests.", 429)

            elif response.status_code == 200 or response.status_code == 201:
                if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                    pass
                elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                    if CONTENT_TYPE_HEADER_VALUE in response.headers['content-type'].lower():
                        result = response.json() if response.content else None
                        # elif 'image' in response.headers['content-type'].lower():
                        #     result = response.content
            else:
                raise CognitiveAPIError(response.json()['error']['message'], response.status_code)

            break

        return result


if __name__ == '__main__':
    # URL direction to image
    urlImage = 'https://raw.githubusercontent.com/Microsoft/ProjectOxford-ClientSDK/master/Face/Windows/Data/detection3.jpg'

    ea = EmotionAnalysis()
    image_sentiments = ea.process_request(urlImage)
    for face_analysis in image_sentiments:
        print(face_analysis)
