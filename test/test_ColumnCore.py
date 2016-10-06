import unittest
from Core import ColumnCore
from Ram import Ram
import numpy as np
from MatrixLayout import layout_matrix_column_wise


class TestColumnCore(unittest.TestCase):
    def setUp(self):
        matrix = np.array([
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 1, 1, 0],
            [1, 1, 1, 0, 0, 0, 1, 1],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 1, 1, 0, 1, 0, 1],
            [0, 1, 1, 1, 1, 0, 0, 1],
            [0, 1, 0, 1, 0, 1, 1, 0],
            [1, 1, 0, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 1, 0, 1, 0, 0],
        ])
        laid_out_matrix = layout_matrix_column_wise(matrix, 2, 2)

        ram = Ram()
        ram_offset = ram.add_content(laid_out_matrix)
        self._x_bus = np.zeros(8, dtype=np.int)
        self._reset = 0

        self._core = ColumnCore(
            runners=2,
            word_size=2,
            matrix_shape=matrix.shape,
            ram=ram,
            ram_offset=ram_offset,
            x_bus_stream=lambda: self._x_bus,
            reset_stream=lambda: self._reset
        )

    def do_cycle(self):
        self._core.propagate_combinatorial_logic()
        self._core.tick()

        return self._core.y_stream()()

    def test_full(self):
        # --- First multiplication ---
        # Vector: [1, 0, 1, 0, 1, 1, 1, 1]
        self._reset = 1
        self.do_cycle()
        self._reset = 0
        # First train pass
        self._x_bus = np.array([1, 0, -1, -1, -1, -1, -1, -1])
        self.do_cycle()
        self._x_bus = np.array([1, 0, 1, 0, -1, -1, -1, -1])
        self.assertEqual(4, self.do_cycle())
        self._x_bus = np.array([1, 0, 1, 0, 1, 1, -1, -1])
        self.assertEqual(2, self.do_cycle())
        self._x_bus = np.array([1, 0, 1, 0, 1, 1, 1, 1])
        self.assertEqual(2, self.do_cycle())
        self.assertEqual(2, self.do_cycle())
        self.assertEqual(1, self.do_cycle())
        self.assertEqual(4, self.do_cycle())
        self.assertEqual(2, self.do_cycle())
        self.assertEqual(3, self.do_cycle())
        self.assertEqual(4, self.do_cycle())
        self.assertEqual(3, self.do_cycle())
        self.assertEqual(1, self.do_cycle())
        self.assertEqual(2, self.do_cycle())

        # Second train pass
        self.assertEqual(6, self.do_cycle())
        self.assertEqual(2, self.do_cycle())
        self.assertEqual(6, self.do_cycle())
        self.assertEqual(4, self.do_cycle())
        self.assertEqual(3, self.do_cycle())
        self.assertEqual(6, self.do_cycle())
        self.assertEqual(4, self.do_cycle())
        self.assertEqual(5, self.do_cycle())
        self.assertEqual(6, self.do_cycle())
        self.assertEqual(4, self.do_cycle())
        self.assertEqual(3, self.do_cycle())
        self._x_bus = np.array([1, 1, -1, -1, -1, -1, 1, 1])
        self.assertEqual(5, self.do_cycle())

        # --- Second multiplication ---
        # Vector: [1, 1, 0, 0, 0, 0, 1, 1]

        # First train pass
        self._x_bus = np.array([1, 1, 0, 0, -1, -1, -1, -1])
        self.assertEqual(2, self.do_cycle())
        self.assertEqual(2, self.do_cycle())
        self.assertEqual(2, self.do_cycle())
        self.assertEqual(0, self.do_cycle())
        self.assertEqual(1, self.do_cycle())
        self.assertEqual(2, self.do_cycle())
        self.assertEqual(4, self.do_cycle())
        self.assertEqual(3, self.do_cycle())
        self.assertEqual(2, self.do_cycle())
        self.assertEqual(1, self.do_cycle())
        self.assertEqual(3, self.do_cycle())
        self._x_bus = np.array([1, 1, 0, 0, 0, 0, -1, -1])
        self.assertEqual(2, self.do_cycle())

        # Second train pass
        self._x_bus = np.array([1, 1, 0, 0, 0, 0, 1, 1])
        self.assertEqual(4, self.do_cycle())
        self.assertEqual(4, self.do_cycle())
        self.assertEqual(4, self.do_cycle())
        self.assertEqual(2, self.do_cycle())
        self.assertEqual(1, self.do_cycle())
        self.assertEqual(4, self.do_cycle())
        self.assertEqual(6, self.do_cycle())
        self.assertEqual(5, self.do_cycle())
        self.assertEqual(4, self.do_cycle())
        self.assertEqual(2, self.do_cycle())
        self.assertEqual(5, self.do_cycle())
        self.assertEqual(5, self.do_cycle())
