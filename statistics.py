""" Module for basic statistic operations. """


def mean(values):
    return sum(values) / max(len(values), 1)


def online_vectors_mean(curr_mean_vector, new_vector, sample_size):
    """
    Perform step of online mean algorithm, for each component of a vector
    (refer https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance).
    Note: side-effect on curr_mean_vector.
    """
    for component, (curr_mean, new_elem) in enumerate(zip(curr_mean_vector, new_vector)):
        delta = new_elem - curr_mean
        curr_mean_vector[component] += (delta / sample_size)


def vectors_mean(vectors):
    """
    Compute mean of a group of vectors (of same length).
    """
    return list(map(mean, zip(*vectors)))


if __name__ == '__main__':
    a = [[240, 240, 239],
         [250, 249, 237],
         [242, 239, 237],
         [240, 234, 233]]
    r = vectors_mean(a)
    print(r)
