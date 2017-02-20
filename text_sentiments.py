import indicoio

from secret_keys import *

LIMIT_EXCEEDED_TAG = 'exceeded'


class SentimentAnalysis(object):

    max_key = len(INDICO_API_KEYS) - 1

    def __init__(self, debug=True):
        self.key = 0
        self.debug = debug

    def get_sentiment_score(self, text):
        while True:
            try:
                indicoio.config.api_key = INDICO_API_KEYS[self.key]
                score = indicoio.sentiment_hq(text, language='detect')  # raises exception if language not supported
                break

            except indicoio.IndicoError as e:
                if self.debug:
                    print("IndicoError occurred: {}".format(e))
                if LIMIT_EXCEEDED_TAG in str(e):
                    if self.key <= SentimentAnalysis.max_key:
                        self.key += 1
                else:
                    return None
            except IndexError:
                self.key = 0
                raise indicoio.IndicoError("Monthly limit exceeded for ALL keys.")

        return score


if __name__ == '__main__':
    # example
    sa = SentimentAnalysis()
    # res = sa.get_sentiment_score("I love writing code!")
    res = sa.get_sentiment_score("https://t.co/OvtrsMtLe1")
    print(res)
