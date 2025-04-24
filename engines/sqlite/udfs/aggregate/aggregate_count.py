#  U27.	Count: Calculates count 

class aggregate_count:
    registered=True
    def __init__(self):
        self.scount = 0
    def step(self,val):
        self.scount += 1
    def final(self):
         return self.scount
