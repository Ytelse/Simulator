import numpy as np


class ColumnRunner:
    def __init__(self, x_stream, w_stream, prev_prefix_y_stream):
        self._x_stream = x_stream
        self._w_stream = w_stream
        self._prev_prefix_y_stream = prev_prefix_y_stream
        self._combinatorial_value = -1
        self._prefix_y_value = -1

    def propagate_combinatorial_logic(self):
        self._combinatorial_value = sum(self._x_stream() ^ self._w_stream()) +\
                            self._prev_prefix_y_stream()

    def tick(self):
        self._prefix_y_value = self._combinatorial_value

    def prefix_y_stream(self):
        return lambda: self._prefix_y_value


class ColumnCore:
    def __init__(self, width, word_size, row_width, ram,
                 x_bus_stream, start_stream, offset_stream):

        assert len(x_bus_stream()) == width * word_size

        self.row_width = row_width
        self.width = width
        self.word_size = word_size

        self._start_stream = start_stream
        self._offset_stream = offset_stream

        self._offset_value = -1
        self._next_offset_value = -1

        self._runners = [None] * width
        self._w_streams = [None] * width
        for i in range(width):
            x_stream = self._make_x_stream(x_bus_stream, i)

            matrix_index = i*(width + 1)*word_size
            self._w_streams[i] = self._make_w_stream(ram, i)

            prev_prefix_y_stream = \
                self._runners[i-1].prefix_y_stream() if i > 0 else lambda: 0

            self._runners[i] = ColumnRunner(
                x_stream,
                self._w_streams[i],
                prev_prefix_y_stream
            )

    def _make_x_stream(self, x_bus_stream, i):
        return lambda: x_bus_stream()[i*self.word_size:(i+1)*self.word_size]

    def _make_w_stream(self, ram, i):
        return lambda: ram(
            self._offset_value - i*(self.row_width - self.word_size),
            self.word_size)

    def propagate_combinatorial_logic(self):
        for runner in self._runners:
            runner.propagate_combinatorial_logic()

        self._next_offset_value = self._offset_value + self.row_width

    def tick(self):
        for runner in self._runners:
            runner.tick()

        if self._start_stream() == 1:
            self._offset_value = self._offset_stream()
        else:
            self._offset_value = self._next_offset_value

    def y_stream(self):
        return self._runners[-1].prefix_y_stream()
