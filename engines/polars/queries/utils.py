from abc import ABC, abstractmethod
from types import SimpleNamespace
from typing import TypeVar, Literal, Iterable, Sequence, TypedDict
import inspect
import importlib.util
from typing import Literal
import datetime
import polars as pl
from ordered_set import OrderedSet
import os

def load_module(module_full_path: str):
    module_name = os.path.splitext(
        os.path.basename(module_full_path)
    )[0]
    # Load the module dynamically
    spec = assert_expr(
        importlib.util.spec_from_file_location(
            module_name, module_full_path
        ),
        f'Failed to get ModuleSpec for {module_full_path}'
    )
    module = importlib.util.module_from_spec(spec)
    assert_expr(spec.loader, 'Spec Loader is None').exec_module(module)
    return module

T = TypeVar("T")
def assert_expr(expr: T | None, error_msg: str | None = None) -> T:
    if (expr is None):
        raise ValueError(f'Unexpected `None` value: {error_msg}')
    return expr

SupportedDataFormat = Literal['csv', 'parquet']
class UDFPathKwargs(TypedDict, total=False):
    scalar_udf_path: str
    agg_udf_path: str
    table_udf_path: str
class PolarsQueryBase(ABC):
    
    def __init__(
        self,
        schema_module,
        **udf_paths,
        # **udf_paths: Unpack[UDFPathKwargs]
    ):
        super().__init__()
        scalar_udf_path = udf_paths.get('scalar_udf_path')
        aggr_udf_path = udf_paths.get('aggr_udf_path')
        table_udf_path = udf_paths.get('table_udf_path')
        if schema_module:
            self.schemas = SimpleNamespace(**dict(
                inspect.getmembers(
                    schema_module,
                    lambda m: type(m) is OrderedSet
                )
            ))
        if scalar_udf_path:
            self.scalar_udfs = SimpleNamespace(**dict(
                inspect.getmembers(
                    load_module(scalar_udf_path),
                )
            ))
        if aggr_udf_path:
            self.aggr_udfs = SimpleNamespace(**dict(
                inspect.getmembers(
                    load_module(aggr_udf_path),
                    inspect.isfunction
                )
            ))
        if table_udf_path:
            self.table_udfs = SimpleNamespace(**dict(
                inspect.getmembers(
                    load_module(table_udf_path),
                    inspect.isfunction
                )
            ))

    def __scan_df__(
        self,
        dataset_path: str,
        filename_no_ext: str,
        data_format: SupportedDataFormat,
        col_names: Sequence[str],
        select_cols: Iterable[str] | None = None,
    ) -> pl.LazyFrame:
        path = PolarsQueryBase.__create_data_file_path__(
            dataset_path,
            filename_no_ext + (
                f'.{data_format}' if data_format != 'parquet' else ''
            )
        )
        match data_format:
            case 'csv':
                if select_cols:
                    return pl.scan_csv(
                        path, has_header=False, new_columns=col_names
                    ).select(select_cols)
                else:
                    return pl.scan_csv(path, has_header=False)
            case 'parquet':
                if select_cols:
                    return pl.scan_parquet(path).rename({
                        str(i): col for i, col in enumerate(col_names)
                    }).select(col_names)
                else:
                    return pl.scan_parquet(path)
            case _:
                raise ValueError(
                    f'`data_format` value was `{data_format}`, expected `csv` or `parquet`'
                )
            
    def __gen_output_filename__(
        self,
        dir_path: str,
        df_name: str,
        data_format: SupportedDataFormat
    ) -> str:
        return (
            ((dir_path and (dir_path + "/")) or "") +
            f'polars_output_{(df_name and (df_name + "_")) or ""}' +
            f'{datetime.datetime.now(datetime.timezone.utc).isoformat()}.{data_format}'
        )

    def __write_df__(
        self,
        df: pl.DataFrame,
        data_format: SupportedDataFormat = 'csv',
        df_name: str = '',
        dir_path: str = ''
    ):
        file_name = self.__gen_output_filename__(
            dir_path, df_name, data_format
        )
        if data_format == 'csv':
            df.write_csv(file_name, include_header=False)
        elif data_format == 'parquet':
            df.write_parquet(file_name)
        else:
            raise ValueError(
                f'`data_format` value was `{data_format}`, expected `csv` or `parquet`'
            )

    @staticmethod
    def __create_data_file_path__(dataset_path: str, filename: str,):
        return f'{dataset_path}/{filename}'
    
    @staticmethod
    def __time_fn__(fn, msg = None):
        import time
        start = time.time()
        startp = time.process_time()

        # print(f'[START]: {msg} - {datetime.datetime.fromtimestamp(start, datetime.timezone(datetime.timedelta(hours=3))).strftime("%H:%M:%S")}')
        res = fn()
        end = time.time()
        endp = time.process_time()
        # print(f'[END]: {msg} - {datetime.datetime.fromtimestamp(end, datetime.timezone(datetime.timedelta(hours=3))).strftime("%H:%M:%S")}')
        # print(f'{msg or "Time Elapsed"}: {(end-start)*1000} ms')
        print(f'Execution Time: {(end-start)*1000:.3f} ms\n')
        print(f'Process Time: {(endp-startp)*1000} ms')
        return res
    
    def exec(
        self,
        dataset_path: str,
        data_format: SupportedDataFormat,
        external_data_path: str
    ):            
        # print('Results length: ' + str(len(
        self.__time_fn__(
            lambda: self.__exec__(
                dataset_path, data_format, external_data_path
            ),
            'Polars Execution Time'
        )            
        # )))
    
    @abstractmethod
    def __exec__(
        self,
        dataset_path: str,
        data_format: SupportedDataFormat,
        external_data_path: str
    ) -> pl.DataFrame:
        raise NotImplementedError(
            'The `query` method of abstract base class '
            'PolarsQueryBase` has not been implemented.'
        )
