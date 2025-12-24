import itertools
import polars as pl
import numpy as np
from typing import Literal
import json
from lxml import etree
import csv
from sklearn.cluster import KMeans

def extractfromdate(arg: str):
    try:
        return np.array((
            int(arg[:arg.find('-')]),
            int(arg[arg.find('-')+1:arg.rfind('-')]),
            int(arg[arg.rfind('-')+1:])
        ))
    except:
        return np.array((-1, -1, -1))
    
def get_stats_alt(lf: pl.LazyFrame):
    return lf.with_columns(
        pl.col('authors'),
        pl.col('authors').is_null().alias('is_null'),
    ).select(
        pl.when(pl.all('is_null')).then(np.nan).otherwise(
            pl.col('authors').map_batches(
                lambda s: np.nanmean(s.to_numpy()),
                return_dtype=pl.Float64,
                returns_scalar=True,
            )
        ).alias('avg'),
        pl.when(pl.all('is_null')).then(np.nan).otherwise(
            pl.col('authors').map_batches(
                lambda s: np.nanmedian(s.to_numpy()),
                return_dtype=pl.Float64,
                returns_scalar=True,
            )
        ).alias('median'),
    )

def get_stats(lf: pl.LazyFrame):
    def get_mean_median(s: pl.Series):
        arr = s.to_numpy()
        return {
            "avg": np.nanmean(arr),
            "median": np.nanmedian(arr)
        }
    
    return lf.with_columns(
        pl.col('authors'),
        pl.col('authors').is_null().alias('is_null'),
    ).select(
        pl.when(pl.all('is_null')).then(
            pl.struct(avg=np.nan, median=np.nan)
        ).otherwise(
            pl.col('authors').map_batches(
                get_mean_median,
                return_dtype=pl.Struct([
                    pl.Field("avg", pl.Float64),
                    pl.Field("median", pl.Float64)
                ]),
                returns_scalar=True,
            )
        ).alias('stats')
    ).unnest('stats')

def file(
    path: str,
    file_type: Literal[
        'csv',
        'parquet',
        'json',
        'xml',
        'txt'
    ],
    **kwargs
) -> pl.DataFrame:
    match file_type:
        case 'csv':
            return pl.read_csv(path, **kwargs)
        case 'parquet':
            return pl.read_parquet(path, **kwargs)
        case 'json':
            f = pl.read_ndjson if kwargs.pop('lines', None) else pl.read_json
            return f(path, **kwargs)
        case 'xml':
            # Polars does not provide a `read_xml`
            with open(path, 'r') as f:
                return pl.DataFrame((
                    # Problem: subchild.text will always be string, no infer
                    { subchild.tag: subchild.text for subchild in child }
                    for child in etree.fromstring(f.read())
                ))
        case 'txt':
            with open(path, 'r') as f:
                return pl.DataFrame(
                    (line.strip() for line in f),
                    schema={'text': pl.String},
                )
        case _:
            raise ValueError(f'Unexpected file type: `{file_type}`.')

