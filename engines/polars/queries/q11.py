from typing import Callable
import q10
import polars as pl

class Q11(q10.Q10):
    @property
    def __kmeans__(self) -> Callable[
        [
            pl.DataFrame,
            str,
            str,
            str,
            int,
        ],
        pl.DataFrame
    ]:
        return self.table_udfs.kmeans_recursive
