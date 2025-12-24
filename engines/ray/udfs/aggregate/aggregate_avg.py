import json
import ray
import pyarrow as pa
from ray.data.datatype import DataType
from ray.data.expressions import udf, col
import pyarrow.compute as pc
import numpy as np


#  U26.	Avg: Calculates average

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

class Aggregate_avg(AggregateFnV2):


    def __init__(
        self,
        on: Optional[str] = None,
        ignore_nulls: bool = True,
        alias_name: Optional[str] = None,
    ):
        super().__init__(
            alias_name if alias_name else f"avg({str(on)})",
            on=on,
            ignore_nulls=ignore_nulls,
            zero_factory=lambda: list([0, 0]),  
        )

    def aggregate_block(self, block: Block) -> AggType:
        count = pc.count(block[self._target_col_name])
        if count == 0 or count is None:
            return None

        sum_ = pc.sum(block[self._target_col_name])
        if is_null(sum_):
            return sum_
        return [sum_, count]

    def combine(self, current_accumulator: AggType, new: AggType) -> AggType:
        return [current_accumulator[0] + new[0], current_accumulator[1] + new[1]]

    def finalize(self, accumulator: AggType) -> Optional[U]:
        if accumulator[1] == 0:

            return np.nan

        return accumulator[0] / accumulator[1]
