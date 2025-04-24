
-- U37.	Kmeans: Recursive  version of the above 

CREATE OR REPLACE FUNCTION kmeans_recursive(
    subquery text,  
    group_by_column text,  
    kmeans_column text,     
    ids_column text,    
    num_clusters int
)RETURNS SETOF RECORD
AS $$
    import pandas as pd
    import plpy
    import numpy as np
    from sklearn.cluster import KMeans

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


    try:
        rows = plpy.execute(subquery)
        data = list(rows)
        df = pd.DataFrame(data)


        for row in recursive_kmeans_per_type(df,group_by_column,kmeans_column, ids_column,num_clusters, 30, 1e-3):
            yield row

    except:
        return None
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;