-- U30.	Extractfromdate: Reads a date (as a string) and returns 3 column values (year, month, day)

CREATE TYPE _extractfromdate AS (
    extractyear integer, 
    extractmonth integer,
    extractday integer
);

CREATE or replace FUNCTION extractfromdate(arg text)
    RETURNS _extractfromdate
AS $$
        try:
            return {"extractyear":int(arg[:arg.find('-')]),
                    "extractmonth":int(arg[arg.find('-')+1:arg.rfind('-')]),
                    "extractday":int(arg[arg.rfind('-')+1:])
            }
        except:
            return {"extractyear":-1,
                    "extractmonth":-1,
                    "extractday":-1
            }

$$
LANGUAGE 'plpython3u'IMMUTABLE STRICT PARALLEL SAFE;

-- U31.	Jsonparse: Parses a json dict per time and returns a tuple with the values

CREATE OR REPLACE FUNCTION jsonparse(subquery text,column_name text,key1  text, key2 text) 
RETURNS SETOF RECORD AS $$
    import plpy

    try:
        import json
        for line in plpy.execute(subquery):
            data = json.loads(line[column_name])
            if isinstance(data, list):
                for item in data:
                    yield (item.get(key1),item.get(key2))
            elif isinstance(data, dict):
                yield (data.get(key1),data.get(key2)) 
            else:
                yield None,None
    

    except Exception as e:
        plpy.error(f"Error parsing JSON content: {str(e)}")
        return None,None


$$ LANGUAGE 'plpython3u'IMMUTABLE STRICT PARALLEL SAFE;


-- U32.	Combinations: Reads a json list and returns a table with all the combinations per an integer parameter

CREATE OR REPLACE FUNCTION combinations(val text,numcomb int)
    RETURNS TABLE  (authorpair text)
AS $$
        import json
        import itertools
        def jcombinations(jval,N):
            try:
                name_list = json.loads(jval)
                for name_per in itertools.combinations(name_list, N):
                    yield [json.dumps(name_i) for name_i in name_per]
    
            except:
                yield('[]')

        for row in jcombinations(val,numcomb):
            yield(row)
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;

-- U33.	Extractkeys: Selects keys from xml parsed input 

CREATE OR REPLACE FUNCTION extractkeys(jval text,key1 text,key2 text) 
RETURNS TABLE (
    key1 text,
    key2 text
) AS $$
    import json
    import plpy

    try:
        data = json.loads(jval)

        if isinstance(data, list):
            for item in data:
                yield (item.get(key1),item.get(key2))

        elif isinstance(data, dict):
            # Extract values dynamically for all keys in the dictionary
            yield (data.get(key1),data.get(key2))

        else:
            yield (None,None)

    except Exception as e:
        plpy.error(f"Error extracting keys from XML content: {str(e)}")
        return (None,None)
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;



-- U34.	Strsplitv: Processes a string at a time and returns its tokens in separate rows 

CREATE OR REPLACE FUNCTION strsplitv(val text)
    RETURNS TABLE  (word text)
AS $$

        def strsplitv(val):
            try:
                return val.split()   
            except:
                return ['']
        return strsplitv(val)
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;



-- U35.	JGROUPORDERED: Processes a subquery which is ordered by an attribute, and runs a group by with an aggregate defined as a (named) parameter

CREATE OR REPLACE FUNCTION JGROUPORDERED(
    subquery text,
    order_by_col text,
    count_col text
)
RETURNS TABLE ( term text,docid text, tf float, jcount bigint)
AS $$
    import pandas as pd

    def process_ordered_group(subquery, order_by_col,count_col):
        try:
            rows = plpy.execute(subquery + f" ORDER BY {order_by_col}")
            data = list(rows)

            df = pd.DataFrame(data)

            df['jcount'] = df.groupby([order_by_col])[count_col].transform('size')

            for _, row in df.iterrows():
                yield tuple(row.values)

        except Exception as e:
            plpy.error(f"Error processing ordered group: {str(e)}")
            return None

    return process_ordered_group(subquery, order_by_col,count_col)
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;


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




-- U38.	Xmlparser :  Parses xml input and returns a table 

CREATE OR REPLACE FUNCTION xmlparser(subquery text,root_name text,column_name text) 
RETURNS SETOF RECORD AS $$
    import xml.etree.ElementTree as ET
    import plpy
    import json
    import re
    
    result_text = ''
    result_text = '\n'.join([str(row[column_name]) for row in plpy.execute(subquery)])

    try:
        root = ET.fromstring(result_text)

        for elem in root.iter(root_name):
            record = {}
            for item in elem:
                record[item.tag] = item.text
            yield (json.dumps(record),)

    except Exception as e:
        plpy.error(f"Error parsing XML: {str(e)}")
        return None
$$ LANGUAGE 'plpython3u'IMMUTABLE STRICT PARALLEL SAFE;




-- U39.	Pivot: Converts rows of a specific attribute (optionally grouped by another attribute) into columns, while applying an aggregation within the transformed dataset. It returns one tuple per input group

