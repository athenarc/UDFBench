
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

