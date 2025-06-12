# To install and experiment with the benchmark run the following steps:

# 1. Grant execute permissions to bash scripts, with the following command:
find . -type f -name "*.sh" -exec  chmod +x {} \;

# 2. Update the configuration file as needed, then apply the changes:
"./automations/config_udfbench.sh"

Before running the benchmark, or executing any of the  scripts, you need to configure a set of environment variables, such as UDFs, queries, executables, databases storage paths.
These variables should be updated based on your system’s set up and directory structure.
By default, the configuration files in the engines folder ("$system"_config.sh) are set up to create all the required systems from the beginning.

 Variables in the Configuration file (automations/config_udfbench.sh) common for all systems:
1.	PYTHONEXEC: Path to the Python executable, used for Python scripts (e.g., export PYTHONEXEC='python3.10' ).
2.	EXTERNALPATHSSD: The path to the folder where external data files on SSD storage (CSV, XML, JSON, etc.) are stored. These files are required by some queries to run (e.g., export EXTERNALPATHSSD=PWD'/dataset/files') 
3.	EXTERNALPATHMEM: The path to the folder where in-memory external data files (CSV, XML, JSON, etc.) are stored. These files are required by some queries to run (e.g., export EXTERNALPATHMEM=PWD'/dataset/files'  where $PWD is /dev/shm/path  a temporary storage path) 
4.	EXTERNALPATHHDD: The path to the folder where external data files on HDD storage (CSV, XML, JSON, etc.) are stored. These files are required by some queries to run (e.g., export EXTERNALPATHHDD=PWD'/dataset/files'  where $PWD is /hdd/path) 
5.  DATASETSPATHSSD: Path to the folder where the CSV and Parquet files on SSD storage are stored. This directory is  structured with subfolders for organizing different file types used in data loading and processing  (e.g., export DATASETSPATHSSD=$PWD'/dataset', with DATASETSPATHSSD/csvs and DATASETSPATHSSD/parquet: Contains CSV, Parquet files needed to load data into the databases.).
6.  DATASETSPATHMEM: Path to the folder where the in-memory CSV and Parquet files are stored. This directory is  structured with subfolders for organizing different file types used in data loading and processing (e.g., export DATASETSPATHMEM=$PWD'/dataset', with DATASETSPATHMEM/csvs and DATASETSPATHMEM/parquet: Contains CSV, Parquet files needed to load data into the databases, where $PWD is /dev/shm/path  a temporary storage path).
7.  DATASETSPATHHDD: Path to the folder where the CSV and Parquet files on HDD storage are stored. This directory is  structured with subfolders for organizing different file types used in data loading and processing  (e.g., export DATASETSPATHSSD=$PWD'/dataset', with DATASETSPATHSSD/csvs and DATASETSPATHSSD/parquet: Contains CSV, Parquet files needed to load data into the databases,  where $PWD is /hdd/path). 

Variables in the Configuration file for PostgresSQL:
1.	PSQLPATH: Path to the PostgreSQL psql command-line (e.g., export PSQLPATH=$PWD'/databases/postgres/bin/psql').

2.	POSTGRESPATH: Path to the PostgreSQL database storage directory (e.g., export POSTGRESPATH=$PWD'/databases/postgres').

3.	PSQLSSDPORT:  Port for PostgreSQL database running on SSD storage (e.g. , export PSQLSSDPORT = “50007” where this port refers to /ssd/path).

4.	PSQLHDDPORT:   Port for PostgreSQL database running on HDD storage. By default, this variable is empty  (e.g. , export PSQLHDDPORT = “50009” where this port refers to /hdd/path).

5.	PSQLMEMPORT: Port for PostgreSQL database running in-memory. By default, this variable is empty  (e.g., /dev/shm). (e.g.  export PSQLMEMPORT=”50010” where this port refers to /dev/shm/path  a temporary storage path).

6.	PSQLUSER: PostgreSQL user name usually the system user (e.g.  export PSQLUSER=$USER).

7.	POSTGRESQUERIES: Path to the PostgreSQL SQL query files (e.g., export POSTGRESQUERIES=$PWD'/engines/postgres/queries').

