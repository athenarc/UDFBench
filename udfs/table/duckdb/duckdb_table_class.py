import duckdb
import os
import pandas as pd
import numpy as np

class Table:
    def __init__(self,conn,external_path=None):
        self.con = conn.cursor()
        self.external_path = external_path

    # U30.	Extractfromdate: Reads a date (as a string) and returns 3 column values (year, month, day)

    def extractfromdate(self,arg:str):
        try:
            return (int(arg[:arg.find('-')]),
                        int(arg[arg.find('-')+1:arg.rfind('-')]),
                        int(arg[arg.rfind('-')+1:])) 
        except:
            return (-1,-1,-1)



    # U30.	Extractfromdate(v2): Reads a date (as a string) and returns 3 column values (year, month, day)


    def extractfromdate_v2(self,arg:str):

        def extractdate(arg):
            try:
                return {"year":int(arg[:arg.find('-')]),
                        "month":int(arg[arg.find('-')+1:arg.rfind('-')]),
                        "day":int(arg[arg.rfind('-')+1:])
                }
            except:
                return {"year":-1,
                        "month":-1,
                        "day":-1
                }

        return [(extractdate(str(x))) if x.is_valid else ({"year":None,"month":None,"day":None}) for x in arg]




    #  U31.	Jsonparse: Parses a json dict per time and returns a tuple with the values


    def jsonparse(self,json_content: str,key1: str,key2: str):
        import json
        try:
            data = json.loads(json_content)
            if isinstance(data, list):
                for item in data:
                    return (item.get(key1),item.get(key2))
            elif isinstance(data, dict):
                    return (data.get(key1),data.get(key2))
            else:
                return (None,None)
        except:
            return (None,None)


    def jsonparse_v2(self,json_content: str,key1: str,key2: str):
        import json

        def jsonparse(json_content,key1,key2):
            try:
                data = json.loads(json_content)
                if isinstance(data, list):
                    for item in data:
                        return ({'publicationdoi':item.get(key1), 'fundinginfo':item.get(key2)})
                elif isinstance(data, dict):
                        return ({'publicationdoi':data.get(key1),'fundinginfo':data.get(key2)})
                else:
                    return ({'publicationdoi':None, 'fundinginfo':None})
            except:
                return ({'publicationdoi':None, 'fundinginfo':None})
        
        return [(jsonparse(str(val),str(k1),str(k2))) if val.is_valid else ({"publicationdoi":None,"fundinginfo":None}) for val,k1,k2 in zip(json_content,key1,key2)]


    # U32.	Combinations: Reads a json list and returns a table with all the combinations per an integer parameter

    def combinations(self,jval:str,N:int):
        import json
        import itertools

        from itertools import combinations

        def jcombinations(jval,N):
            if jval:
                try:
                    name_list = json.loads(jval)
                    for name_per in itertools.combinations(name_list, N):
                        yield json.dumps([name_per_i for name_per_i in name_per])
                except:
                    yield('[]') 
            else:
                yield None 
        rows = []
        for row in jcombinations(str(jval),int(N)):
            rows.append(row)
        return rows


    # U32.	Combinations(v2): Reads a json list and returns a table with all the combinations per an integer parameter

    # @profile
    def combinations_v2(self,jval:str,N:int):
        import json
        import itertools
        from itertools import combinations
        def jcombinations(jval,N=2):
            if jval:
                try:
                    name_list = json.loads(str(jval))
                    for name_per in itertools.combinations(name_list, int(N)):
                        yield json.dumps([name_per_i for name_per_i in name_per])
                except:
                    yield('[]') 
            else:
                yield None 
                
        return [[y for y in  jcombinations(str(arg1),arg2.as_py())] if arg1.is_valid else [None] for arg1,arg2 in zip(jval,N) ]

    


    def combinations_fused(self,fundingstring:str,jval:str,N:int):
        import json
        import itertools
        from itertools import combinations
        def jcombinations(jval,N=2):
            if jval:
                try:
                    name_list = json.loads(str(jval))
                    for name_per in itertools.combinations(name_list, int(N)):
                        yield json.dumps([name_per_i for name_per_i in name_per])
                except:
                    yield('[]') 
            else:
                yield None 
        
        def extractfunder(project):
            if project:
                try:
                    if '::' in project:
                        return project.split("::")[0]
                    else:
                        return None
                except:
                    return None
            else:
                return 
                
        def extractclass(project):
            if project:
                try:
                    return project.split("::")[1]
                except:
                    return None
            else:
                return None

                
        def extractid(project):
            if project:
                try:
                    return project.split("::")[2]
                except:
                    return None
            else:
                return None

        def extractfundingstring(project):
            try:
                listproject = project.split("::")
                return  listproject[0], listproject[1], listproject[2]
            except:
                return None,None,None
           
    
        def removeshortwords(name):
            return " ".join([word for word in name.split(' ') if len(word) > 2])
        
        def sortname(name):
            return " ".join(sorted(name.split(' ')))


        def jfusedudfs(jval):
            if jval:
                try:
                    jval = json.loads(jval)
                    jval = [name.lower() for name in jval]
                    jval = [removeshortwords(name) for name in jval]
                    jval = [sortname(name) for name in jval]
                    jval = sorted(jval)

                    return json.dumps(jval)
                except:
                    return "[]"
            else:
                return None

        # reslist = []
        result = []
        for _fundingstring, arg1, arg2 in zip(fundingstring, jval, N):
            (funder, _class, projectid) = extractfundingstring(str(_fundingstring))
            if arg1.is_valid:
                sub_result = []
                for y in jcombinations(jfusedudfs(str(arg1)), arg2.as_py()):
                    sub_result.append({
                        "funder": funder,
                        "fclass": _class,
                        "projectid": projectid,
                        "authorpair": y
                    })
                result.append(sub_result)
            else:
                result.append([{
                    "funder": funder,
                    "fclass": _class,
                    "projectid": projectid,
                    "authorpair": None
                }])
        return result
        # return [[{"funder":extractfunder(str(_fundingstring)),"fclass":extractclass(str(_fundingstring)),"projectid":extractid(str(_fundingstring)),"authorpair":y} for y in  jcombinations(str(arg1),arg2.as_py())] if arg1.is_valid else ({"funder":funder,"fclass":_class,"projectid":projectid,"authorpair":None}) for _fundingstring,arg1,arg2 in zip(fundingstring,jval,N) ]
    def q16b_fused_sub(self,subquery:str):
        import pandas as pd
        import numpy as np
        from collections import defaultdict

        def cleandate(pubdate):
            if pubdate:
                try:
                    if "-" in pubdate:
                        splitnum = pubdate.count('-')
                        pubdate_split = pubdate.split("-")
                        if splitnum ==1:
                            return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                        elif splitnum ==2:
                            return pubdate_split[0] + "/" + pubdate_split[1] + "/" + pubdate_split[2]
                        else:
                            return None
                    elif "/" in pubdate:
                        splitnum = pubdate.count('/')
                        pubdate_split = pubdate.split("/")
                        if splitnum ==1:
                            return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                        elif splitnum ==2:
                            return pubdate_split[0] + "-" + pubdate_split[1] + "-" + pubdate_split[2]
                        else:
                            return None
                    else:
                        return None
                except:
                    return None
            else:
                return None
                
        try:

            cur  = self.con
            df = cur.sql(f"{str(subquery[0])};").fetchdf()
            df['pstartcleaned'] = df['projectstart'].apply(cleandate)
            df['pendcleaned'] = df['projectend'].apply(cleandate)
            df['pubdatecleaned'] = df['pubdate'].apply(cleandate)

            df.drop(['projectstart', 'projectend', 'pubdate'], axis=1, inplace=True)

            df['authors_during'] = ((df['pubdatecleaned'] >= df['pstartcleaned']) & (df['pubdatecleaned'] <= df['pendcleaned'])).astype(int)
            df['authors_before'] = (df['pubdatecleaned'] < df['pstartcleaned']).astype(int)
            df['authors_after'] = (df['pubdatecleaned'] > df['pendcleaned']).astype(int)

            result = (
                df.groupby(['funder', 'fclass', 'projectid'], as_index=False)
                .agg(
                    authors_during=('authors_during', 'sum'),
                    authors_before=('authors_before', 'sum'),
                    authors_after=('authors_after', 'sum')
                )
            )

            return [result.to_dict('records')]
     
        except Exception as e:
            return [(None, None, None, None, None, None)]

    # U32.	Combinations(v2): Reads a json list and returns a table with all the combinations per an integer parameter
    def q16b_fused_dict(self,subquery:str):
        import pandas as pd
        import numpy as np
        from collections import defaultdict

        def cleandate(pubdate):
            if pubdate:
                try:
                    if "-" in pubdate:
                        splitnum = pubdate.count('-')
                        pubdate_split = pubdate.split("-")
                        if splitnum ==1:
                            return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                        elif splitnum ==2:
                            return pubdate_split[0] + "/" + pubdate_split[1] + "/" + pubdate_split[2]
                        else:
                            return None
                    elif "/" in pubdate:
                        splitnum = pubdate.count('/')
                        pubdate_split = pubdate.split("/")
                        if splitnum ==1:
                            return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                        elif splitnum ==2:
                            return pubdate_split[0] + "-" + pubdate_split[1] + "-" + pubdate_split[2]
                        else:
                            return None
                    else:
                        return None
                except:
                    return None
            else:
                return None
                
        try:

            cur  = self.con

            rows = cur.sql(f"{str(subquery[0])};").fetchall()
            results = defaultdict(lambda: {'authors_during': None, 'authors_before': None, 'authors_after': None})


            for row in rows:
                invalid_val = True 
                funder = row[0]
                _class = row[1]
                projectid = row[2]
                
                pstartcleaned = cleandate(row[3])
                pendcleaned = cleandate(row[4])
                pubdatecleaned = cleandate(row[5])
                key = (funder, _class, projectid)

                if key not in results:
                    results[key]['authors_during'] = None
                    results[key]['authors_before'] = None
                    results[key]['authors_after'] = None

                if  pubdatecleaned is None:
                    continue


                if pstartcleaned and pendcleaned:
                    if results[key]['authors_during'] is None:
                        results[key]['authors_during'] = 1 if pstartcleaned <= pubdatecleaned <= pendcleaned else None
                    else:
                        results[key]['authors_during'] += 1 if pstartcleaned <= pubdatecleaned <= pendcleaned else 0

                if pstartcleaned:
                    if results[key]['authors_before'] is None:
                        results[key]['authors_before'] = 1 if pubdatecleaned < pstartcleaned else None
                    else:
                        results[key]['authors_before'] += 1 if pubdatecleaned < pstartcleaned else 0

                if pendcleaned:
                    if results[key]['authors_after'] is None:
                        results[key]['authors_after'] = 1 if pubdatecleaned > pendcleaned else None

                    else:
                        results[key]['authors_after'] += 1 if pubdatecleaned > pendcleaned else 0
    
            res= [
                    [{'funder':funder, 'fclass':_class, 'projectid':projectid, 'authors_during':counts['authors_during'], 'authors_before':counts['authors_before'], 'authors_after':counts['authors_after']} 
                    for (funder, _class, projectid), counts in results.items()
                ]]

            return  res

     
        except Exception as e:
            return [(None, None, None, None, None, None)]


    #  U33.	Extractkeys: Selects keys from xml parsed input 


    def extractkeys(self,jval:str,key1:str,key2:str):
        import json
        try:
            data = json.loads(jval)

            if isinstance(data, list):
                for item in data:
                    return  (item.get(key1),item.get(key2))

            elif isinstance(data, dict):
                return  (data.get(key1),data.get(key2))

            else:
                return  (None,None)
        except:
            return (None,None)

    #  U33.	Extractkeys: Selects keys from xml parsed input 


    def extractkeys_v2(self,jval:str,key1:str,key2:str):
        import json

        def extractkeys(jval,key1,key2):
            try:
                data = json.loads(jval)

                if isinstance(data, list):
                    for item in data:
                        return  ({"key1":item.get(key1),"key2":item.get(key2)})
                elif isinstance(data, dict):
                    return  ({"key1":data.get(key1),"key2":data.get(key2)})
                else:
                    return  ({"key1":None,"key2":None})
            except:
                return ({"key1":None,"key2":None})

        
        return [(extractkeys(str(val),str(k1),str(k2))) if val.is_valid else ({"key1":None,"key2":None}) for val,k1,k2 in zip(jval,key1,key2)]

    #  U34.	Strsplitv: Processes a string at a time and returns its tokens in separate rows 

    def strsplitv(self,val:str):
        if val:
            try:
                return val.split()   
            except:
                return []
        else:
            return None


    #  U34.	Strsplitv: Processes a string at a time and returns its tokens in separate rows 

    def strsplitv_v2(self,val:str):
        def strsplitv_loc(val):
            try:
                return val.split()   
            except:
                return []
        return [{"term":strsplitv_loc(str(x))} if x.is_valid else ({"term":None}) for x in val]
   
    #  U34.	Strsplitv: Processes a string at a time and returns its tokens in separate rows 

    def strsplitv_v3(self,val:str,docid:str):
        def strsplitv_loc(val):
            try:
                return val.split()   
            except:
                return []
        res= [{"docid":y,"term":strsplitv_loc(str(x))} if x.is_valid else ({"docid":y,"term":None}) for x,y in zip(val,docid)]

        return res

    #  U35.	JGROUPORDERED: Processes a subquery which is ordered by an attribute, and runs a group by with an aggregate defined as a (named) parameter

    def JGROUPORDERED(self,subquery:str, order_by_col:str,count_col:str):


        try:
            con_func = self.con
            df = con_func.sql(f"{str(subquery[0])};").fetchdf()

            df['jcount'] = df.groupby([str(order_by_col[0])])[str(count_col[0])].transform('size')
            df.dropna(inplace=True)  
            return [df.to_dict('records')]
        except:
            return [None]

    #  U35.	JGROUPORDERED(v2): Processes a subquery which is ordered by an attribute, and runs a group by with an aggregate defined as a (named) parameter

    def JGROUPORDERED_v2(self,term:str,docid:str,tf:float, order_by_col:str,count_col:str)->int:

        dataset = pd.DataFrame({'term': term, 'docid':docid, 'tf':tf})
        try:
            grouped_data = dataset.groupby([str(order_by_col[0])])
            dataset['jcount'] = grouped_data[str(count_col[0])].transform('size')
            return dataset['jcount']
        except:
            dataset['jcount']= None
            return dataset['jcount']


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

    #  U38.	Xmlparser :  Parses xml input and returns a table 


    def xmlparser(self,subquery:str,root_name:str):

        import xml.etree.ElementTree as ET
        import json
        import pandas as pd

        result_text = ''
        result_text = '\n'.join([str(row) for row in subquery])
        rows =[]
        try:
            root = ET.fromstring(result_text)

            for elem in root.iter(str(root_name[0])):
                record = {}
                for item in elem:
                    record[item.tag] = item.text

                rows.append(json.dumps(record),)
            return [rows]
        except:
            return[None]


    # U39.	Pivot: Converts rows of a specific attribute (optionally grouped by another attribute) into columns, while applying an aggregation within the transformed dataset. It returns one tuple per input group

    def pivot(self,
        subquery:str,
        group_by_column:str,  
        pivot_column:str,      
        aggregate_function:str
    ):

        import pandas as pd
        try:
            cur  = self.con
            df = cur.sql(f"{str(subquery[0])};").fetchdf()
            
            group_by_col=str(group_by_column[0])
            pivot_col=str(pivot_column[0])
            aggr_func = str(aggregate_function[0])
            
            pivoted_df = df.pivot_table(
                index=group_by_col,
                columns=pivot_col,
                aggfunc=aggr_func,
                fill_value=0
            ).reset_index()
            return [pivoted_df.to_dict('records')]
        except:
            return [None]

    # U40.	Top: Processes one group at a time and returns the top N values of an attribute 

    def aggregate_top(self,subquery:str,group_col:str,value_col:str,top_n:int):
        import pandas as pd
        import duckdb
        try:
            cur  = self.con

            df = cur.sql(f"{str(subquery[0])};").fetchdf()
            res = df.groupby(str(group_col[0])).apply(lambda x: x.nlargest(int(top_n[0].as_py()), str(value_col[0]))).reset_index(drop=True)
            res.dropna(inplace=True)  
            return [res.to_dict('records')]
        except:
            return [None]




    # U41.	File: parses an external file (csv, xml, json) and returns a table 

    def file(self,file_path:str,file_type:str):
        import pandas as pd
        import xml.etree.ElementTree as ET
        import numpy as np
        import json
        import os
 
        def parse_csv(file_path):
            return pd.read_csv(file_path,header=None)

        def parse_xml(file_path):
            tree = ET.parse(file_path)
            root = tree.getroot()

            data = []
            columns = []

            for elem in root:
                if not columns:
                    columns = [child.tag for child in elem]

                row_data = [elem.find(column).text if elem.find(column) is not None else None for column in columns]
                data.append(row_data)

            return pd.DataFrame(data, columns=columns).fillna('')

        def parse_json(file_path):
            rows=[]
            with open(file_path, 'r') as file:
                first_character = file.read(1)
                file.seek(0)
                if first_character == '[':
                    data = json.load(file)
                    if isinstance(data, list):
                        for item in data:
                            rows.append(item)
                    elif isinstance(data, dict):
                        rows.append(data)

                else:
                    for line in file:
                        data = json.loads(line)
                        rows.append(data)

            return pd.DataFrame(rows)

        def parse_text(file_path):
            with open(file_path, 'r') as f:
                lines = f.read().splitlines()
                return pd.DataFrame(lines,columns=['line'])

        def parse_file_TYPE(file_path, file_type):
            if file_type == 'csv':
                res= parse_csv(file_path)
                if 0 in res.columns:
                    res.columns = [f"column{i}" for i in range(res.shape[1])]
                return res
            elif file_type == 'xml':
                return parse_xml(file_path)
            elif file_type == 'json':
                return parse_json(file_path)
            elif file_type == 'text':
                return parse_text(file_path)
            else:
                raise ValueError("Unsupported file type")

        def file_parser_udf(file_path, file_type):
            table = parse_file_TYPE(file_path, file_type)
            # table = table.astype(str)
            table = table.where(pd.notnull(table), None)

            return table

        res = file_parser_udf(str(self.external_path)+'/'+str(file_path[0]), str(file_type[0]))  
        # records = [{col: row[col] for col in ['doi', 'amount', 'totalpubs','sdate']} for index, row in res.iterrows()]
        return [res.to_dict('records')]



    #  U42.	Output: Exports the results of a subquery to local storage in various formats and returns a True in success 


    def output(self,
        subquery:str,
        output_path:str,
        output_format:str
    )->bool:

        import csv
        import json
        import xml.etree.ElementTree as ET
        import pandas as pd
        import duckdb
        def export_to_csv(result, output_path):
            with open(output_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(result.keys())
                
                # Write data
                for row in zip(*result.values()):
                    writer.writerow(row)
            return True

        def export_to_json(result, output_path):
            with open(output_path, 'w') as jsonfile:
                json.dump(list(result), jsonfile, indent=2)
            return True

        def export_to_xml(result, output_path):
            root = ET.Element('root')
            for row in list(result):
                result_element = ET.SubElement(root, 'publications')
                for key, value in row.items():
                    ET.SubElement(result_element, key).text = str(value)

            tree = ET.ElementTree(root)
            tree.write(output_path)
            return True



        try:
            cur  = self.con

            result = cur.sql(f"{str(subquery[0])} ;").fetchnumpy()

            out_format= str(output_format[0])
            out_path = str(self.external_path)+'/'+str(output_path[0])
            if out_format.lower() == 'csv':
                return [export_to_csv(result, out_path)]
            elif out_format.lower() == 'json':
                return [export_to_json(result, out_path)]
            elif out_format.lower() == 'xml':
                return [export_to_xml(result, out_path)]
            else:
                return [False]
        
        except:
            return [False]

    # U43.	Getstats: gets a whole table with integer values as input and returns the avg and the median for each input column.

    def getstats(self,subquery:str):

        import numpy as np
        import pyarrow as pa
        import  duckdb

        cur  = self.con

        table = cur.sql(str(subquery[0])).fetchdf()
        avg_val =  np.NaN if table['authors'].isnull().all()  else np.nanmean(table.authors)
        median_val = np.NaN if table['authors'].isnull().all() else np.nanmedian(table.authors)
        return ({'avg':avg_val,'median':median_val},)

