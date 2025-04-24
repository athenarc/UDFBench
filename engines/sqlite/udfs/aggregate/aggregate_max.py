#  U28. Calculates max date

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
