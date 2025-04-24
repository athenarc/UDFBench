from . import setpath
from . import vtbase
import functions
import csv
import os
import json
import xml.etree.ElementTree as ET
import pandas as pd
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
### Classic stream iterator
registered=True

class kmeans_recursive(vtbase.VT):
  def VTiter(self, *parsedArgs, **envars):
    largs, dictargs = self.full_parse(parsedArgs)
    self.nonames=True
    self.names=[]
    self.types=[]
    group_by_column = largs[0]
    kmeans_column = largs[1]
    ids_column = largs[2]
    num_clusters = int(largs[3])
    if 'query' not in dictargs:
            raise functions.OperatorError(__name__.rsplit('.')[-1],"No query argument ")
    query=dictargs['query']
    cur = envars['db'].cursor()


    def recursive_kmeans_per_type(df,group_by_column,kmeans_column, ids_column,num_clusters, max_iterations=30, tolerance=1e-3):
        types = df[group_by_column].unique()

        for type_ in types:
            type_df = df[df[group_by_column] == type_]
            type_df = type_df.dropna(subset=[kmeans_column])

            data_subset = type_df[kmeans_column].values.reshape(-1, 1)
            ids_subset = type_df[ids_column].values

            cluster_labels = recursive_kmeans(data_subset, num_clusters, max_iterations, tolerance, None, 10)
            for cluster_id, id, data_point in zip(cluster_labels, ids_subset, data_subset.flatten()):
                yield (str(cluster_id), id, type_, float(data_point))


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
        data = list(cur.execute(query))
        sch = list(cur.getdescriptionsafe())
        names = [x[0] for x in sch]
        df = pd.DataFrame(data)
        header=0
        for row in recursive_kmeans_per_type(df,names.index(group_by_column),names.index(kmeans_column), names.index(ids_column),num_clusters, 10, 1e-3):
            if header==0:
                yield ('c'+str(d) for x,d in enumerate(row))
                header=1
            yield row

    except :
        raise
        return None


def Source():
    return vtbase.VTGenerator(kmeans_recursive)