CREATE OR REPLACE FUNCTION pivot(
    subquery text, 
    group_by_column text, 
    pivot_column text,    
    aggregate_function text -- Aggregate function to apply(size,sum )
)RETURNS SETOF RECORD
AS $$
    import pandas as pd
    import plpy

    try:
        rows = plpy.execute(subquery)
        data = list(rows)
        df = pd.DataFrame(data)

        pivoted_df = df.pivot_table(
            index=group_by_column,
            columns=pivot_column,
            aggfunc=aggregate_function,
            fill_value=0
        ).reset_index()

        for row in pivoted_df.itertuples(index=False):
            yield tuple(row)

    except:
        return None
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;


-- U40.	Top: Processes one group at a time and returns the top N values of an attribute 


CREATE OR REPLACE FUNCTION aggregate_top(subquery text, top_n int,group_col text,value_col text)
RETURNS SETOF record
AS $$
    import pandas as pd

    try:
        rows = plpy.execute(subquery)

        data = list(rows)
        dataset = pd.DataFrame(data) 
        df = dataset.groupby(group_col).apply(lambda x: x.nlargest(top_n, value_col)).reset_index(drop=True)
        df.dropna(inplace=True)  

        for _, row in df.iterrows():
            yield tuple(row.values)

       
    except:
        return None
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;


-- U40.	Top (v2 without parallelism): Processes one group at a time and returns the top N values of an attribute 

CREATE OR REPLACE FUNCTION aggregate_top_v2(subquery text, top_n int,group_col text,value_col text)
RETURNS SETOF record
AS $$

    import pandas as pd

    try:
        rows = plpy.execute(subquery)

        data = list(rows)
        dataset = pd.DataFrame(data)  
        df = dataset.groupby(group_col).apply(lambda x: x.nlargest(top_n, value_col)).reset_index(drop=True)

        for _, row in df.iterrows():
            yield tuple(row.values)

       
    except:
        return None
$$ LANGUAGE 'plpython3u';



-- U41.	File: parses an external file (csv, xml, json) and returns a table 

