import unittest
from Core import ColumnTrain
import numpy as np
from MatrixLayout import layout_matrix_column_wise


class TestColumnTrain(unittest.TestCase):
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
        laid_out_matrix = layout_matrix_column_wise(matrix, 3, 2)

        def ram(addr, width):
            r = laid_out_matrix[addr:addr+width]
            if len(r) < width:
                r = np.array([0] * width)
            return r

        self.x_bus = np.zeros(6)
        self.start = 0
        self.offset = 0

        self.train = ColumnTrain(
            runners=3,
            word_size=2,
            matrix_shape=matrix.shape,
            ram=ram,
            x_bus_stream=lambda: self.x_bus,
            start_stream=lambda: self.start,
            offset_stream=lambda: self.offset
        )
        self.y_stream = self.train.y_stream()

    def do_cycle(self, x_bus, start, offset):
        self.x_bus = x_bus
        self.start = start
        self.offset = offset

        self.train.propagate_combinatorial_logic()
        self.train.tick()

        return self.y_stream()

    def test_full(self):

        x_bus_1 = [1, 0, 1, 0, 1, 1]
        x_bus_2 = [1, 1, 1, 0, 0, 0]

        x_bus = np.array(x_bus_1)

        # Run 1 over the first six columns
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
        x_bus = np.array(x_bus_2[:2] + x_bus_1[2:])
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 2)
        x_bus = np.array(x_bus_2[:4] + x_bus_1[4:])
        self.assertEqual(self.do_cycle(x_bus, start=0, offset=-1), 3)
        x_bus = np.array(x_bus_2)

        # Run 2 over the last six columns

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
