import queue

class aggregate_top:
    registered=True
    multiset=True


    def __init__(self):
        self.topn=None
        self.size=None
        self.lessval=None
        self.stepsnum=0
        self.argnum = 1

    def step(self, *args):
        if not self.size:
            self.size=int(args[0])
            self.topn=queue.PriorityQueue(self.size)
            self.argnum = len(args)-2
        inparg=args[1]
        outarg=args[2:]

        if not self.topn.full():
            self.topn.put_nowait((inparg,outarg))
        else:
            inparg_old , outarg_old=self.topn.get_nowait()     
            self.topn.put_nowait(max((inparg,outarg),(inparg_old ,outarg_old)))

        self.stepsnum+=1


    def final(self):
        output=[]
        if self.topn:
            while not self.topn.empty():
                output+=[self.topn.get_nowait()[1]]

        yield tuple(["top"+str(i+1) for i in range(self.argnum)])

        for el in reversed(output):
            yield el
