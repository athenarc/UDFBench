
-- U36.	Kmeans (iterative) : Clusters input data using kmeans, returns cluster id and data point


CREATE OR REPLACE FUNCTION kmeans_iterative(ids string,  types string, amounts double,k int)
RETURNS TABLE ( cluster_id string, ids string, result_type string, points double)
LANGUAGE PYTHON
{
    from sklearn.cluster import KMeans
    import pandas as pd
    def iter_kmeans_per_type(df,group_by_column, kmeans_column, ids_column,num_clusters, max_iterations=10, tolerance=1e-4):
        cluster_results_per_type = {}
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
                if prev_centroids is not None and numpy.allclose(prev_centroids, centroids, atol=tolerance):
                    break
                prev_centroids = centroids.copy()
                iteration += 1
                if iteration >= max_iterations:
                    break

            cluster_labels = kmeans.labels_

            for cluster_id, id, data_point in zip(cluster_labels, ids_subset, data_subset.flatten()):
                yield (cluster_id, id, type_, float(data_point))



    try:
        if type(ids)==numpy.ndarray or type(ids)==numpy.ma.core.MaskedArray:

            df = pd.DataFrame({'id': ids, 'type': types, 'amount': amounts})
            

            return pd.DataFrame([row for row in iter_kmeans_per_type(df,"type","amount", "id",int(k[0]), 10, 1e-3)],columns=['cluster_id','ids','result_type', 'points']).to_dict('list')

        else:
            return pd.DataFrame({'cluster_id': [],'id': [], 'result_type':[], 'points':[]}, columns=['cluster_id','ids','result_type', 'points'])

    except:
        return pd.DataFrame({'cluster_id': [],'id': [], 'result_type':[], 'points':[]}, columns=['cluster_id','ids','result_type', 'points'])

};
