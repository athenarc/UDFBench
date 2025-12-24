import ray
import pyarrow as pa
from ray.data.datatype import DataType
from ray.data.expressions import udf, col
import pyarrow.compute as pc




#  U27.	Count: Calculates count 


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



class Aggregate_count(AggregateFnV2):
    def __init__(
        self,
        on: Optional[str] = None,
        ignore_nulls: bool = False,
        alias_name: Optional[str] = None,
    ):
        super().__init__(
            alias_name if alias_name else f"count({on or ''})",
            on=on,
            ignore_nulls=ignore_nulls,
            zero_factory=lambda: 0,
        )

    def aggregate_block(self, block: Block) -> AggType:

        if self._target_col_name is None:
            return len(block)

        return pc.count(block[self._target_col_name])


    def combine(self, current_accumulator: AggType, new: AggType) -> AggType:
        return current_accumulator + new
