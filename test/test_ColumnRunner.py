import unittest
from Core import ColumnRunner
import numpy as np


class TestColumnRunner(unittest.TestCase):
    def setUp(self):
        self.x = None
        self.parameter = None
        self.prev_y_prefix = None

        def x_stream(): return self.x

        def parameter_stream(): return self.parameter

        def prev_y_prefix_stream(): return self.prev_y_prefix

        self.runner = ColumnRunner(x_stream, parameter_stream, prev_y_prefix_stream)
        self.prefix_y_stream = self.runner.prefix_y_stream()

    def do_cycle(self, x, parameter, prev_y_prefix):
        self.x = np.array(x)
        self.parameter = np.array(parameter)
        self.prev_y_prefix = np.array(prev_y_prefix)

        self.runner.propagate_combinatorial_logic()
        self.runner.tick()

        return self.prefix_y_stream()

    def test_zero_driving(self):
        result = self.do_cycle([0, 0], [0, 0], 0)
        self.assertTrue(0 == result)

    def test_single_cycle(self):
        result = self.do_cycle([0, 1, 1, 0], [0, 0, 1, 1], 5)
        self.assertEqual(result, 7)

    def test_multiple_cycles(self):
        result = self.do_cycle([0, 1, 1, 0], [0, 0, 1, 1], 5)
        self.assertEqual(result, 7)

        result = self.do_cycle([0, 1, 1, 0], [1, 1, 1, 0], 5)
        self.assertEqual(result, 6)

        result = self.do_cycle([0, 1, 1, 0], [0, 0, 0, 1], 5)
        self.assertEqual(result, 8)


if __name__ == '__main__':
    unittest.main()
