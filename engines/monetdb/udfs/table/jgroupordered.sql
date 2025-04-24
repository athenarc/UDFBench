
-- U35.	Jgroupordered: Processes a subquery which is ordered by an attribute, and runs a group by with an aggregate defined as a (named) parameter

CREATE OR REPLACE FUNCTION jgroupordered(
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