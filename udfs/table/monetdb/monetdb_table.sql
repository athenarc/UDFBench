-- U30.	Extractfromdate: Reads a date (as a string) and returns 3 column values (year, month, day)

CREATE or replace FUNCTION extractfromdate(id string, input string)
RETURNS TABLE(id string, extractyear INTEGER, extractmonth INTEGER, extractdate INTEGER)
LANGUAGE PYTHON
{

    def extractfromdate(arg):
        try:
            return int(arg[:arg.find('-')]), \
                    int(arg[arg.find('-')+1:arg.rfind('-')]), \
                    int(arg[arg.rfind('-')+1:])
            
        except:
            return -1,-1,-1
            

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        result = dict()
        result['id'] = id
        extract_vals = [extractfromdate(x) if x else (numpy.nan,numpy.nan,numpy.nan) for x in input]
        result['extractyear'], result['extractmonth'], result['extractdate'] = map(list, zip(*extract_vals))
        return result
    else:
        result = dict()
        result['id'] = [id]
        extract_vals = [extractfromdate(input) if input else (numpy.nan,numpy.nan,numpy.nan)]
        result['extractyear'], result['extractmonth'], result['extractdate'] = map(list, zip(*extract_vals))
        return result


};


-- U31.	Jsonparse: Parses a json dict per time and returns a tuple with the values


CREATE OR REPLACE FUNCTION jsonparse(subquery STRING,key1  STRING, key2 STRING) 
RETURNS TABLE (publicationdoi STRING, fundinginfo STRING)
LANGUAGE PYTHON {


    import json
    import pandas as pd
    try:
        rows =[]
        for line in subquery:
            data = json.loads(line)
            if isinstance(data, list):
                for item in data:
                    rows.append((item.get(key1[0]),item.get(key2[0])))
            elif isinstance(data, dict):
                rows.append((data.get(key1[0]),data.get(key2[0])) )
            else:
                rows.append( None,None)
        return pd.DataFrame(rows)

    except:
        return pd.DataFrame({'publicationdoi':[],'fundinginfo':[]})
   
};

-- U32.	Combinations: Reads a json list and returns a table with all the combinations per an integer parameter
CREATE or replace FUNCTION combinations(input1 string, input2 integer)
RETURNS TABLE  (authorpair string)
LANGUAGE PYTHON
{

    import json
    import itertools
    def jcombinations(jval,N):
        try:
            name_list = json.loads(jval)
            for name_per in itertools.combinations(name_list, N):
                yield json.dumps([name_per_i for name_per_i in name_per])

        except:
            yield('[]')  
    try:
        if type(input1)==numpy.ndarray or type(input1)==numpy.ma.core.MaskedArray:
            res = numpy.array([y for arg1,arg2 in zip(input1,input2) for y in jcombinations(arg1,arg2)], dtype=object)
            if not res.any():
                return ['[]']
            else:
                return res

        else:
            res =  numpy.array([y for y in jcombinations(input1,input2)], dtype=object)
            if not res.any():
                return ['[]']
            else:
                return res

    except:
        return ['[]']

};

-- U32.	Combinations(for q16): Reads a json list and returns a table with all the combinations per an integer parameter



CREATE or replace FUNCTION combinations(pubid string, pubdate string, projectstart string, projectend string, funder string, fclass string, projectid string, input1 string, input2 integer)
RETURNS TABLE  (pubid string, pubdate string, projectstart string, projectend string, funder string, fclass string, projectid string,authorpair string)
LANGUAGE PYTHON
{

    import json
    import itertools
    import pandas as pd


    def jcombinations(jval,N):
        try:
            name_list = json.loads(jval)
            for name_per in itertools.combinations(name_list, N):
                yield json.dumps([name_per_i for name_per_i in name_per])

        except:
            yield('[]')  
    try:
        if type(input1)==numpy.ndarray or type(input1)==numpy.ma.core.MaskedArray:
            reslist = {
                'pubid': [],
                'pubdate': [],
                'projectstart': [],
                'projectend': [],
                'funder': [],
                'fclass': [],
                'projectid': [],
                'authorpair': []
            }
            for _pubid, _pubdate, _projectstart, _projectend,_funder,_class,_projectid,arg1,arg2 in zip(pubid, pubdate, projectstart, projectend,funder,fclass,projectid,input1,input2):
                _pubdate = _pubdate if _pubdate and _pubdate!='-' else numpy.nan
                _projectstart = _projectstart if _projectstart and _projectstart!='-' else numpy.nan
                _projectend = _projectend if _projectend!='-' else numpy.nan
                for y in jcombinations(arg1,arg2):
                    reslist['pubid'].append(_pubid)
                    reslist['pubdate'].append(_pubdate)
                    reslist['projectstart'].append(_projectstart)
                    reslist['projectend'].append(_projectend)
                    reslist['funder'].append(_funder)
                    reslist['fclass'].append(_class)
                    reslist['projectid'].append(_projectid)
                    reslist['authorpair'].append(y)

            return pd.DataFrame(reslist)
        else:
            res = pd.DataFrame([[pubid, pubdate, projectstart, projectend,funder,fclass,projectid,y] for y in jcombinations(input1,input2)])
        
        if not res.empty:
            return res
        else:
            return pd.DataFrame({'pubid': [], 'pubdate': [], 'projectstart': [], 'projectend': [], 'funder': [], 'fclass': [], 'projectid': [], 'authorpair': []})

    except:
        return pd.DataFrame({'pubid': [], 'pubdate': [], 'projectstart': [], 'projectend': [], 'funder': [], 'fclass': [], 'projectid': [], 'authorpair': []})

};

