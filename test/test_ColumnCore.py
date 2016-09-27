import unittest
from Core import ColumnCore
import numpy as np


class TestColumnRunner(unittest.TestCase):
    def setUp(self):
        matrix = np.array([
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        ])
        matrix = matrix.flatten()

        def ram(addr, width):
            r = matrix[addr:addr+width]
            if len(r) < width:
                r = np.array([0] * width)
            return r

        self.x_bus = np.zeros(6)
        self.start = 0
        self.offset = 0

        self.core = ColumnCore(
            width=3,
            word_size=2,
            row_width=12,
            ram=ram,
            x_bus_stream=lambda: self.x_bus,
            start_stream=lambda: self.start,
            offset_stream=lambda: self.offset
        )
        self.y_stream = self.core.y_stream()

    def do_cycle(self, x_bus, start, offset):
        self.x_bus = x_bus
        self.start = start
        self.offset = offset

        self.core.propagate_combinatorial_logic()
        self.core.tick()

        return self.y_stream()

    def test_full(self):
        # Run 1 over the first six columns
        x_bus = np.array([1, 0, 1, 0, 1, 1])

        self.do_cycle(x_bus, start=1, offset=0)

        self.do_cycle(x_bus, start=0, offset=-1)
        self.do_cycle(x_bus, start=0, offset=-1)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 5)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 2)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 4)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 3)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 3)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 5)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 3)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 4)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 5)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 4)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 2)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 3)

        # Run 2 over the last six columns
        x_bus = np.array([1, 1, 1, 0, 0, 0])

        self.do_cycle(x_bus, start=1, offset=6)

        self.do_cycle(x_bus, start=0, offset=-1)
        self.do_cycle(x_bus, start=0, offset=-1)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 2)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 0)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 2)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 2)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 0)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 1)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 1)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 2)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 2)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 1)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 1)
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 2)


if __name__ == '__main__':
    unittest.main()
