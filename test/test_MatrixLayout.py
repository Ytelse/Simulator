import unittest
from MatrixLayout import layout_matrix_column_wise
import numpy as np


class Layout(unittest.TestCase):

    def setUp(self):
        self.matrix = np.array([
            [1,   2,  3,  4,  5,  6,  7,  8,  9, 10],
            [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
            [31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
            [41, 42, 43, 44, 45, 46, 47, 48, 49, 50],
            [51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
        ])

    def test_layout_matrix_columnwise(self):
        laid_out = layout_matrix_column_wise(self.matrix, 2)
        correct = np.array([
            1, 2, 11, 12, 21, 22, 31, 32, 41, 42, 51, 52,
            13, 14, 23, 24, 33, 34, 43, 44, 53, 54, 3, 4,
            25, 26, 35, 36, 45, 46, 55, 56, 5, 6, 15, 16,
            37, 38, 47, 48, 57, 58, 7, 8, 17, 18, 27, 28,
            49, 50, 59, 60, 9, 10, 19, 20, 29, 30, 39, 40,
        ])
        self.assertTrue((laid_out == correct).all())