-- U32.	Combinations(for q10a and q11a): Reads a json list and returns a table with all the combinations per an integer parameter


CREATE or replace FUNCTION combinations(pubdate STRING, input1 STRING, input2 INTEGER)
RETURNS TABLE  (authorpair STRING, pubdate STRING)
LANGUAGE PYTHON
{

    import json
    import itertools
    import pandas as pd
    def jcombinations(jval,N):
        try:
            name_list = json.loads(jval)
            for name_per in itertools.combinations(name_list, N):
                yield json.dumps([name_per_i for name_per_i in name_per])

        except:
            yield('[]')  
    try:
        if type(input1)==numpy.ndarray or type(input1)==numpy.ma.core.MaskedArray:
            reslist = {
                'authorpair': [],
                'pubdate': []

            }
            for _pubdate, arg1,arg2 in zip(pubdate, input1,input2):
                _pubdate = _pubdate if _pubdate and _pubdate!='-' else numpy.nan
                for y in jcombinations(arg1,arg2):
                    reslist['pubdate'].append(_pubdate)
                    reslist['authorpair'].append(y)

            return pd.DataFrame(reslist)
        else:
            res = pd.DataFrame([[ pubdate,y] for y in jcombinations(input1,input2)])
        
        if not res.empty:
            return res
        else:
            return pd.DataFrame({ 'pubdate': [], 'authorpair': []})

    except:
        return pd.DataFrame({ 'pubdate': [], 'authorpair': []})

};


-- U33.	Extractkeys: Selects keys from xml parsed input 

CREATE OR REPLACE FUNCTION extractkeys(jval STRING,key1 STRING,key2 STRING) 
RETURNS TABLE (
    publicationdoi STRING,
    fundinginfo STRING
) 
LANGUAGE PYTHON {

    import json
    import pandas as pd 

    def extract_keys(jval,key1,key2):
        try:
            data = json.loads(jval)

            if isinstance(data, list):
                for item in data:
                    yield (item.get(key1),item.get(key2))

            elif isinstance(data, dict):
                yield (data.get(key1),data.get(key2))

            else:
                yield (None,None)

        except:
            yield (None,None)
        
    try:

        if type(jval)==numpy.ndarray or type(jval)==numpy.ma.core.MaskedArray:

            res=  pd.DataFrame(((y1,y2) for arg1,arg2,arg3 in zip(jval,key1,key2) for y1,y2 in extract_keys(arg1,arg2,arg3 )))
        else:
            res = pd.DataFrame(((y1,y2)  for y1,y2 in extract_keys(jval,key1,key2)))
        
        if not res.empty:
            return res
        else:
           return pd.DataFrame({'publicationdoi':[],'fundinginfo':[]})


    except:
        return pd.DataFrame({'publicationdoi':[],'fundinginfo':[]})


};

-- U34.	Strsplitv: Processes a string at a time and returns its tokens in separate rows 

CREATE OR REPLACE FUNCTION strsplitv(input STRING)
RETURNS TABLE  (word STRING)
LANGUAGE PYTHON
{
    def strsplitv(val):
        try:
            return val.split()   
        except:
            return []

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        res = numpy.array([y if arg and arg!='-' else numpy.nan for arg in input for y in strsplitv(arg)], dtype=object)
    else:
        res =  numpy.array([y for y in strsplitv(input)], dtype=object)

    if not res.any():
        return ['[]']
    else:
        return res

};