CREATE OR REPLACE FUNCTION file(file_path text,file_type text)
RETURNS SETOF RECORD
LANGUAGE plpython3u
AS $$
    import csv
    import os
    import json
    import xml.etree.ElementTree as ET
    import plpy
    import pandas as pd

    def parse_csv(file_path):
        df = pd.read_csv(file_path,header=None)
        df = df.where(pd.notnull(df), None)
        for _, row in df.iterrows():
                yield tuple(row.values)


    def parse_csv2(file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield tuple(row.values())

    def read_json(file_path):
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
       
    def read_xml(file_path):
        def parse_xml(xml_file_path):
            root = ET.parse(xml_file_path).getroot()
            data = []
            columns = []
            
            for elem in root:
                if not columns:
                    columns = [child.tag for child in elem]

                row_data = [elem.find(column).text if elem.find(column) is not None else None for column in columns]
                data.append(row_data)
            return data
        for record in parse_xml(file_path):
            yield tuple(record)
  
    def parse_text(file_path):
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
            for _line in lines:
                yield (_line,)

    if file_type == 'csv':
        return parse_csv(file_path)
    elif file_type == 'json':
        return read_json(file_path)
    elif file_type == 'xml':
        return read_xml(file_path)
    elif file_type == 'text':
        return parse_text(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_type}")
$$ IMMUTABLE STRICT PARALLEL SAFE;



-- U42.	Output: Exports the results of a subquery to local storage in various formats and returns a True in success 


CREATE OR REPLACE FUNCTION output(
    subquery text,
    output_format text,
    output_path text
)
RETURNS TABLE(res boolean)
LANGUAGE plpython3u
AS $$
    import csv
    import json
    import xml.etree.ElementTree as ET

    def execute_subquery(subquery):
        result = plpy.execute(subquery)
        return result

    def export_to_csv(result, output_path):
        with open(output_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(result[0].keys())
            for row in result:
                csv_writer.writerow(row.values())
        return True

    def export_to_json(result, output_path):
        with open(output_path, 'w') as jsonfile:
            json.dump(list(result), jsonfile, indent=2)
        return True

    def export_to_xml(result, output_path):
        root = ET.Element('root')
        for row in list(result):
            result_element = ET.SubElement(root, 'publication')
            for key, value in row.items():
                ET.SubElement(result_element, key).text = str(value)

        tree = ET.ElementTree(root)
        tree.write(output_path)
        return True

    try:
        result = execute_subquery(subquery)

        if output_format.lower() == 'csv':
            yield export_to_csv(result, output_path)
        elif output_format.lower() == 'json':
            yield export_to_json(result, output_path)
        elif output_format.lower() == 'xml':
            yield export_to_xml(result, output_path)
        else:
            plpy.error('Unsupported output format')
            yield False

    except Exception as e:
        plpy.error(str(e))
        yield False
$$ IMMUTABLE STRICT PARALLEL SAFE;



-- U43.	Getstats: gets a whole table with integer values as input and returns the avg and the median for each input column.

CREATE OR REPLACE FUNCTION getstats(subquery text, value_column text,group_column text)
RETURNS SETOF record
AS $$
    import numpy as np
    import plpy

    def group_avg_median(group_column, value_column, group_id):
        try:
            group_indices = np.where(group_column == group_id)[0]

            group_values = value_column[group_indices]
            avg_indices = np.nanmean(group_values)
            median_indices = np.ma.median(group_values)
            return avg_indices,median_indices

        except Exception as e:
            plpy.error(f"Error processing group {group_id}: {str(e)}")
            return None

    try:
        rows = plpy.execute(subquery)
        if group_column:
            value_column_np = np.array([row[value_column] for row in rows])  
            group_column_np = np.array([row[group_column] for row in rows]) 

            unique_groups = list(set(group_column_np))

            for group_id in unique_groups:
                avg_values,median_values= group_avg_median(group_column_np, value_column_np, group_id)
                yield (group_id,float(avg_values),float(median_values))

        else:
            value_column_np = np.array([row[value_column] for row in rows]) 
            value_column_np = value_column_np[value_column_np !=None]
            avg_values=np.average(value_column_np)

            median_values = np.ma.median(value_column_np)

            yield float(avg_values),float(median_values)
       
    except Exception as e:
        plpy.error(f"Error returning stats: {str(e)}")
        yield None
$$
LANGUAGE 'plpython3u';


-- U44.	Query q16b_fusion: .

CREATE OR REPLACE FUNCTION q16b_fused(subquery text)
    RETURNS TABLE  (funder text, _class text, projectid text, authors_during int,authors_before int,  authors_after int)
AS $$
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


            rows = plpy.execute(subquery)
            results = defaultdict(lambda: {'authors_during': None, 'authors_before': None, 'authors_after': None})

            for row in rows:
                invalid_val = True 
                funder = row['funder']
                _class = row['_class']
                projectid = row['projectid']
                
                pstartcleaned = cleandate(row['projectstart'])
                pendcleaned = cleandate(row['projectend'])
                pubdatecleaned = cleandate(row['pubdate'])
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
    
  
            for (funder, _class, projectid), counts in results.items():
                yield (funder, _class, projectid, counts['authors_during'], counts['authors_before'], counts['authors_after'])

        
        except Exception as e:
            plpy.error(f"An error occurred: {e}")
            return (None, None, None, None, None, None)
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;





-- U45.	Combinations_fusion

CREATE OR REPLACE FUNCTION combinations_fused(fundingstring text,authorlist text,numcomb int)
    RETURNS TABLE  (funder text, _class text, projectid text, authorpair text)
AS $$
        import json
        import itertools
        def jcombinations(jval,N):
            try:
                name_list = json.loads(jval)
                for name_per in itertools.combinations(name_list, N):
                    yield [json.dumps(name_i) for name_i in name_per]
    
            except:
                yield('[]')
                
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



        (funder, _class, projectid) = extractfundingstring(fundingstring)

        for row in jcombinations(jfusedudfs(authorlist),numcomb):
            yield(funder,_class,projectid,row)
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;

CREATE TYPE logistic_regression_result AS (
    weight FLOAT,
    bias FLOAT
);



-- U46. Logistic Regression UDF recursive
CREATE OR REPLACE FUNCTION logistic_regression_recursive_train(
    subquery TEXT,  
    author_pair_column TEXT,  
    date_column TEXT,  
    max_iterations INT DEFAULT 100,  
    tolerance FLOAT DEFAULT 1e-4
) RETURNS SETOF logistic_regression_result
AS $$
    import pandas as pd
    import plpy
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

    try:
        rows = plpy.execute(subquery)
        data = list(rows)
        df = pd.DataFrame(data)

        # Train logistic regression
        weights, bias = train_logistic_regression(df, author_pair_column, date_column, max_iterations, tolerance)

        # Return the trained weights and bias
        result = []
        for weight in weights:
            result.append((weight, bias))

        # Return results as a set of logistic_regression_result
        for res in result:
            yield res

    except Exception as e:
        plpy.error(f"Error in logistic_regression_recursive_train: {str(e)}")
        return None
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;





-- U47. Logistic Regression UDF iterative
CREATE OR REPLACE FUNCTION logistic_regression_iterative_train(
    subquery TEXT,  
    author_pair_column TEXT,  
    date_column TEXT,  
    max_iterations INT DEFAULT 100,  
    tolerance FLOAT DEFAULT 1e-4
) RETURNS SETOF logistic_regression_result
AS $$
    import pandas as pd
    import plpy
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

    try:
        rows = plpy.execute(subquery)
        data = list(rows)
        df = pd.DataFrame(data)

        # Train logistic regression
        weights, bias = train_logistic_regression(df, author_pair_column, date_column, max_iterations, tolerance)

        # Return the trained weights and bias
        result = []
        for weight in weights:
            result.append((weight, bias))

        # Return results as a set of logistic_regression_result
        for res in result:
            yield res

    except Exception as e:
        plpy.error(f"Error in logistic_regression_iterative_train: {str(e)}")
        return None
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;


