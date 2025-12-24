import json
import itertools
import numpy as np
from typing import Literal
from lxml import etree
from sklearn.cluster import KMeans
import csv

def combinations(val: str, n: int):
    try:
        return np.fromiter(
            (json.dumps(c) for c in itertools.combinations(json.loads(val), n)),
            dtype=object
        )
    except:
        return np.array(())

def extractfromdate(arg: str):
    try:
        return np.array((
            int(arg[:arg.find('-')]),
            int(arg[arg.find('-')+1:arg.rfind('-')]),
            int(arg[arg.rfind('-')+1:])
        ))
    except:
        return np.array((-1, -1, -1))

def extractfromdate_nonumpy(arg: str):
    try:
        return (
            int(arg[:arg.find('-')]),
            int(arg[arg.find('-')+1:arg.rfind('-')]),
            int(arg[arg.rfind('-')+1:])
        )
    except:
        return (-1, -1, -1)

def get_stats(artifacts_authors, df_factory):
    avg_val = (
        np.NaN if artifacts_authors.isnull().all().item()
        else np.nanmean(artifacts_authors)
    )
    median_val = (
        np.NaN if artifacts_authors.isnull().all().item()
        else np.nanmedian(artifacts_authors)
    )
    return df_factory([{
        'avg': avg_val,
        'median': median_val,
    }])

def jsonparse(df, pd_module, *properties: str):
    pd = pd_module
    def map_row(row):
        rec = json.loads(row[0])
        if isinstance(rec, list):
            return pd.DataFrame(
                { p: item.get(p) for p in properties } for item in rec
            )
        elif isinstance(rec, dict):
            return pd.DataFrame({ p: (rec.get(p),) for p in properties })
        else:
            return pd.DataFrame()
    res = pd.concat(df.apply(map_row, axis=1).values, ignore_index=True)
    return res

def file(
    path: str,
    file_type: Literal[
        'csv',
        'parquet',
        'json',
        'xml',
        'txt'
    ],
    pd,
    **kwargs
):
    match file_type:
        case 'csv':
            return pd.read_csv(path, **kwargs)
        case 'parquet':
            return pd.read_parquet(path, **kwargs)
        case 'json':
            # Modin `read_json` only supports lines=True
            if kwargs.get('lines'):
                return pd.read_json(path, **kwargs)
            else:
                with open(path, 'r') as f:
                    return pd.DataFrame(json.load(f))
        case 'xml':
            # Modin does not support `read_xml`
            # return pd.read_xml(path, **file_kwargs)
            with open(path, 'r') as f:
                return pd.DataFrame((
                    # Problem: subchild.text will always be string, no infer
                    { subchild.tag: subchild.text for subchild in child }
                    for child in etree.fromstring(f.read())
                ))
        case 'txt':
            with open(path, 'r') as f:
                return pd.DataFrame((row.strip() for row in f))
        case _:
            raise ValueError(f'Unexpected file type: `{file_type}`.')

def kmeans_iterative(
    data_df,
    group_by_column: str,
    kmeans_column: str,
    ids_column: str,
    num_clusters: int,
    pd,
):
    def iter_kmeans_per_type(
        df,
        group_by_column,
        kmeans_column,
        ids_column,
        num_clusters,
        max_iterations=10,
        tolerance=1e-4
    ):
        types = df[group_by_column].unique()

        for type_ in types:
            type_df = df[df[group_by_column] == type_]
            type_df = type_df.dropna(subset=[kmeans_column])
            data_subset = type_df[kmeans_column].values.reshape(-1, 1)
            ids_subset = type_df[ids_column].values

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
    
    return pd.DataFrame(
        tuple(row for row in iter_kmeans_per_type(
            data_df,
            group_by_column=group_by_column,
            kmeans_column=kmeans_column,
            ids_column=ids_column,
            num_clusters=num_clusters,
            max_iterations=10,
            tolerance=1e-3
        )),
        columns=('cluster_id', 'ids','result_type', 'points')
    )

