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


class ColumnTrain:
    def __init__(self, runners, word_size, matrix_shape, ram_access,
                 x_bus_stream, offset_stream):

        assert len(x_bus_stream()) == runners * word_size

        self.matrix_shape = matrix_shape
        self.runners = runners
        self.word_size = word_size

        self._offset_stream = offset_stream

        self._runners = [None] * runners
        self._w_streams = [None] * runners
        for i in range(runners):
            x_stream = self._make_x_stream(x_bus_stream, i)

            matrix_index = i*(runners + 1)*word_size
            self._w_streams[i] = self._make_w_stream(ram_access, i)

            prev_prefix_y_stream = \
                self._runners[i-1].prefix_y_stream() if i > 0 else lambda: 0

            self._runners[i] = ColumnRunner(
                x_stream,
                self._w_streams[i],
                prev_prefix_y_stream
            )

    def _make_x_stream(self, x_bus_stream, i):
        return lambda: x_bus_stream()[i*self.word_size:(i+1)*self.word_size]

    def _make_w_stream(self, ram_access, i):
        shard_length = self.matrix_shape[0]*self.matrix_shape[1] // self.runners
        return lambda: ram_access(
            ((self._offset_stream()*self.word_size) % shard_length) + i*shard_length,
            self.word_size)

    def propagate_combinatorial_logic(self):
        for runner in self._runners:
            runner.propagate_combinatorial_logic()

    def tick(self):
        for runner in self._runners:
            runner.tick()

    def y_stream(self):
        return self._runners[-1].prefix_y_stream()


class ColumnCore:
    def __init__(self, runners, word_size, matrix_shape,
                 ram, ram_offset, x_bus_stream, reset_stream):
        assert matrix_shape[0] % (runners * word_size) == 0

        self.runners = runners
        self.word_size = word_size
        self._ram = ram
        self._matrix_shape = matrix_shape

        self._cycle_time = matrix_shape[0] * (matrix_shape[1]  // (runners * word_size))
        self._reset_stream = reset_stream
        self._tick_counter = -1
        self._next_tick_counter = -1

        def rolling_x_bus_stream():
            rolling_x_bus = []
            for i in range(runners):
                step = ((self._cycle_time + self._tick_counter - i) % self._cycle_time) // matrix_shape[0]
                rolling_x_bus.append(x_bus_stream()[(step*runners + i)*word_size:(step*runners + i + 1)*word_size])

            return np.array(rolling_x_bus).flatten()

        self._train = ColumnTrain(
            runners=runners,
            word_size=word_size,
            matrix_shape=matrix_shape,
            ram_access=ram.get_values,
            x_bus_stream=rolling_x_bus_stream,
            offset_stream=lambda: ram_offset + self._tick_counter
        )

        self._y_accumulator_ram_offset = ram.add_content(np.zeros(matrix_shape[0], dtype=np.int))

    def propagate_combinatorial_logic(self):
        self._train.propagate_combinatorial_logic()

        self._next_tick_counter = (self._tick_counter + 1) % self._cycle_time

    def tick(self):
        self._train.tick()

        y_acc_offset = (self._tick_counter + self._matrix_shape[0] - self.runners + 1) % self._matrix_shape[0]
        next_y_accumulator = 0
        if (self._tick_counter + self._cycle_time - self.runners + 1) % self._cycle_time >= self._matrix_shape[0]:
            next_y_accumulator += self._ram.get_values(self._y_accumulator_ram_offset + y_acc_offset, 1)[0]
        next_y_accumulator += self._train.y_stream()()
        self._ram.put_values(self._y_accumulator_ram_offset + y_acc_offset, np.array([next_y_accumulator]))

        if self._reset_stream() == 1:
            self._tick_counter = 0
        else:
            self._tick_counter = self._next_tick_counter

    def y_stream(self):
        y_acc_offset = ((self._tick_counter + self._matrix_shape[0] - self.runners) % self._matrix_shape[0])
        return lambda: self._ram.get_values(self._y_accumulator_ram_offset + y_acc_offset, 1)
