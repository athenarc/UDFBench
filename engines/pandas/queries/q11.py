import q10

class Q11(q10.Q10):
    @property
    def __kmeans__(self) -> q10.Q10.KMeansFn:
        return self.table_udfs.kmeans_recursive