8.	POSTGRESUDFS: Path to the folder containing PostgreSQL User-Defined Function (UDF) files.(e.g., export POSTGRESUDFS=$PWD'/engines/postgres/udfs').

9.	POSTGRESSCRIPTS: Path to the folder containing PostgreSQL scripts (e.g., export POSTGRESSCRIPTS=$PWD'/engines/postgres/scripts').

10.	POSTGRESRESULTSPATH: Path to the folder where PostgreSQL query results or collectl are stored (e.g., export POSTGRESRESULTSPATH=$PWD'/results/logs/postgres').


Variables in the Configuration file for MonetDB:
1.	MONETDBPATH: Path to the MonetDB mclient command-line(e.g., export MONETDBPATH=$PWD'/databases/monetdb/bin/mclient').

2.	MONETDBDIRPATH: Path to the MonetDB database storage directory (e.g., export MONETDBDIRPATH=$PWD'/databases/monetdb).

3.	MONETDBSSDPORT: Port for MonetDB database running on SSD storage (e.g. , export MONETDBSSDPORT = “50007” where $MONETDBINSTANCE is /ssd/path).

4.	MONETDBHDDPORT: Port for MonetDB database running on HDD storage. By default, this variable is empty (e.g. , export MONETDBHDDPORT= “50011” where MONETDBINSTANCE is /hdd/path).

5.	MONETDBMEMPORT: Port for MonetDB database running in-memory By default, this variable is empty (e.g.,  export MONETDBMEMPORT=”50012” where MONETDBINSTANCE is /dev/shm/path,  a temporary storage path).

6.	MONETDBBINPATH: Path to the MonetDB binary folder (e.g., export MONETDBBINPATH=$PWD'/databases/monetdb/bin/’).

7.	MONETDBINSTANCE: Path to a specific database instance within MonetDB. You can set this variable based on the specific storage type (SSD, HDD, or memory). By default, the database instance is located under the MONETDBDIRPATH directory (e.g., export MONETDBINSTANCE='udfbench').

8.	MONETDBQUERIES: Path to the MonetDB SQL query files (e.g., export MONETDBQUERIES=$PWD'/engines/monetdb/queries').

9.	MONETDBUDFS: Path to the folder containing MonetDB User-Defined Function (UDF) files.(e.g., export MONETDBUDFS=$PWD'/engines/monetdb/udfs').

10.	MONETDBSCRIPTS: Path to the folder containing MonetDB scripts (e.g., export MONETDBSCRIPTS=$PWD'/engines/monetdb/scripts').

11.	MONETDBRESULTSPATH: Path to the folder where MonetDB query results or collectl are stored (e.g., export MONETDBRESULTSPATH=$PWD'/results/logs/monetdb').



Variables in the Configuration file for SQLite:
1.	SQLITEPATH: Path to the SQLite script script to run queries that only require scalar or aggregate UDFs (e.g., export SQLITEPATH=$PWD'/engines/sqlite/queries/exec.py')

2.	SQLITEEXEC: The SQLite3 executable used to connect to SQLite databases directly from the terminal (e.g. export SQLITEEXEC='sqlite3').

3.	SQLITEDBSSDPATH:  Path to the SQLite databases stored on SSD (e.g. , export SQLITEDBSSDPATH = $PWD’ /databases/sqlite/’ where $PWD is /ssd/path)

4.	SQLITEDBMEMPATH:   Path to the SQLite databases stored in-memory (e.g. , export SQLITEDBMEMPATH $PWD’ /databases/sqlite/’ where $PWD is /dev/shm/path  a temporary storage path)

5.	SQLITEDBHDDPATH: Path to the SQLite databases stored on HDD . By default, this variable is empty (e.g.  export SQLITEDBHDDPATH =$PWD’ /databases/sqlite/’  where $PWD is /hdd/path)

6.	SQLITEQUERIES: Path to the SQLite SQL query files (e.g., export SQLITEQUERIES=$PWD'/engines/sqlite/queries').

7.	SQLITEUDFS: Path to the folder containing SQLite User-Defined Function (UDF) files.(e.g., export SQLITEUDFS=$PWD'/engines/sqlite/udfs').

8.	SQLITESCRIPTS: Path to the folder containing SQLite scripts (e.g., export SQLITESCRIPTS=$PWD'/engines/sqlite/scripts').

9.	SQLITERESULTSPATH: Path to the folder where SQLite query results or collectl are stored (e.g., export SQLITERESULTSPATH=$PWD'/results/logs/sqlite').


Variables in the Configuration file for SQLitevtab:
1.	SQLITEVTABPATH/SCRIPTPATH: Path to a custom SQLite virtual table (VTAB) script to run queries that require table UDFs. (e.g., export SQLITEVTABPATH=$PWD'/engines/sqlitevtab/queries/mexec.py')

2.	SQLITEVTABEXEC: The SQLite3 executable used to connect to SQLitevtab databases directly from the terminal (e.g. export SQLITEVTABEXEC='sqlite3').

3.	SQLITEVTABDBSSDPATH:  Path to the SQLitevtab databases stored on SSD (e.g. , export SQLITEVTABDBSSDPATH = $PWD’ /databases/sqlitevtab/’ where $PWD is /ssd/path)

4.	SQLITEVTABDBMEMPATH:   Path to the SQLitevtab databases stored in-memory (e.g. , export SQLITEVTABDBMEMPATH $PWD’ /databases/sqlitevtab/’ where $PWD is /dev/shm/path  a temporary storage path)

5.	SQLITEVTABDBHDDPATH: Path to the SQLitevtab databases stored on HDD . By default, this variable is empty (e.g.  export SQLITEVTABDBHDDPATH =$PWD’ /databases/sqlitevtab/’  where $PWD is /hdd/path)

6.	SQLITEVTABQUERIES: Path to the SQLitevtab SQL query files (e.g., export SQLITEVTABQUERIES=$PWD'/engines/sqlsqlitevtabite/queries').

7.	SQLITEVTABUDFS: Path to the folder containing SQLitevtab User-Defined Function (UDF) files (e.g., export SQLITEVTABUDFS=$PWD'/engines/sqlitevtab/udfs').

8.	SQLITEVTABSCRIPTS: Path to the folder containing SQLitevtab scripts (e.g., export SQLITEVTABSCRIPTS=$PWD'/engines/sqlitevtab/scripts').

9.	SQLITEVTABRESULTSPATH: Path to the folder where SQLitevtab query results or collectl are stored (e.g., export SQLITEVTABRESULTSPATH=$PWD'/results/logs/sqlitevtab').

12.	SQLITEVTABFUNCTIONS: Path to the UDFs for SQLite virtual table (VTAB)  (e.g., export SQLITEVTABFUNCTIONS=$PWD'/queries/sqlitevtab/functions').



Variables in the Configuration file for DuckDB:
1.	DUCKDBEXEC: Path to the DuckDB executable (e.g., export DUCKDBEXEC=$PWD'/engines/duckdb/queries/exec.py')

2.	DUCKDBSSDPATH:  Path to the DuckDB databases stored on SSD (e.g., export DUCKDBSSDPATH= $PWD’ /databases/duckdb/’ where $PWD is /ssd/path)

3.	DUCKDBMEMPATH:   Path to the DuckDB databases stored in-memory. By default, this variable is empty (e.g., export DUCKDBMEMPATH = $PWD'/databases/duckdb’ where $PWD is /dev/shm/path  a temporary storage path)

4.	DUCKDBHDDPATH: Path to the DuckDB databases stored on HDD. By default, this variable is empty (e.g.,  export DUCKDBHDDPATH= $PWD'/databases/duckdb’  where $PWD is /hdd/path)

5.	DUCKDBUDFS: Path to the DuckDB UDFs (User Defined Functions) library (e.g., export DUCKDBUDFS=$PWD'/engines/duckdb/udfs').

6.	DUCKDBQUERIES: Path to the DuckDB SQL query files (e.g., export DUCKDBQUERIES=$PWD'/engines/duckdb/queries').

7.	DUCKDBCLI: Path to the DuckDB CLI (Command Line Interface) executable. The CLI is used to connect to the DuckDB  databases directly from the terminal (e.g., export DUCKDBCLI=$PWD'/databases/duckdb/cli/duckdb').

8.	DUCKDBSCRIPTS: Path to the folder containing DuckDB scripts (e.g.,export DUCKDBSCRIPTS=$PWD'/engines/duckdb/scripts').

9.	DUCKDBRESULTSPATH: Path to the folder where DuckDB query results or collectl are stored (e.g., export DUCKDBRESULTSPATH=$PWD'/results/logs/duckdb').



Variables in the Configuration file for PySpark:
1.	PYSPARKPATH: Path to the PySpark executable (e.g., export PYSPARKPATH=$PWD'/engines/pyspark/queries/exec.py').

2.	PARQUETPATHSSD: Path to the folder where Parquet files are stored on SSD  (e.g., export PARQUETPATHSSD=$PWD'/databases/pyspark/parquet').

3.	PARQUETPATHMEM: Path to the folder where Parquet files are stored  in-memory. By default, this variable is empty (e.g., export PARQUETPATHMEM = $PWD'/databases/pyspark/parquet' where $PWD is /dev/shm/path  a temporary storage path)

4.	PARQUETPATHHDD: Path to the folder where Parquet files are stored on HDD. By default, this variable is empty (e.g.,  export PARQUETPATHHDD= $PWD'/databases/pyspark/parquet'  where $PWD is /hdd/path)

5.	PYSPARKUDFS: Path to the Pyspark UDFs (User Defined Functions) library (e.g., export PYSPARKUDFS=$PWD'/engines/pyspark/udfs').

6.	PYSPARKQUERIES: Path to the Pyspark SQL query files (e.g., export PYSPARKQUERIES=$PWD'/engines/pyspark/queries').

7.	PYSPARKSCRIPTS: Path to the folder containing Pyspark scripts (e.g.,export PYSPARKSCRIPTS=$PWD'/engines/pyspark/scripts').

8.	PYSPARKRESULTSPATH: Path to the folder where Pyspark query results or collectl are stored (e.g., export PYSPARKRESULTSPATH=$PWD'/results/logs/pyspark').



# 3. Install Required Ubuntu Packages:
"./automations/ubuntu_requirements.sh"

# 4. Install Python3 Dependencies:
"$PYTHONEXEC" -m pip install -r $PWD/automations/requirements.txt --upgrade  --user

# 5. Install, Set Up, and Deploy on Database Engines: : PostgreSQL, MonetDB, DuckDB, SQLite, PySpark
The "./automations/deploy_udfbench.sh" script handles the download, installation, deployment of experiments for the following database systems: PostgreSQL, MonetDB, DuckDB, SQLite, Pyspark. It also allows you to select parameters that are compatible with your system.


Command structure:
./automations/deploy_udfbench.sh <disk> <deploy> <download> <install> <system> [ <system2> ..]

Parameter Descriptions:
1.	Disk: Select a storage option:  ‘ssd’ ,  ‘mem’ (in-memory), or ‘hdd’  

3.	Deploy: Select ‘yes’ to deploy the databases, or ‘no’ to skip deployment.

4.	Download: Select ‘yes’ to download the datasets from Zenodo, or ‘no’ to skip downloading.

5.	Install: Select ‘yes’ to install the required database engines, or ‘no’ to skip installation.

6.	System:  Select ‘postgres’ for PostgreSQL, ‘monetdb’ for MonetDB, ‘duckdb’ for DuckDB, or ‘sqlite3’ for SQLite3 (including SQLite with virtual tables) to install, deploy, or run the experiment. You can choose one or more systems from the list.

Example Usage:
- Download the necessary datasets, install the systems, create and deploy the databases across all systems:
./automations/deploy_udfbench.sh ssd yes yes yes postgres monetdb duckdb sqlite sqlitevtab pyspark

- Run this once to download datasets from zenodo:
./automations/deploy_udfbench.sh ssd no yes no 

- Install database engines, create, deploy and load the databases:
./automations/deploy_udfbench.sh ssd yes no yes postgres monetdb duckdb sqlite sqlitevtab pyspark

- Create and deploy the databases to pre-installed data engines:
./automations/deploy_udfbench.sh ssd yes no no postgres monetdb duckdb sqlite sqlitevtab pyspark


# 6. Run Experiment on Database Engines: : PostgreSQL, MonetDB, DuckDB, SQLite, SQLitevtab, PySpark

The "./automations/run_udfbench.sh" script handles the execution of experiments for the following database systems: PostgreSQL, MonetDB, DuckDB, SQLite, SQLitevtab, Pyspark. It also allows you to select parameters that are compatible with your system.

The "./automations/run_udfbench.sh" script allows for fine tuned experimentation as the user may select specific queries, engines and setups to instantiate custom experiments with the UDFBench.   
To run experiment script (run_udfbench.sh),  several parameters that control the system configuration, experiment settings, resource monitoring should be specified. Below is  a description of  each parameter with examples (scenarios) to help you run the experiment.

Command structure:
 "./automations/run_udfbench.sh" $system $database  t$nthreads $cache $disk $collectl [$query1 $query2 .. ]

Parameter Descriptions:
1.	System: Select ‘postgres’ for PostgreSQL, ‘monetdb’ for MonetDB, ‘duckdb’ for DuckDB, ‘sqlite3’ for SQLite3, or ‘sqlitevtab’  for SQLite with virtual tables 
2.	Database :  Select ‘s’ for small, ‘m’ for medium, or ‘l’ for large
3.	Nthreads: Select ‘0’ to run the experiment with default threads, or select a number for the available cores on your system
4.	Cache: Select between `cold` (fresh start) or `hot` (preloaded) cache scenarios.
5.	Disk: Select between ‘ssd’, ‘mem’ (memory), or ‘hdd’ for storage
6.	Collectl: Select ‘true’ to monitor system resource usage (CPU, memory, disk, etc.) ,else ‘false’ to disable
7.	Query (Optional): Select one or more query numbers between 1 and 21. (By default, if no query number is provided, all queries (1-21) stored in the folder engines/"$system"/queries/ will be run)

Examples: 
Scenario 1 – Postgres with Large Dataset: The script will run all the SQL queries [1-21] in the folder engines/postgres/queries on the PostgreSQL system, using the large dataset, with default threads, cold cache, on SSD storage, without wordload, and without collectl 
(e.g.,  ./automations/run_udfbench.sh postgres l t0 cold ssd false)

Scenario 2 – Monetdb with Parallelism: The script will run Query 2 on MonetDB system,  using the medium dataset, with 2 thread, cold cache, on SSD storage, without wordload, and with collectl 
(e.g.,  ./automations/run_udfbench.sh monetdb m t2 cold ssd true 2)

Scenario 3 – DuckDB with Cache State: The script will run Queries 10-11 on the DuckDB system,  using the small dataset, with 1 thread, hot cache, on SSD storage, without wordload, and without collectl 
(e.g.,  ./automations/run_udfbench.sh duckdb s t1 hot ssd false 10 11)

Scenario 4a – Sqlite with Storage: The script will run Query 1 on SQLite system,  using the large dataset, with default thread, hot cache, on MEM storage, without wordload, and without collectl 
(e.g.,  ./automations/run_udfbench.sh sqlite3 l t0 hot mem false 1)

Scenario 4b – Sqlitevtab with Storage: The script will run Query 2 on SQLitevtab system,  using the large dataset, with default thread, cold cache, on HDD storage, without wordload, and with collectl 
(e.g.,  ./automations/run_udfbench.sh sqlitevtab l t0 cold hdd true 2)

Scenario 6 – Monetdb with Resources: The script will run Queries 1- 7 on MonetDB system,  using the large dataset, with default threads, cold cache, on SSD storage, without wordload, and with collectl 
(e.g.,  ./automations/run_udfbench.sh monetdb l t0 cold ssd true 1 2 3 4 5 6 7)


# 7. Collect Experiment Results to a CSV file across all systems:

The "./collectl_results.sh" script collects execution time, CPU time, and resource usage data from all systems in the engines/ folder and stores it in a CSV file. 
The data is extracted from experiment log files and, if available, from collectl logs for resource monitoring. (e.g., ./collectl_results.sh $RESULTSPATH/results.csv)

Command structure:
./collectl_results.sh <resultscsvpath>

1. Resultscsvpath: Is the path to the CSV file where the collected experiment results will be saved.
