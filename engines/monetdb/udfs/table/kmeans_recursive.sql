-- U37.	Kmeans: Recursive  version of the above 

CREATE OR REPLACE FUNCTION kmeans_recursive(ids string,  types string, amounts double,k int)
RETURNS TABLE ( cluster_id string, ids string, result_type string, points double)
LANGUAGE PYTHON
{
    from sklearn.cluster import KMeans
    import pandas as pd
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

        if prev_centroids is not None and numpy.allclose(prev_centroids, centroids, atol=tolerance):
            return kmeans.labels_

        if max_recursive_calls > 0:
            return recursive_kmeans(data, num_clusters, max_iterations, tolerance, centroids, max_recursive_calls - 1)
        else:
            return kmeans.labels_

    try:
        if type(ids)==numpy.ndarray or type(ids)==numpy.ma.core.MaskedArray:

            df = pd.DataFrame({'id': ids, 'type': types, 'amount': amounts})
            

            return pd.DataFrame([row for row in recursive_kmeans_per_type(df,"type","amount", "id",int(k[0]), 30, 1e-3)],columns=['cluster_id','ids','result_type', 'points']).to_dict('list')

        else:
            return pd.DataFrame({'cluster_id': [],'id': [], 'result_type':[], 'points':[]}, columns=['cluster_id','id','result_type', 'points'])

    except:
        return pd.DataFrame({'cluster_id': [],'id': [], 'result_type':[], 'points':[]}, columns=['cluster_id','id','result_type', 'points'])

};