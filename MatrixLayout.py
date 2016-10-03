import numpy as np


def _rotate(l, n):
    return l[n:] + l[:n]


def layout_matrix_column_wise(matrix, word_size):
    flattened = []
    for start_column in range(0, matrix.shape[1], word_size):
        column_domain = []
        for row in range(matrix.shape[0]):
            for col in range(start_column, start_column + word_size):
                column_domain.append(matrix[row][col])
        column_domain = _rotate(column_domain, start_column)
        flattened.extend(column_domain)

    return np.array(flattened)

