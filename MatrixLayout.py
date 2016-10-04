import numpy as np


def _rotate(l, n):
    return l[n:] + l[:n]


def layout_matrix_column_wise(matrix, runners, word_size):
    flattened = []
    runner_domains = [[] for i in range(runners)]
    runner = 0
    for start_column in range(0, matrix.shape[1], word_size):
        column_domain = []
        for row in range(matrix.shape[0]):
            for col in range(start_column, start_column + word_size):
                column_domain.append(matrix[row][col])
        runner_domains[runner].extend(column_domain)
        runner = (runner + 1) % runners

    for i in range(runners):
        runner_domains[i] = _rotate(runner_domains[i], i * -word_size)

    return np.array(runner_domains).flatten()