-- U34.	Strsplitv(q17): Processes a string at a time and returns its tokens in separate rows 



CREATE OR REPLACE FUNCTION strsplitv(docid string, abstract string) 
RETURNS TABLE (docid string, term string) 
LANGUAGE PYTHON
{
    import pandas as pd
    def strsplitv(val):
        try:
            return val.split()   
        except:
            return [""]

    if type(docid)==numpy.ndarray or type(docid)==numpy.ma.core.MaskedArray:

        res=  pd.DataFrame([[id,y] for id,arg in zip(docid,abstract)  if arg and arg!='-' for y in strsplitv(arg) ], columns=['docid', 'term'])
    else:
        res = pd.DataFrame([[docid,y] for y in strsplitv(abstract) ], columns=['docid', 'term'])
    
    if not res.empty:
        return res
    else:
        return pd.DataFrame({'docid': [], 'term': []})

};

-- U35.	JGROUPORDERED: Processes a subquery which is ordered by an attribute, and runs a group by with an aggregate defined as a (named) parameter

CREATE OR REPLACE FUNCTION JGROUPORDERED(
    term string,
    docid string,
    tf float, 
    order_by_col string,
    count_col string
)
RETURNS TABLE ( term string,docid string, tf float,jcount bigint)
LANGUAGE PYTHON
{
    import pandas as pd
    try:
        if type(term)==numpy.ndarray or type(term)==numpy.ma.core.MaskedArray:
            dataset = pd.DataFrame({'term': term, 'docid':docid, 'tf':tf}, columns=['term','docid', 'tf'])
            grouped_data = dataset.groupby([order_by_col[0]])
            dataset['jcount'] = grouped_data[count_col[0]].transform('size')
            dataset.dropna(inplace=True)  
            return dataset[['term', 'docid', 'tf', 'jcount']].to_dict('list')
        else:
            return pd.DataFrame({'term': [], 'docid':[], 'tf':[],'jcount':[]}, columns=['term','docid', 'tf','jcount'])
    except:
        return pd.DataFrame({'term': [], 'docid':[], 'tf':[],'jcount':[]}, columns=['term','docid', 'tf','jcount'])


};

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



-- U38.	Xmlparser :  Parses xml input and returns a table 

CREATE OR REPLACE FUNCTION xmlparser(subquery STRING,root_name STRING) 
RETURNS TABLE (record STRING)
LANGUAGE PYTHON {

    import xml.etree.ElementTree as ET
    import json
    import pandas as pd

    result_text = ''
    result_text = '\n'.join([str(row) for row in subquery])
    rows =[]

    try:
        root = ET.fromstring(result_text)

        for elem in root.iter(root_name[0]):
            record = {}
            for item in elem:
                record[item.tag] = item.text

            rows.append(json.dumps(record),)
        
        return pd.DataFrame(rows)

    except:
        return pd.DataFrame({'record':[]})
};



-- U39.	Pivot: Converts rows of a specific attribute (optionally grouped by another attribute) into columns, while applying an aggregation within the transformed dataset. It returns one tuple per input group

CREATE OR REPLACE FUNCTION pivot(
    pid string,
    result_type string,
    group_by_column string,  
    pivot_column string,      
    aggregate_function string -- Aggregation function to apply(size,sum )
)
RETURNS TABLE ( pid string, publication int, dataset int, software int, other int)
LANGUAGE PYTHON
{
    import pandas as pd
    try:

        if type(pid)==numpy.ndarray or type(pid)==numpy.ma.core.MaskedArray:

            dataset = pd.DataFrame({'pid': pid, 'result_type':result_type}, columns=['pid','result_type'])
            pivoted_df = dataset.pivot_table(index=group_by_column[0], columns=pivot_column[0], aggfunc=aggregate_function[0],fill_value=0).reset_index()
            pivoted_df.columns = ['pid','publication', 'dataset','software','other']
            return pivoted_df.to_dict('list')
        else:
            return pd.DataFrame({'pid': [], 'publication':[], 'dataset':[],'software':[],'other':[]})
    except:
        return pd.DataFrame({'pid': [], 'publication':[], 'dataset':[],'software':[],'other':[]})


};



-- U40.	Top: Processes one group at a time and returns the top N values of an attribute 

