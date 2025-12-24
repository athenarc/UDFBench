from abc import ABC, abstractmethod
from types import SimpleNamespace
import pandas
from typing import TypeVar, Literal, Iterable, Dict, get_args
import inspect
import importlib.util
from typing import Literal
import datetime
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
SupportedPandasLike = Literal[
    'pandas',
    'modin',
    'fireducks'
]
SupportedPandasLikeValues = get_args(SupportedPandasLike)
class PandasQueryBase(ABC):
    
    def __init__(
        self,
        pd_module: SupportedPandasLike,
        schema_module,
        **udf_paths: str
    ):
        super().__init__()
        if pd_module not in SupportedPandasLikeValues:
            raise ValueError(
                f'Provided value for `pd_module` was {pd_module}. Use one of: ' +
                ", ".join(tuple(map(lambda s: f'`{s}`', SupportedPandasLikeValues)))
            )
        self.pd_module: Literal['pandas', 'modin', 'fireducks'] = pd_module
        scalar_udf_path = udf_paths.get('scalar_udf_path')
        aggr_udf_path = udf_paths.get('aggr_udf_path')
        table_udf_path = udf_paths.get('table_udf_path')
        if schema_module:
            self.schemas = SimpleNamespace(**dict(
                inspect.getmembers(schema_module, inspect.isclass)
            ))
        if scalar_udf_path:
            self.scalar_udfs = SimpleNamespace(**dict(
                inspect.getmembers(
                    load_module(scalar_udf_path),
                    inspect.isfunction
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

    def __read_df__(
        self,
        dataset_path: str,
        filename_no_ext: str,
        usecols: Iterable[str] | None,
        data_format: SupportedDataFormat,
    ) -> pandas.DataFrame:
        path = f'{dataset_path}/{filename_no_ext}' + (
            f'.{data_format}' if data_format != 'parquet' else ''
        )
        match data_format:
            case 'csv':
                if usecols:
                    cols = (usecols and list(map(int, usecols)))
                    data = self.pd.read_csv(
                        path,
                        usecols=cols,
                        header=None
                    )[cols]
                    data.columns = usecols
                    return data
                else:
                    return self.pd.read_csv(path, header=None)
            case 'parquet':
                if usecols:
                    cols = list(map(str, usecols or ()))
                    data = self.pd.read_parquet(
                        path,
                        columns=cols
                    )
                    data = data[list(map(int, cols))]
                    data.columns = usecols
                    return data
                else:
                    return self.pd.read_parquet(path)
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
            f'{self.pd_module}_output_{(df_name and (df_name + "_")) or ""}' +
            f'{datetime.datetime.now(datetime.timezone.utc).isoformat()}.{data_format}'
        )

    def __write_df__(
        self,
        df,
        data_format: SupportedDataFormat = 'csv',
        df_name: str = '',
        dir_path: str = ''
    ):
        file_name = self.__gen_output_filename__(
            dir_path, df_name, data_format
        )
        if data_format == 'csv':
            df.to_csv(file_name, header=False, index=False)
        elif data_format == 'parquet':
            df.to_parquet(file_name)
        else:
            raise ValueError(
                f'`data_format` value was `{data_format}`, expected `csv` or `parquet`'
            )

    @staticmethod
    def __create_data_file_path__(
        dataset_path: str,
        filename_no_ext: str,
        data_format: SupportedDataFormat | Literal['xml', 'json', 'txt']
    ):
        return f'{dataset_path}/{filename_no_ext}.{data_format}'
    
    @staticmethod
    def __time_fn__(fn, msg = None):
        import time
        import psutil, os

        def get_cpu_time_in_ms():
            parent = psutil.Process(os.getpid())
            total = 0.0
            try:
                pt= parent.cpu_times()
                total = pt.user + pt.system
                for child in parent.children(recursive=True):
                    try:
                        ct = child.cpu_times()
                        total += ct.user + ct.system
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            return total * 1000.0
        
        start_cpu = get_cpu_time_in_ms()
        start = time.time()
        res = fn()
        end = time.time()
        end_cpu = get_cpu_time_in_ms()

        if msg == 'Modin Execution Time' or  msg == 'Pandas Execution Time':
            print(f'Execution Time: {(end-start)*1000:.3f} ms\n')
            print(f'Process Time: {(end_cpu-start_cpu):.3f} ms\n')

        return res
    
    def __modin_init__(self):
        # Use this block when benchmarking Modin

        # import os
        # if os.environ['MODIN_ENGINE'].lower().strip() == 'ray':
        #     import ray
        #     # Force warmup
        #     ray.init(num_cpus=int(os.environ['MODIN_CPUS']))
        # from modin.config import BenchmarkMode, LogMode
        # # Lazy off
        # BenchmarkMode.put(True)
        # # Logging on
        # LogMode.put(True)
        
        # End
        
        import modin.pandas
        self.pd = modin.pandas
    
    def exec(
        self,
        dataset_path: str,
        data_format: SupportedDataFormat,
        external_data_path: str
    ):
        match self.pd_module:
            case 'modin':
                self.__time_fn__(lambda: self.__modin_init__(), 'Modin Init')
            case 'pandas':
                import pandas
                self.pd = pandas
            case _:
                raise ValueError(
                    f'Invalid `pd_module`: {self.pd_module}.'
                )
            
        # print('Results length: ' + str(len(
        self.__time_fn__(
            lambda: self.__exec__(
                dataset_path, data_format, external_data_path
            ),
            f"{self.pd_module.capitalize()} Execution Time"
        )            
        # )))
    
    def execUsingCtx(
        self,
        dataset_path: str,
        data_format: SupportedDataFormat,
        external_data_path: str,
        modin_ctx: Dict[str, any]
    ):        
        def __execUsingCtx__():
            import modin.config
            with modin.config.context(**modin_ctx):
                import modin.pandas
                self.pd = modin.pandas
                return self.__exec__(
                    dataset_path, data_format, external_data_path
                )
                    
        # print('Results length: ' + str(len(
        self.__time_fn__(
            __execUsingCtx__,
            f"{self.pd_module.capitalize()} Execution Time"
        )            
        # )))    
    
    @abstractmethod
    def __exec__(
        self,
        dataset_path: str,
        data_format: SupportedDataFormat,
        external_data_path: str
    ):
        raise NotImplementedError(
            'The `query` method of abstract base class '
            'PandasQueryBase` has not been implemented.'
        )    
