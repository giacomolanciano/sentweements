from secret_keys import EMOTION_API_KEYS
import requests
import time

EMOTION_API_URL = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
API_SUBSCR_HEADER_KEY = 'Ocp-Apim-Subscription-Key'
CONTENT_TYPE_HEADER_KEY = 'Content-Type'
CONTENT_TYPE_HEADER_VALUE = 'application/json'
MAX_NUM_RETRIES = 60
SENTIMENTS_NUM = 8  # 'anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise'
SENTIMENTS = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']


class CognitiveAPIError(Exception):
    def __init__(self, message, http_status):
        super(CognitiveAPIError, self).__init__(message)

        self.http_status = http_status


def process_request(url_image, headers, data=None, params=None):
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

        # print('REQUEST: {}'.format(url_image))

        response = requests.request('post', EMOTION_API_URL, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:  # Too many requests (rate limiting)
            # print("Message: %s" % (response.json()['error']['message']))

            if retries <= MAX_NUM_RETRIES:
                time.sleep(1)
                retries += 1
                continue
            else:
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

    headers = dict()
    headers[API_SUBSCR_HEADER_KEY] = EMOTION_API_KEYS[0]
    headers[CONTENT_TYPE_HEADER_KEY] = CONTENT_TYPE_HEADER_VALUE

    image_sentiments = process_request(urlImage, headers)
    for face_analysis in image_sentiments:
        print(face_analysis)
