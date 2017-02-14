""" Module for basic statistic operations. """

from emotions import SENTIMENTS

DIGITS = 5


def mean(values):
    return sum(values) / max(len(values), 1)


def online_vectors_mean(curr_mean_vector, new_vector, sample_size):
    """
    Perform step of online mean algorithm, for each component of a vector
    (refer https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance).
    Note: side-effect on curr_mean_vector.
    """

    for sentiment in SENTIMENTS:
        delta = new_vector[sentiment] - curr_mean_vector[sentiment]
        curr_mean_vector[sentiment] += delta / sample_size
        curr_mean_vector[sentiment] = round(curr_mean_vector[sentiment], DIGITS)


def vectors_mean(vectors):
    """
    Compute mean of a group of vectors (of same length).
    """
    return list(map(mean, zip(*vectors)))


if __name__ == '__main__':
    a = {'neutral': 0, 'contempt': 0, 'anger': 0, 'surprise': 0, 'disgust': 0, 'sadness': 0, 'happiness': 0, 'fear': 0}
    b = {'neutral': 1, 'contempt': 2, 'anger': 3, 'surprise': 4, 'disgust': 5, 'sadness': 6, 'happiness': 7, 'fear': 8}
    c = {'neutral': 1, 'contempt': 6, 'anger': 3, 'surprise': 1, 'disgust': 9, 'sadness': 6, 'happiness': 7, 'fear': 8}

    online_vectors_mean(a, b, 1)
    print(a)

    online_vectors_mean(a, c, 2)
    print(a)