CREATE OR REPLACE FUNCTION aggregate_top(group_column1 string,group_column2 string, value_column numeric,top_n int)
RETURNS TABLE(group_column1 string,group_column2 string,top_s numeric)
LANGUAGE PYTHON
{
    import pandas as pd

    if type(group_column1)==numpy.ndarray or type(group_column1)==numpy.ma.core.MaskedArray:

        try:
            dataset = pd.DataFrame({'groups': group_column1, 'group2':group_column2,'val':value_column }, columns=['groups','group2', 'val'])
            res = dataset.groupby('groups').apply(lambda x: x.nlargest(top_n[0], 'val')).reset_index(drop=True)
            return res.dropna()  
        except:
            return pd.DataFrame({'group_column1': [], 'group_column2': [],'top_s': []})

    else:
        return pd.DataFrame({'group_column1': [], 'group_column2': [],'top_s': []})
};


CREATE OR REPLACE FUNCTION aggregate_top(group_column1 string,group_column2 string, value_column float,top_n int)
RETURNS TABLE(group_column1 string,group_column2 string,top_s float)
LANGUAGE PYTHON
{
    import pandas as pd

    if type(group_column1)==numpy.ndarray or type(group_column1)==numpy.ma.core.MaskedArray:

        try:
            dataset = pd.DataFrame({'groups': group_column1, 'group2':group_column2,'val':value_column }, columns=['groups','group2', 'val'])
            res = dataset.groupby('groups').apply(lambda x: x.nlargest(top_n[0], 'val')).reset_index(drop=True)
            return res.dropna()  
        except:
            return pd.DataFrame({'group_column1': [], 'group_column2': [],'top_s': []})

    else:
        return pd.DataFrame({'group_column1': [], 'group_column2': [],'top_s': []})
};

-- U41.	File(q6): parses an external file (csv, xml, json) and returns a table 


