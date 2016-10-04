import unittest
from MatrixLayout import layout_matrix_column_wise
import numpy as np


class Layout(unittest.TestCase):

    def setUp(self):
        self.matrix = np.array([
            [1,   2,  3,  4,  5,  6,  7,  8,  9, 10, 101, 102],
            [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 201, 202],
            [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 301, 302],
            [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 401, 402],
            [41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 501, 502],
            [51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 601, 602]
        ])

    def test_layout_matrix_columnwise(self):
        laid_out = layout_matrix_column_wise(self.matrix, 3, 2)
        correct = np.array([
            1, 2, 11, 12, 21, 22, 31, 32, 41, 42, 51, 52,
            7, 8, 17, 18, 27, 28, 37, 38, 47, 48, 57, 58,

            59, 60,
            3, 4, 13, 14, 23, 24, 33, 34, 43, 44, 53, 54,
            9, 10, 19, 20, 29, 30, 39, 40, 49, 50,

            501, 502, 601, 602,
            5, 6, 15, 16, 25, 26, 35, 36, 45, 46, 55, 56,
            101, 102, 201, 202, 301, 302, 401, 402,
        ])
        self.assertTrue((laid_out == correct).all())
