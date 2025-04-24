# U29.	Median(v2): Calculates median with quickselect

import random

class aggregate_median_v2:
    registered = True

    def __init__(self):
        self.init = True
        self.sample = []
        self.counter = 0

    def initargs(self, args):
        self.init = False
        if not args:
            raise functions.OperatorError("median", "No arguments")
        if len(args) > 1:
            raise functions.OperatorError("median", "Wrong number of arguments")

    def step(self, *args):
        if self.init:
            self.initargs(args)

        if not isinstance(args[0], str) and args[0] is not None:
            self.counter += 1
            self.sample.append(int(args[0]) if isinstance(args[0], int) else float(args[0]))

    def partition(self, low, high):
        pivot = self.sample[(low + high) // 2]
        left = low
        right = high
        while True:
            while self.sample[left] < pivot:
                left += 1
            while self.sample[right] > pivot:
                right -= 1
            if left >= right:
                return right
            self.sample[left], self.sample[right] = self.sample[right], self.sample[left]
            left += 1
            right -= 1

    def quickselect(self, k):
        low, high = 0, self.counter - 1
        while low < high:
            pivot_index = self.partition(low, high)
            if pivot_index < k:
                low = pivot_index + 1
            else:
                high = pivot_index
        return self.sample[k]

    def final(self):
        if not self.sample:
            return None

        mid = self.counter // 2
        if self.counter % 2:
            return self.quickselect(mid)*1.0
        else: 
            left = self.quickselect(mid - 1)
            right = self.quickselect(mid)
            return (left + right) / 2