def kmeans_recursive(
    data_df,
    group_by_column: str,
    kmeans_column: str,
    ids_column: str,
    num_clusters: int,
    pd,
):
    def recursive_kmeans_per_type(df,group_by_column,kmeans_column, ids_column,num_clusters, max_iterations=30, tolerance=1e-3):
        types = df[group_by_column].unique()
        for type_ in types:
            type_df = df[df[group_by_column] == type_]
            type_df = type_df.dropna(subset=[kmeans_column])
            data_subset = type_df[kmeans_column].values.reshape(-1, 1)
            ids_subset = type_df[ids_column].values

            cluster_labels = recursive_kmeans(data_subset, num_clusters, max_iterations, tolerance, None, 10)
            for cluster_id, id, data_point in zip(cluster_labels, ids_subset, data_subset.flatten()):
                yield (cluster_id, id, type_, float(data_point))    

    def recursive_kmeans(data, num_clusters, max_iterations, tolerance, prev_centroids=None, max_recursive_calls=10):
        kmeans = KMeans(n_clusters=num_clusters, max_iter=max_iterations, tol=tolerance)
        kmeans.fit(data)
        centroids = kmeans.cluster_centers_

        if prev_centroids is not None and np.allclose(prev_centroids, centroids, atol=tolerance):
            return kmeans.labels_

        if max_recursive_calls > 0:
            return recursive_kmeans(data, num_clusters, max_iterations, tolerance, centroids, max_recursive_calls - 1)
        else:
            return kmeans.labels_
    
    return pd.DataFrame(
        tuple(row for row in recursive_kmeans_per_type(
            data_df,
            group_by_column=group_by_column,
            kmeans_column=kmeans_column,
            ids_column=ids_column,
            num_clusters=num_clusters,
            max_iterations=30,
            tolerance=1e-3
        )),
        columns=('cluster_id', 'ids','result_type', 'points')
    )

def pivot(
    df,
    group_by_column: str,
    pivot_column: str,
    aggregate_function: str
):
    import pandas as pd

    res = None
    if isinstance(df, pd.DataFrame):
        res = df.pivot_table(
        index=group_by_column,
        columns=pivot_column,
        aggfunc=aggregate_function,
        fill_value=0
    ).reset_index()
    else:

        res = (
            df.groupby([group_by_column, pivot_column])
            .agg(aggregate_function)
            .unstack(fill_value=0)
            .reset_index()
        )
    #     res = df._to_pandas().pivot_table(
    #     index=group_by_column,
    #     columns=pivot_column,
    #     aggfunc=aggregate_function,
    #     fill_value=0
    # ).reset_index()

    return res

def xmlparser(data_df, root_name: str, column_name, pd):
    try:
        return pd.DataFrame((
            json.dumps({ item.tag: item.text for item in elem })
            for elem in etree.fromstring(
                '\n'.join((str(row) for row in data_df[column_name]))
            ).iter(root_name)
        ))
    except:
        return pd.DataFrame()

def extractkeys(jval, key1, key2):
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

def extractkeys_nonumpy(jval, key1, key2):
    try:
        data = json.loads(jval)
        if isinstance(data, list):
            return tuple((i.get(key1), i.get(key2)) for i in data)
        elif isinstance(data, dict):
            # Extract values dynamically for all keys in the dictionary
            return (data.get(key1), data.get(key2))
        else:
            return ()
    except Exception:
        return ()

def aggregate_top(group_df, top_n: int, value_col):
    return group_df.nlargest(top_n, value_col)

def strsplitv(val: str):
    try:
        return val.split()
    except:
        return ['']

def jgroupordered(data_df, order_by_col, count_col):
    res = data_df.copy()
    res['jscount'] = data_df.groupby(by=order_by_col)[count_col].transform('size')
    return res

def output(
    data_df,
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
                for row in data_df.values:
                    writer.writerow(row)
        case 'json':
            with open(output_path, 'w') as jsonfile:
                json.dump(data_df.values.tolist(), jsonfile, indent=2)
        case 'xml':
            root = etree.Element('root')
            for row in data_df.values:
                result_element = etree.SubElement(root, 'row')
                for col, value in zip(data_df.columns, row):
                    etree.SubElement(result_element, col).text = str(value)
            tree = etree.ElementTree(root)
            tree.write(output_path)
        case _:
            raise ValueError(f'Unexpected file type: `{file_type}`.')
