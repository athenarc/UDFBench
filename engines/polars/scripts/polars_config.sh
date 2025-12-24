export POLARSQUERIES=$PWD'/engines/polars/queries'
export POLARSSCRIPTS=$PWD'/engines/polars/scripts'
export POLARSEXEC=$PWD'/engines/polars/queries/exec.py'
export POLARSSCHEMA=$PWD'/engines/polars/scripts/polars_schema.py'


export POLARSSCALAR=$PWD'/engines/polars/udfs/scalar/scalar.py'
export POLARSAGGR=$PWD'/engines/polars/udfs/aggregate/aggrs.py'
export POLARSTABLE=$PWD'/engines/polars/udfs/table/table.py'
# Can be 'csv' or 'parquet'
export POLARSDATAFORMAT="csv"
export POLARSRESULTSPATH=$PWD'/results/logs/polars'

export POLARSSSDPATH=$PWD'/databases/polars'
export POLARSMEMPATH=''
export POLARSHDDPATH=''