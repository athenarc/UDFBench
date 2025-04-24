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