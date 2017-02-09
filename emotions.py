import requests
import time
from secret_keys import emotion_api_key

# Variables
_url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
_maxNumRetries = 10


def process_request(json, headers, data=None, params=None):
    """
    Helper function to process the request to Microsoft's APIs.

    Parameters:
    json: Used when processing images from its URL.
    headers: Used to pass the key information and the data type request.
    data: Used when processing image read from disk.
    params: Query string parameters (not used).
    """

    retries = 0
    result = None

    while True:

        response = requests.request('post', _url, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:
            print("Message: %s" % (response.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print("Error code: %d" % response.status_code)
            print("Message: %s" % (response.json()['error']['message']))

        break

    return result

if __name__ == '__main__':
    # URL direction to image
    urlImage = 'https://raw.githubusercontent.com/Microsoft/ProjectOxford-ClientSDK/master/Face/Windows/Data/detection3.jpg'

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = emotion_api_key
    headers['Content-Type'] = 'application/json'

    json = {'url': urlImage}

    result = process_request(json, headers)

    print(result)
