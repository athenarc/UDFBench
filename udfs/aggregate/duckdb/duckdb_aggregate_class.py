import duckdb
import numpy as np
import pyarrow as pa
import os


class Aggregate:
    def __init__(self,con):
        self.con = con.cursor()

#  U26.	Avg: Calculates average

    def aggregate_avg(self,subquery:str,value_column:str)->float:
        import numpy as np
        import pyarrow as pa
        import pandas as pd

        try:
            table = self.con.sql(str(subquery)).fetchdf()
            value_column = str(value_column)
            avg_val = table[value_column].mean() if not table[value_column].isnull().all() else np.nan

            return avg_val
        except:
            return None

    #  U26.	Avg(v2): Calculates average with group by

    def aggregate_avg_v2(self,subquery:str,value_column:str,group_column=None)->float:
        import numpy as np
        import pandas as pd
        import pyarrow as pa
        try:
            table = self.con.sql(str(subquery)).fetchdf()
            table = table.where(pd.notnull(table), None)
            table.dropna(inplace=True)
            result = table.groupby(str(group_column))[str(value_column)].agg(['mean']).reset_index()
            return result.to_dict('records')
        except:
            return [None]

    #  U27.	Count: Calculates count 

    def aggregate_count(self,subquery:str,value_column:str)->int:
        import numpy as np
        import pandas as pd
        import pyarrow as pa
        try:
            table = self.con.sql(str(subquery)).fetchdf()
            table = table.where(pd.notnull(table), None)
            count_vals =  int(table[str(value_column)].count())
            return count_vals
        except:
            return None


    # U27.	Count(v2): Calculates count  with group by

    def aggregate_count_v2(self,subquery:str,value_column:str,group_column=None)->float:
        import numpy as np
        import pandas as pd
        import pyarrow as pa
        try:
            table = self.con.sql(str(subquery)).fetchdf()
            table = table.where(pd.notnull(table), None)
            table.dropna(inplace=True)
            result = table.groupby(str(group_column))[str(value_column)].agg(['count']).reset_index()
            return result.to_dict('records')
        except:
            return [None]

    #  U28. Max: Calculates max date with group by

    def aggregate_max(self,subquery:str,value_column:str,group_column=None)->str:
        import numpy as np
        import pyarrow as pa
        import pandas as pd

        try:
            table = self.con.sql(str(subquery)).fetchdf()
            table = table.where(pd.notnull(table), None)
            table.dropna(inplace=True)
            result = table.groupby(str(group_column))[str(value_column)].agg(['max']).reset_index()
            return result.to_dict('records')
        except:
            return [None]

    #  U28. Max(v2): Calculates max date

    def aggregate_max_v2(self,subquery:str,value_column:str)->str:
        import numpy as np
        import pandas as pd
        import pyarrow as pa
        try:
            table = self.con.sql(str(subquery)).fetchdf()
            max_val =  np.NaN if table[str(value_column)].isnull().all()  else np.nanmax(table[str(value_column)])
            return max_val
        except:
            return None

    #  U29.	Median: Calculates median
    def aggregate_median(self,subquery:str,value_column:str)->float:
        import numpy as np
        import pandas as pd
        import pyarrow as pa

        try:
            table = self.con.sql(str(subquery)).fetchdf()
            value_column = str(value_column)
            median_val = table[value_column].median() if not table[value_column].isnull().all() else np.nan

            # median_val =  np.NaN if table[str(value_column)].isnull().all()  else np.nanmedian(table[str(value_column)])
            return median_val
        except:
            return None

    #  U29.	Median(v2): Calculates median with group by

    def aggregate_median_v2(self,subquery:str,value_column:str,group_column=None)->float:
        import numpy as np
        import pandas as pd
        import pyarrow as pa
        try:
            table = self.con.sql(str(subquery)).fetchdf()
            table = table.where(pd.notnull(table), None)
            table.dropna(inplace=True)
            result = table.groupby(str(group_column))[str(value_column)].agg(['median']).reset_index()
            return result.to_dict('records')
        except:
            return [None]