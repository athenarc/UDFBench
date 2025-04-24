#  U29.	Median: Calculates median

class aggregate_median:
    registered=True #Value to define db operator

    def __init__(self):
        self.init=True
        self.sample = []
        self.counter=0

    def initargs(self, args):
        self.init=False
        if not args:
            raise functions.OperatorError("median","No arguments")
        if len(args)>1:
            raise functions.OperatorError("median","Wrong number of arguments")

    def step(self, *args):
        if self.init==True:
            self.initargs(args)

        if not(isinstance(args[0], str)) and args[0]:
            self.counter +=1
            self.element = float((args[0]))
            self.sample.append(self.element)

    def final(self):
        if (not self.sample):
            return
        self.sample.sort()

        """Determine the value which is in the exact middle of the data set."""
        if self.counter % 2:  # Number of elements in data set is odd.
            self.median = self.sample[self.counter // 2]
        else:  # Number of elements in data set is even.
            midpt = self.counter // 2
            self.median = (self.sample[midpt - 1] + self.sample[midpt]) / 2.0

        return self.median
