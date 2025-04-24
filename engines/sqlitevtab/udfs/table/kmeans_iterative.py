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

class kmeans_iterative(vtbase.VT):
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
                yield (str(cluster_id), id, type_, float(data_point))


    try:
        data = list(cur.execute(query))
        sch = list(cur.getdescriptionsafe())
        names = [x[0] for x in sch]
        df = pd.DataFrame(data)
        header=0
        for row in iter_kmeans_per_type(df,names.index(group_by_column),names.index(kmeans_column), names.index(ids_column),num_clusters, 10, 1e-3):
            if header==0:
                yield ('c'+str(d) for x,d in enumerate(row))
                header=1
            yield row

    except :
        raise
        return None



def Source():
    return vtbase.VTGenerator(kmeans_iterative)


