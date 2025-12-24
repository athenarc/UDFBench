export PANDASQUERIES=$PWD'/engines/pandas/queries'
export PANDASSCRIPTS=$PWD'/engines/pandas/scripts'
export PANDASEXEC=$PWD'/engines/pandas/queries/exec.py'
export PANDASSCHEMA=$PWD'/engines/pandas/scripts/pandas_schema.py'
export PANDASSCALAR=$PWD'/engines/pandas/udfs/scalar/scalar.py'
export PANDASAGGR=$PWD'/engines/pandas/udfs/aggregate/aggrs.py'
export PANDASTABLE=$PWD'/engines/pandas/udfs/table/table.py'
# Can be 'csv' or 'parquet'
export PANDASDATAFORMAT="csv"
export PANDASRESULTSPATH=$PWD'/results/logs/pandas'
# Can be 'pandas' or 'modin'
export DFENGINE="pandas"
# export DFENGINE="modin"
export PANDASSSDPATH=$PWD'/databases/pandas'

export PANDASMEMPATH=''
export PANDASHDDPATH=''