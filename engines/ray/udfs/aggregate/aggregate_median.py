import ray
import pyarrow as pa
from ray.data.datatype import DataType
from ray.data.expressions import udf, col
import pyarrow.compute as pc


#  U29.	Median: Calculates median


from ray.data.aggregate import AggregateFnV2

from ray.data._internal.util import is_null
from ray.data.block import (
    AggType,
    Block,
    BlockAccessor,
    BlockColumnAccessor,
    KeyType,
    T,
    U,
)

from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Protocol,
    Set,
    TypeVar,
    Union,
)



class Aggregate_median(AggregateFnV2):

    def __init__(
        self,
        on: Optional[str] = None,
        ignore_nulls: bool = True,
        alias_name: Optional[str] = None,
    ):
        super().__init__(
            alias_name if alias_name else f"median({str(on)})",
            on=on,
            ignore_nulls=ignore_nulls,
            zero_factory=lambda: list, 
        )


    def aggregate_block(self, block: Block) -> AggType:
        block_tolist =block[self._target_col_name].to_pylist()
        return block_tolist

    def combine(self, accumulator: AggType, new: AggType) -> AggType:
        if not new:
            return accumulator
        accumulator.extend(new)
        return accumulator
    def finalize(self, accumulator: AggType) -> Optional[U]:
        if not accumulator:
            return None

        sorted_values = sorted(accumulator)
        n = len(sorted_values)

        if n % 2 == 0:
            mid = n // 2
            return float(sorted_values[mid - 1] + sorted_values[mid]) / 2.0
        else:
            return sorted_values[n // 2]
       