def output(
    df: pl.DataFrame,
    output_path: str,
    file_type: Literal[
        'csv',
        'json',
        'xml',
    ]
):
    match file_type:
        case 'csv':
            with open(output_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in df.iter_rows():
                    writer.writerow(row)
        case 'json':
            with open(output_path, 'w') as jsonfile:
                json.dump(df.to_numpy().tolist(), jsonfile, indent=2)
        case 'xml':
            root = etree.Element('root')
            for row in df.iter_rows():
                result_element = etree.SubElement(root, 'row')
                for col, value in zip(df.columns, row):
                    etree.SubElement(result_element, col).text = str(value)
            tree = etree.ElementTree(root)
            tree.write(output_path)
        case _:
            raise ValueError(f'Unexpected file type: `{file_type}`.')

def combinations(val: str, n: int):
    try:
        return tuple(
            json.dumps(c)
            for c in itertools.combinations(json.loads(val), n)
        )
    except:
        return ()
    
def kmeans_iterative(
    df: pl.DataFrame,
    group_by_column: str,
    kmeans_column: str,
    ids_column: str,
    num_clusters: int,
):
    def iter_kmeans_per_type(
        df: pl.DataFrame,
        group_by_column: str,
        kmeans_column: str,
        ids_column: str,
        num_clusters: int,
        max_iterations=10,
        tolerance=1e-4
    ):
        types = df[group_by_column].unique()

        for type_ in types:
            type_df = df.lazy().filter(
                pl.col(group_by_column) == type_
            ).drop_nulls(
                subset=[kmeans_column]
            ).collect()
            data_subset = type_df[kmeans_column].to_numpy().reshape((-1, 1))
            ids_subset = type_df[ids_column].to_numpy()

            kmeans = KMeans(n_clusters=num_clusters, max_iter=max_iterations, tol=tolerance)
            prev_centroids = None
            iteration = 0
            while True:
                kmeans.fit(data_subset)
                centroids = kmeans.cluster_centers_
                if prev_centroids is not None and np.allclose(prev_centroids, centroids, atol=tolerance):
                    break
                prev_centroids = centroids.copy()
                iteration += 1
                if iteration >= max_iterations:
                    break

            cluster_labels = kmeans.labels_

            for cluster_id, id, data_point in zip(cluster_labels, ids_subset, data_subset.flatten()):
                yield (cluster_id, id, type_, float(data_point))
    
    return pl.DataFrame(
        tuple(row for row in iter_kmeans_per_type(
            df,
            group_by_column=group_by_column,
            kmeans_column=kmeans_column,
            ids_column=ids_column,
            num_clusters=num_clusters,
            max_iterations=10,
            tolerance=1e-3
        )),
        schema={
            'cluster_id': pl.String,
            'ids': pl.String,
            'result_type': pl.String,
            'points': pl.Float64
        },
        orient="row",
    )

def kmeans_recursive(
    df: pl.DataFrame,
    group_by_column: str,
    kmeans_column: str,
    ids_column: str,
    num_clusters: int,
):    
    def recursive_kmeans(
        data: np.ndarray,
        num_clusters: int,
        max_iterations: int,
        tolerance: float,
        prev_centroids: np.ndarray=None,
        max_recursive_calls=10
    ):
        kmeans = KMeans(n_clusters=num_clusters, max_iter=max_iterations, tol=tolerance)
        kmeans.fit(data)
        centroids = kmeans.cluster_centers_

        if prev_centroids is not None and np.allclose(prev_centroids, centroids, atol=tolerance):
            return kmeans.labels_

        if max_recursive_calls > 0:
            return recursive_kmeans(data, num_clusters, max_iterations, tolerance, centroids, max_recursive_calls - 1)
        else:
            return kmeans.labels_
        
    def recursive_kmeans_per_type(
        df: pl.DataFrame,
        group_by_column: str,
        kmeans_column: str,
        ids_column: str,
        num_clusters: int,
        max_iterations=30,
        tolerance=1e-3
    ):
        types = df[group_by_column].unique()
        for type_ in types:
            type_df = df.filter(
                pl.col(group_by_column) == type_
            ).drop_nulls(subset=[kmeans_column])
            data_subset = type_df[kmeans_column].to_numpy().reshape((-1, 1))
            ids_subset = type_df[ids_column].to_numpy()

            cluster_labels = recursive_kmeans(data_subset, num_clusters, max_iterations, tolerance, None, 10)
            for cluster_id, id, data_point in zip(cluster_labels, ids_subset, data_subset.flatten()):
                yield (cluster_id, id, type_, float(data_point))    
    
    return pl.DataFrame(
        tuple(row for row in recursive_kmeans_per_type(
            df,
            group_by_column=group_by_column,
            kmeans_column=kmeans_column,
            ids_column=ids_column,
            num_clusters=num_clusters,
            max_iterations=30,
            tolerance=1e-3
        )),
        schema={
            'cluster_id': pl.String,
            'ids': pl.String,
            'result_type': pl.String,
            'points': pl.Float64
        },
        orient="row",
    )

def jsonparse(df: pl.DataFrame, *properties: str):
    def map_row(row):
        rec = json.loads(row[0])
        if isinstance(rec, list):
            return pl.DataFrame(
                { p: item.get(p) for p in properties } for item in rec
            )
        elif isinstance(rec, dict):
            return pl.DataFrame({ p: (rec.get(p),) for p in properties })
        else:
            return pl.DataFrame()
    return pl.concat((
        map_row(row) for row in df.iter_rows()
    ))

def xmlparser(
    df: pl.DataFrame,
    root_name: str,
    column_name,
):
    try:
        return pl.DataFrame(
            (
                json.dumps({ item.tag: item.text for item in elem })
                for elem in etree.fromstring(
                    '\n'.join((str(row) for row in df[column_name]))
                ).iter(root_name)
            ),
            schema={column_name: pl.String},
        )
    except:
        return pl.DataFrame()
    
def extractkeys(
    jval: str,
    key1: str,
    key2: str,
):
    try:
        data = json.loads(jval)
        if isinstance(data, list):
            return np.array(
                ((i.get(key1), i.get(key2)) for i in data), dtype=object
            )
        elif isinstance(data, dict):
            # Extract values dynamically for all keys in the dictionary
            return np.array((data.get(key1),data.get(key2)), dtype=object)
        else:
            return np.array((), dtype=object)

    except Exception:
        return np.array((), dtype=object)

def aggregate_top(
    group_df: pl.DataFrame,
    top_n: int,
    value_col: str
):
    return group_df.top_k(top_n, by=value_col)

def strsplitv(val: str):
    try:
        return val.split()
    except:
        return ['']

def jgroupordered(
    df: pl.LazyFrame,
    order_by_col: str,
    count_col: str,
):
    return df.join(
        df.group_by(order_by_col).agg(
            pl.col(count_col).count().alias("jscount")
        ),
        on=order_by_col,
    )

def pivot(
    df: pl.DataFrame,
    group_by_column: str,
    pivot_column: str,
    aggregate_function: str
):
    return (
        df.pivot(
            values=None,
            index=group_by_column,
            columns=pivot_column,
            aggregate_function=aggregate_function
        )
        if aggregate_function != 'count' else
        df.with_columns(
            # Polars needs a non-null column in `values`
            # to row count each (group_by_column, pivot_column) pair,
            # so fill a dummy column with non-nulls
            pl.lit(0).alias("_dummy")
        ).pivot(
            values="_dummy",
            index=group_by_column,
            columns=pivot_column,
            aggregate_function=aggregate_function
        )
    ).fill_null(0)
