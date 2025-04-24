
-- U36.	Kmeans (iterative) : Clusters input data using kmeans, returns cluster id and data point

CREATE OR REPLACE FUNCTION kmeans_iterative(
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


    def iter_kmeans_per_type(df,group_by_column, kmeans_column, ids_column,num_clusters, max_iterations=10, tolerance=1e-4):

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


    try:
        rows = plpy.execute(subquery)
        data = list(rows)
        df = pd.DataFrame(data)


        for row in iter_kmeans_per_type(df,group_by_column,kmeans_column, ids_column,num_clusters, 10, 1e-3):
            yield row

    except:
        return None
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;
