import indicoio
from secret_keys import *


class SentimentAnalysis(object):

    max_key = len(INDICO_API_KEYS) - 1

    def __init__(self):
        self.key = 0

    def get_sentiment_score(self, text):
        score = None
        working_key = False

        while not working_key:
            indicoio.config.api_key = INDICO_API_KEYS[self.key]
            score = indicoio.sentiment(text)
            if not isinstance(score, float):
                if self.key <= SentimentAnalysis.max_key:
                    self.key += 1
                else:
                    self.key = 0
                    return None
            else:
                working_key = True
        return score


if __name__ == '__main__':
    # example
    sa = SentimentAnalysis()
    res = sa.get_sentiment_score("I love writing code!")
    print(res)
