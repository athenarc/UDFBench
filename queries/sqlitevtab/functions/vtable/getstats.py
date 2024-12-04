from . import setpath
from . import vtbase
import functions
import numpy as np


### Classic stream iterator
registered=True

class getstats(vtbase.VT):
    def VTiter(self, *parsedArgs, **envars):
        largs, dictargs = self.full_parse(parsedArgs)

        self.nonames=True
        self.names=[]
        self.types=[]

        if 'query' not in dictargs:
            raise functions.OperatorError(__name__.rsplit('.')[-1],"No query argument ")
        query=dictargs['query']

        cur = envars['db'].cursor()
        c=cur.execute(query)
        rows = c.fetchall()
        yield ('c1', 'c2')
        try:
            value_column_np = np.array([row[0] for row in rows])
            value_column_np = value_column_np[value_column_np !=None]
            avg_values=np.average(value_column_np)
            median_values = np.ma.median(value_column_np)
            yield (avg_values,median_values)
        except:
            raise

def Source():
    return vtbase.VTGenerator(getstats)