CREATE or replace  FUNCTION file_q6(file_path2 STRING, file_type2 STRING)
RETURNS TABLE (column1 STRING, column2 STRING,column3 STRING, column4 STRING)
LANGUAGE PYTHON {

    import pandas as pd
    import xml.etree.ElementTree as ET
    import json
    import numpy as np

    def parse_csv(file_path):
        return pd.read_csv(file_path)

    def parse_xml(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        data = []
        columns = [child.tag for child in root[0]] if root else []

        for elem in root:
            row_data = [elem.find(column).text if elem.find(column) is not None else None for column in columns]
            data.append(row_data)

        return pd.DataFrame(data, columns=columns).fillna('')

            
    def parse_json(file_path):
        def iter_json(file_path):
            with open(file_path, 'r') as file:
                first_character = file.read(1)
                file.seek(0)  # Reset the file pointer to the beginning
                if first_character == '[':
                    data = json.load(file)
                    if isinstance(data, list):
                        for item in data:
                            yield tuple(item.values())
                    elif isinstance(data, dict):
                        yield tuple(data.values())
                else:
                    for line in file:
                        data = json.loads(line)
                        if isinstance(data, list):
                            for item in data:
                                yield tuple(item.values())
                        elif isinstance(data, dict):
                            yield tuple(data.values())
  
        rows=[]
        for row in iter_json(file_path):
            rows.append(row)
        return pd.DataFrame(rows).fillna('')

    def parse_file(file_path, file_type):
        if file_type == 'csv':
            return parse_csv(file_path)
        elif file_type == 'xml':
            return parse_xml(file_path)
        elif file_type == 'json':
            return parse_json(file_path)
        else:
            raise ValueError("Unsupported file type")

    def file_parser_udf(file_path, file_type):
        table = parse_file(file_path, file_type)
        
        # Your additional processing or analysis using NumPy can go here
        table = table.astype(str)

        return table

    return file_parser_udf(file_path2, file_type2)
};

-- U41.	File(q7): parses an external file (csv, xml, json) and returns a table 

CREATE or replace  FUNCTION file_q7(file_path2 STRING, file_type2 STRING)
RETURNS TABLE (column1 STRING, column2 STRING,column3 STRING)
LANGUAGE PYTHON {

    import pandas as pd
    import xml.etree.ElementTree as ET
    import json
    import numpy as np

    def parse_csv(file_path):
        return pd.read_csv(file_path)

    def parse_xml(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        data = []
        columns = [child.tag for child in root[0]] if root else []

        for elem in root:
            row_data = [elem.find(column).text if elem.find(column) is not None else None for column in columns]
            data.append(row_data)

        return pd.DataFrame(data, columns=columns)

        
    def parse_json(file_path):
        def iter_json(file_path):
            with open(file_path, 'r') as file:
                first_character = file.read(1)
                file.seek(0)  # Reset the file pointer to the beginning
                if first_character == '[':
                    data = json.load(file)
                    if isinstance(data, list):
                        for item in data:
                            yield tuple(item.values())
                    elif isinstance(data, dict):
                        yield tuple(data.values())
                else:
                    for line in file:
                        data = json.loads(line)
                        if isinstance(data, list):
                            for item in data:
                                yield tuple(item.values())
                        elif isinstance(data, dict):
                            yield tuple(data.values())
  
        rows=[]
        for row in iter_json(file_path):
            rows.append(row)
        return pd.DataFrame(rows).fillna('')

    def parse_file(file_path, file_type):
        if file_type == 'csv':
            return parse_csv(file_path)
        elif file_type == 'xml':
            return parse_xml(file_path)
        elif file_type == 'json':
            return parse_json(file_path)
        else:
            raise ValueError("Unsupported file type")

    def file_parser_udf(file_path, file_type):
        table = parse_file(file_path, file_type)
        
        table = table.astype(str)

        return table

    return file_parser_udf(file_path2, file_type2)
};

-- U41.	File(q13): parses an external file (csv, xml, json) and returns a table 


CREATE or replace  FUNCTION file_q13(file_path2 STRING, file_type2 STRING)
RETURNS TABLE (column1 STRING)
LANGUAGE PYTHON {

    import pandas as pd
    import xml.etree.ElementTree as ET
    import json
    import numpy as np

    def parse_csv(file_path):
        return pd.read_csv(file_path)

    def parse_xml(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        data = []
        columns = [child.tag for child in root[0]] if root else []

        for elem in root:
            row_data = [elem.find(column).text if elem.find(column) is not None else None for column in columns]
            data.append(row_data)

        return pd.DataFrame(data, columns=columns)

            
    def parse_json(file_path):
        def iter_json(file_path):
            with open(file_path, 'r') as file:
                first_character = file.read(1)
                file.seek(0)  # Reset the file pointer to the beginning
                if first_character == '[':
                    data = json.load(file)
                    if isinstance(data, list):
                        for item in data:
                            yield tuple(item.values())
                    elif isinstance(data, dict):
                        yield tuple(data.values())
                else:
                    for line in file:
                        data = json.loads(line)
                        if isinstance(data, list):
                            for item in data:
                                yield tuple(item.values())
                        elif isinstance(data, dict):
                            yield tuple(data.values())
  
        rows=[]
        for row in iter_json(file_path):
            rows.append(row)
        return pd.DataFrame(rows).fillna('')
    
    def parse_text(file_path):
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
            return pd.DataFrame(lines)

    def parse_file(file_path, file_type):
        if file_type == 'csv':
            return parse_csv(file_path)
        elif file_type == 'xml':
            return parse_xml(file_path)
        elif file_type == 'json':
            return parse_json(file_path)
        elif file_type == 'text':
            return parse_text(file_path)
        else:
            raise ValueError("Unsupported file type")

    def file_parser_udf(file_path, file_type):
        table = parse_file(file_path, file_type)
        
        # Your additional processing or analysis using NumPy can go here
        table = table.astype(str)

        return table

    return file_parser_udf(file_path2, file_type2)
};


-- U41.	File(q18): parses an external file (csv, xml, json) and returns a table 

CREATE or replace  FUNCTION file_q18(file_path2 STRING, file_type2 STRING)
RETURNS TABLE (column1 STRING, column2 STRING)
LANGUAGE PYTHON {

    import pandas as pd
    import xml.etree.ElementTree as ET
    import json
    import numpy as np

    def parse_csv(file_path):
        return pd.read_csv(file_path,header=None)

    def parse_xml(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        data = []
        columns = [child.tag for child in root[0]] if root else []

        for elem in root:
            row_data = [elem.find(column).text if elem.find(column) is not None else None for column in columns]
            data.append(row_data)

        return pd.DataFrame(data, columns=columns)

            
    def parse_json(file_path):
        def iter_json(file_path):
            with open(file_path, 'r') as file:
                first_character = file.read(1)
                file.seek(0)  # Reset the file pointer to the beginning
                if first_character == '[':
                    data = json.load(file)
                    if isinstance(data, list):
                        for item in data:
                            yield tuple(item.values())
                    elif isinstance(data, dict):
                        yield tuple(data.values())
                else:
                    for line in file:
                        data = json.loads(line)
                        if isinstance(data, list):
                            for item in data:
                                yield tuple(item.values())
                        elif isinstance(data, dict):
                            yield tuple(data.values())
  
        rows=[]
        for row in iter_json(file_path):
            rows.append(row)
        return pd.DataFrame(rows).fillna('')

    def parse_file(file_path, file_type):
        if file_type == 'csv':
            return parse_csv(file_path)
        elif file_type == 'xml':
            return parse_xml(file_path)
        elif file_type == 'json':
            return parse_json(file_path)
        else:
            raise ValueError("Unsupported file type")

    def file_parser_udf(file_path, file_type):
        table = parse_file(file_path, file_type)
        
        return table

    return file_parser_udf(file_path2, file_type2)
};




-- U42.	Output: Exports the results of a subquery to local storage in various formats and returns a True in success 

CREATE OR REPLACE FUNCTION output(
    doi string,
    amount string,
    numofpubs string,
    sdate string,
    output_path string,
    output_format string
)
RETURNS table (val boolean)
LANGUAGE PYTHON
{

    import csv
    import json
    import xml.etree.ElementTree as ET


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

        
    if type(doi)==numpy.ndarray or type(doi)==numpy.ma.core.MaskedArray:

        
        result = {'doi':doi,'amount':amount,'numofpubs': numofpubs,'sdate':sdate}

        if output_format[0].lower() == 'csv':
            return export_to_csv(result, output_path[0])
        elif output_format[0].lower() == 'json':
            return export_to_json(result, output_path[0])
        elif output_format[0].lower() == 'xml':
            return export_to_xml(result, output_path[0])
        else:
            return False

      
    else:
        return False
 
    
};




-- U43.	Getstats: gets a whole table with integer values as input and returns the avg and the median for each input column.

CREATE OR REPLACE FUNCTION getstats( value_column int)
RETURNS TABLE ( avg_val float, median_val float)
LANGUAGE PYTHON
{

    import pandas as pd
    try:
        if type(value_column)==numpy.ndarray or type(value_column)==numpy.ma.core.MaskedArray:
            avg_values=numpy.average(value_column)
            median_values = numpy.ma.median(value_column)

            return pd.DataFrame([(avg_values,median_values)])
        else:

            return pd.DataFrame([(None,None)])

    except:
        return pd.DataFrame([(None,None)])
};

-- U43.	Getstats: gets a whole table with integer values as input and returns the avg and the median for each input column with group by column.

CREATE OR REPLACE FUNCTION getstats(value_column int, group_column string)
RETURNS TABLE (group_column string, avg_val float, median_val float)
LANGUAGE PYTHON {

    import pandas as pd

    def group_avg(group_column, value_column, group_id):
        try:
            group_indices = numpy.where(group_column == group_id)[0]
            group_values = value_column[group_indices]
            avg_value = numpy.average(group_values)
            median_value = numpy.ma.median(group_values)
            return avg_value, median_value
        except:
            return None, None

    try:
        if isinstance(value_column, numpy.ndarray) or isinstance(value_column, numpy.ma.core.MaskedArray):
            unique_groups = numpy.unique(group_column)
            rows = []
            for group_id in unique_groups:
                avg_value, median_value = group_avg(group_column, value_column, group_id)
                rows.append((group_id, avg_value, median_value))
            return pd.DataFrame(rows, columns=['group_column', 'avg_val', 'median_val'])
        else:
            return pd.DataFrame([(None, None, None)], columns=['group_column', 'avg_val', 'median_val'])
    except:
        return pd.DataFrame([(None, None, None)], columns=['group_column', 'avg_val', 'median_val'])
};

-- U44.	Query q16b_fusion: 

CREATE or replace FUNCTION q16b_fused(pubdate string, projectstart string, projectend string, funder string, fclass string, projectid string)
RETURNS TABLE  (funder string, fclass string, projectid string, authors_during float,authors_before float,  authors_after float)
LANGUAGE PYTHON
{

        import pandas as pd
        from collections import defaultdict

        def cleandate(pubdate):
            if pubdate and pubdate!='-':
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

        if isinstance(projectid, (numpy.ndarray, numpy.ma.core.MaskedArray)):
        

            results = defaultdict(lambda: {'authors_during': None, 'authors_before': None, 'authors_after': None})
            for _projectid, _funder, _class, _pubdate, _projectstart, _projectend in zip(
                projectid, funder, fclass, pubdate, projectstart, projectend):                   

          
                pstartcleaned = cleandate(_projectstart)
                pendcleaned = cleandate(_projectend)
                pubdatecleaned = cleandate(_pubdate)
       
                key = (_funder, _class, _projectid)
                
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
    


            res = pd.DataFrame([
                [_funder, _class, _projectid, counts['authors_during'], counts['authors_before'], counts['authors_after']]
                for (_funder, _class, _projectid), counts in results.items()
            ], columns=['funder', 'fclass', 'projectid', 'authors_during', 'authors_before', 'authors_after'])
            return  res

        return pd.DataFrame(columns=['funder', 'fclass', 'projectid', 'authors_during', 'authors_before', 'authors_after'])
};    


-- U45.	Combinations_fusion

CREATE or replace FUNCTION combinations_fused(pubid string, pubdate string, projectstart string, projectend string, fundingstring string, input1 string, input2 integer)
RETURNS TABLE  (pubid string, pubdate string, projectstart string, projectend string, funder string, fclass string, projectid string,authorpair string)
LANGUAGE PYTHON
{

    import json
    import itertools
    import pandas as pd


    def jcombinations(jval,N):
        try:
            name_list = json.loads(jval)
            for name_per in itertools.combinations(name_list, N):
                yield json.dumps([name_per_i for name_per_i in name_per])

        except:
            yield('[]')  
            
             
    def extractfundingstring(project):
        try:
            listproject = project.split("::")
            return  listproject[0], listproject[1], listproject[2]
        except:
            return numpy.NaN,numpy.NaN,numpy.nan

    
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
            return numpy.nan
    
    reslist = {
        'pubid': [],
        'pubdate': [],
        'projectstart': [],
        'projectend': [],
        'funder': [],
        'fclass': [],
        'projectid': [],
        'authorpair': []
    }
    if type(input1)==numpy.ndarray or type(input1)==numpy.ma.core.MaskedArray:


        for _pubid, _pubdate, _projectstart, _projectend,fundingstring,arg1,arg2 in zip(pubid, pubdate, projectstart, projectend,fundingstring,input1,input2):
            (_funder, _class, _projectid) = extractfundingstring(fundingstring)
            _pubdate = _pubdate if _pubdate and _pubdate!='-' else numpy.nan
            _projectstart = _projectstart if _projectstart and _projectstart!='-' else numpy.nan
            _projectend = _projectend if _projectend and _projectend!='-' else numpy.nan
            for y in jcombinations(jfusedudfs(arg1),arg2):
                reslist['pubid'].append(_pubid)
                reslist['pubdate'].append(_pubdate)
                reslist['projectstart'].append(_projectstart)
                reslist['projectend'].append(_projectend)
                reslist['funder'].append(_funder)
                reslist['fclass'].append(_class)
                reslist['projectid'].append(_projectid)
                reslist['authorpair'].append(y)
                
    
        return pd.DataFrame(reslist)

    else:
        (_funder, _class, _projectid) = extractfundingstring(fundingstring)
        _pubdate = pubdate if pubdate and pubdate!='-' else numpy.nan
        _projectstart = projectstart if projectstart and projectstart!='-' else numpy.nan
        _projectend = projectend if projectend and projectend!='-' else numpy.nan
        for y in jcombinations(jfusedudfs(input1),input2):
            reslist['pubid'].append(_pubid)
            reslist['pubdate'].append(_pubdate)
            reslist['projectstart'].append(_projectstart)
            reslist['projectend'].append(_projectend)
            reslist['funder'].append(_funder)
            reslist['fclass'].append(_class)
            reslist['projectid'].append(_projectid)
            reslist['authorpair'].append(y)
        
        return pd.DataFrame(reslist)
    
};


-- U46. Logistic Regression UDF recursive


CREATE OR REPLACE FUNCTION logistic_regression_recursive_train(
    authorpair TEXT,
    mdate TEXT,  
    author_pair_column TEXT,  
    date_column TEXT,  
    max_iterations INT,  
    tolerance FLOAT
) RETURNS TABLE (weight FLOAT, bias FLOAT)
LANGUAGE PYTHON
{
    import pandas as pd
    import numpy as np

    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    def compute_loss(X, y, weights, bias):
        m = len(y)
        predictions = sigmoid(np.dot(X, weights) + bias)
        loss = - (1/m) * np.sum(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))
        return loss

    def recursive_gradient_descent(X, y, weights, bias, learning_rate=0.01, iteration=0, max_iterations=100, tolerance=1e-4):
        if iteration >= max_iterations:
            return weights, bias

        m = len(y)
        predictions = sigmoid(np.dot(X, weights) + bias)
        loss = compute_loss(X, y, weights, bias)

        # Compute gradients
        dw = (1/m) * np.dot(X.T, predictions - y)
        db = (1/m) * np.sum(predictions - y)

        # Update weights and bias
        weights -= learning_rate * dw
        bias -= learning_rate * db

        # Check for convergence
        if np.linalg.norm(dw) < tolerance and np.abs(db) < tolerance:
            return weights, bias

        # Recursive call for next iteration
        return recursive_gradient_descent(X, y, weights, bias, learning_rate, iteration + 1, max_iterations, tolerance)

    def train_logistic_regression(df, author_pair_column, date_column, max_iterations, tolerance):
        # Remove empty author pairs
        df = df[~df[author_pair_column].astype(str).isin(["['\"\"', '\"\"']"])]

        # Create target variable (whether the author pair will collaborate again)
        df = df.sort_values(by=[author_pair_column, date_column])
        df['will_collaborate_again'] = df.groupby(author_pair_column)[date_column].shift(-1).notnull().astype(int)

        # Drop NaN values in features
        df = df.dropna(subset=[date_column, 'will_collaborate_again'])

        # Feature engineering: Convert date to numerical format
        df[date_column] = pd.to_datetime(df[date_column])
        df['date_numeric'] = (df[date_column] - df[date_column].min()).dt.days

        # Define X (features) and y (target)
        X = df[['date_numeric']].values
        y = df['will_collaborate_again'].values

        # Initialize weights and bias
        weights = np.zeros(X.shape[1])
        bias = 0

        # Perform recursive gradient descent
        weights, bias = recursive_gradient_descent(X, y, weights, bias, max_iterations=max_iterations, tolerance=tolerance)

        return weights, bias

    df = pd.DataFrame({
        "authorpair": authorpair,
        "date": mdate
    })

    weights, bias = train_logistic_regression(df, author_pair_column[0], date_column[0], max_iterations[0], tolerance[0])
    result = {}
    result['weight'] = []
    result['bias'] = []
    for weight in weights:
        result['weight'].append(weight)
        result['bias'].append(bias)
    return result

};

-- U47. Logistic Regression UDF iterative
CREATE OR REPLACE FUNCTION logistic_regression_iterative_train(
    authorpair TEXT,
    mdate TEXT,  
    author_pair_column TEXT,  
    date_column TEXT,  
    max_iterations INT,  
    tolerance FLOAT
) RETURNS TABLE (weight FLOAT, bias FLOAT)
LANGUAGE PYTHON
{
    import pandas as pd
    import numpy as np

    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    def compute_loss(X, y, weights, bias):
        m = len(y)
        predictions = sigmoid(np.dot(X, weights) + bias)
        loss = - (1/m) * np.sum(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))
        return loss

    def iterative_gradient_descent(X, y, weights, bias, learning_rate=0.01, max_iterations=100, tolerance=1e-4):
        m = len(y)
        for _ in range(max_iterations):
            predictions = sigmoid(np.dot(X, weights) + bias)
            loss = compute_loss(X, y, weights, bias)

            # Compute gradients
            dw = (1/m) * np.dot(X.T, predictions - y)
            db = (1/m) * np.sum(predictions - y)

            # Update weights and bias
            weights -= learning_rate * dw
            bias -= learning_rate * db

            # Check for convergence
            if np.linalg.norm(dw) < tolerance and np.abs(db) < tolerance:
                break

        return weights, bias

    def train_logistic_regression(df, author_pair_column, date_column, max_iterations, tolerance):
        # Remove empty author pairs
        df = df[~df[author_pair_column].astype(str).isin(["['\"\"', '\"\"']"])]

        # Create target variable (whether the author pair will collaborate again)
        df = df.sort_values(by=[author_pair_column, date_column])
        df['will_collaborate_again'] = df.groupby(author_pair_column)[date_column].shift(-1).notnull().astype(int)

        # Drop NaN values in features
        df = df.dropna(subset=[date_column, 'will_collaborate_again'])

        # Feature engineering: Convert date to numerical format
        df[date_column] = pd.to_datetime(df[date_column])
        df['date_numeric'] = (df[date_column] - df[date_column].min()).dt.days

        # Define X (features) and y (target)
        X = df[['date_numeric']].values
        y = df['will_collaborate_again'].values

        # Initialize weights and bias
        weights = np.zeros(X.shape[1])
        bias = 0

        # Perform iterative gradient descent
        weights, bias = iterative_gradient_descent(X, y, weights, bias, max_iterations=max_iterations, tolerance=tolerance)

        return weights, bias


    df = pd.DataFrame({
        "authorpair": authorpair,
        "date": mdate
    })

    weights, bias = train_logistic_regression(df, author_pair_column[0], date_column[0], max_iterations[0], tolerance[0])
    result = {}
    result['weight'] = []
    result['bias'] = []
    for weight in weights:
        result['weight'].append(weight)
        result['bias'].append(bias)
    return result

   
};



