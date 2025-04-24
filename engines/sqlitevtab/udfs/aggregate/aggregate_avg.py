#  U26.	Avg: Calculates average


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

