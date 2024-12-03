class aggregate_avg:
    registered=True
    def __init__(self):
        self.ssum = 0
        self.scount = 0
    def step(self,val):
      if val is not None:
        self.ssum += val
        self.scount += 1 
    def final(self):
         return self.ssum*1.0/self.scount


class aggregate_count:
    registered=True
    def __init__(self):
        self.scount = 0
    def step(self,val):
        self.scount += 1
    def final(self):
         return self.scount


class aggregate_max:
    registered=True
    def __init__(self):
        self.max = None
    def step(self,val):
        try:
          if val>self.max:
              self.max = val
        except:
          self.max = val
    def final(self):
         return self.max


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
