
import duckdb
import os
import pandas as pd
import numpy as np

# U37.	Kmeans: Recursive  version of the above 


def kmeans_recursive(self,subquery:str,k:int,group_col:str,kmeans_col:str,ids_column:str):

    from sklearn.cluster import KMeans
    import pandas as pd
    import numpy as np
    import duckdb

    def recursive_kmeans_per_type(df,group_by_column,kmeans_column, ids_column,num_clusters, max_iterations=30, tolerance=1e-3):
        types = df[group_by_column].unique()

        for type_ in types:
            type_df = df[df[group_by_column] == type_]
            type_df = type_df.dropna(subset=[kmeans_column])
            data_subset = type_df[kmeans_column].values.reshape(-1, 1)
            ids_subset = type_df[ids_column].values

            if len(data_subset) == 0:
                continue 

            cluster_labels = recursive_kmeans(data_subset, num_clusters, max_iterations, tolerance, None, 10)
            for cluster_id, id, data_point in zip(cluster_labels, ids_subset, data_subset.flatten()):
                yield ({'cluster_id':int(cluster_id), ids_column:id, group_by_column:type_, kmeans_column:float(data_point)})


    def recursive_kmeans(data, num_clusters, max_iterations, tolerance, prev_centroids=None, max_recursive_calls=30):

        kmeans = KMeans(n_clusters=num_clusters, max_iter=max_iterations, tol=tolerance)
        kmeans.fit(data)
        centroids = kmeans.cluster_centers_

        if prev_centroids is not None and np.allclose(prev_centroids, centroids, atol=tolerance):
            return kmeans.labels_

        if max_recursive_calls > 0:
            return recursive_kmeans(data, num_clusters, max_iterations, tolerance, centroids, max_recursive_calls - 1)
        else:
            return kmeans.labels_


    try:
        cur  = self.con

        df = cur.sql(f"{str(subquery[0])};").fetchdf()
        group_by_col=str(group_col[0])
        kmeans_col=str(kmeans_col[0])
        id_col = str(ids_column[0])
        clusters_num = k[0].as_py()
        res =  [row for row in recursive_kmeans_per_type(df,group_by_col,kmeans_col,id_col,int(clusters_num))]
        return [res]
    except:
        return [None]