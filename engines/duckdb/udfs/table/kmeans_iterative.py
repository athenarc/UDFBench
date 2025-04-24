

import duckdb
import os
import pandas as pd
import numpy as np


#  U36.	Kmeans (iterative) : Clusters input data using kmeans, returns cluster id and data point


def kmeans_iterative(self,subquery:str,k:int,group_col:str,kmeans_col:str,ids_column:str)->tuple:
    from sklearn.cluster import KMeans
    import pandas as pd
    import numpy as np
    import duckdb
    import time
    def iter_kmeans_per_type(df,group_by_column, kmeans_column, ids_column,num_clusters, max_iterations=10, tolerance=1e-3):
        types = df[group_by_column].unique()
        for type_ in types:
            type_df = df[df[group_by_column] == type_]

            type_df = type_df.dropna(subset=[kmeans_column])
            data_subset = type_df[kmeans_column].values.reshape(-1, 1)
            ids_subset = type_df[ids_column].values
            if len(data_subset) == 0:
                pass 

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
                yield ({'cluster_id':int(cluster_id), ids_column:id, group_by_column:type_, kmeans_column:float(data_point)})
        

    try:

        cur  = self.con
        df = cur.sql(f"{str(subquery[0])};").fetchdf()
    
        group_by_col=str(group_col[0])
        kmeans_col=str(kmeans_col[0])
        id_col = str(ids_column[0])
        clusters_num = k[0].as_py()
        res =  [row for row in iter_kmeans_per_type(df,group_by_col,kmeans_col,id_col,int(clusters_num))]

        return [res]
    except:
        return [None]


