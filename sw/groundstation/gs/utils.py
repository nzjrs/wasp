def calculate_dt_seconds(then, now):
    d = now - then
    return d.seconds + d.microseconds / 1000000.0

def has_elapsed_time_passed(then, now, dt):
    ds = calculate_dt_seconds(then, now)
    if ds > dt:
        return now, True, ds
    else:
        return then, False, ds

class MovingAverage:
    def __init__(self, length, contains=float):
        self._type = contains
        self._len = length
        self._d = [contains()] * length
        self._i = 0
        self._num_added = 0

    def add(self, val):
        self._i = (self._i + 1) % self._len
        self._d[self._i] = self._type(val)
        self._num_added += 1

    def average(self):
        return self._type(sum(self._d) / float(min(self._len, self._num_added)))
