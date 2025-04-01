# To install and experiment with the benchmark run the following steps:

# 1. Grant execute permissions to bash scripts, with the following command:
find . -type f -name "*.sh" -exec  chmod +x {} \;

# 2. Update the configuration file as needed, then apply the changes:
Before running the benchmark, or executing any of the  scripts, you need to configure a set of environment variables, such as UDFs, queries, executables, databases storage paths.
These variables should be updated based on your system’s set up and directory structure.
By default, the configure file (config.sh) is set up to create all the required systems from the beginning.

 Variables in the Configuration file common for all systems:
1.	PYTHONEXEC: Path to the Python executable, used for Python scripts (e.g., export PYTHONEXEC='python3.10' ).
2.	EXTERNALPATH: Path to the folder where the external data files (CSV, XML, JSON, etc.) are stored, which are required by some queries to run(e.g., export EXTERNALPATH=PWD'/dataset/externalfiles') 
3.	CSVSPATH: Path to the folder where the CSV files needed to  load data into the databases are stored(e.g., export CSVSPATH=$PWD'/dataset/csvs').

Variables in the Configuration file for PostgresSQL:
1.	PSQLPATH: Path to the PostgreSQL psql command-line (e.g., export PSQLPATH=$PWD'/databases/postgres/bin/psql').

2.	POSTGRESPATH: Path to the PostgreSQL database storage directory (e.g., export POSTGRESPATH=$PWD'/databases/postgres').

3.	PSQLSSDPORT:  Port for PostgreSQL database running on SSD storage (e.g. , export PSQLSSDPORT = “50007” where this port refers to /ssd/path).

4.	PSQLHDDPORT:   Port for PostgreSQL database running on HDD storage. By default, this variable is empty  (e.g. , export PSQLHDDPORT = “50009” where this port refers to /hdd/path).

5.	PSQLMEMPORT: Port for PostgreSQL database running in-memory. By default, this variable is empty  (e.g., /dev/shm). (e.g.  export PSQLMEMPORT=”50010” where this port refers to /dev/shm/path  a temporary storage path).

6.	PSQLUSER: PostgreSQL user name usually the system user (e.g.  export PSQLUSER=$USER).

7.	POSTGRESQUERIES: Path to the PostgreSQL SQL query files (e.g., export POSTGRESQUERIES=$PWD'/queries/postgres').


Variables in the Configuration file for MonetDB:
1.	MONETDBPATH: Path to the MonetDB mclient command-line(e.g., export MONETDBPATH=$PWD'/databases/monetdb/bin/mclient').

2.	MONETDBDIRPATH: Path to the MonetDB database storage directory (e.g., export MONETDBDIRPATH=$PWD'/databases/monetdb).

3.	MONETDBSSDPORT:  Port for MonetDB database running on SSD storage (e.g. , export MONETDBSSDPORT = “50007” where $MONETDBINSTANCE is /ssd/path).

4.	MONETDBHDDPORT:   Port for MonetDB database running on HDD storage. By default, this variable is empty (e.g. , export MONETDBHDDPORT= “50011” where MONETDBINSTANCE is /hdd/path).

5.	MONETDBMEMPORT: Port for MonetDB database running in-memory By default, this variable is empty (e.g.,  export MONETDBMEMPORT=”50012” where MONETDBINSTANCE is /dev/shm/path,  a temporary storage path).

6.	MONETDBBINPATH: Path to the MonetDB binary folder (e.g., export MONETDBBINPATH=$PWD'/databases/monetdb/bin/’).

7.	MONETDBQUERIES: Path to the MonetDB SQL query files (e.g., export MONETDBQUERIES =$PWD'/queries/monetdb).

8.	MONETDBINSTANCE: Path to a specific database instance within MonetDB. You can set this variable based on the specific storage type (SSD, HDD, or memory). By default, the database instance is located under the MONETDBDIRPATH directory (e.g., export MONETDBINSTANCE='udfbench').


Variables in the Configuration file for SQLite / SQLitevtab:
1.	SQLITEPATH: Path to the SQLite script script to run queries that only require scalar or aggregate UDFs (e.g., export SQLITEPATH=$PWD'/queries/sqlite/exec.py')

2.	SQLITEVTABPATH: Path to a custom SQLite virtual table (VTAB) script to run queries that require table UDFs. (e.g., export SQLITEVTABPATH=$PWD'/queries/sqlitevtab/mexec.py')

3.	SQLITEEXEC: The SQLite3 executable used to connect to SQLite databases directly from the terminal (e.g. export SQLITEEXEC='sqlite3').

4.	SQLITEDBSSDPATH:  Path to the SQLite databases stored on SSD (e.g. , export SQLITEDBSSDPATH = $PWD’ /databases/sqlite/’ where $PWD is /ssd/path)

5.	SQLITEDBMEMPATH:   Path to the SQLite databases stored in-memory (e.g. , export SQLITEDBMEMPATH $PWD’ /databases/sqlite/’ where $PWD is /dev/shm/path  a temporary storage path)

6.	SQLITEDBHDDPATH: Path to the SQLite databases stored on HDD . By default, this variable is empty (e.g.  export SQLITEDBHDDPATH =$PWD’ /databases/sqlite/’  where $PWD is /hdd/path)

7.	SQLITESCALAR: Path to the Scalar UDFs for SQLite (e.g., export SQLITESCALAR=$PWD'/udfs/scalar/sqlite').

8.	SQLITEAGGRS: Path to the Aggregate UDFs for SQLite (e.g., export SQLITEAGGRS=$PWD'/udfs/aggregate/sqlite').

9.	SQLITEVTABTABLES: Path to the Table UDFs for SQLite virtual table (VTAB)  (e.g., export SQLITEVTABTABLES=$PWD'/udfs/table/sqlitevtab').

10.	SQLITEQUERIES: Path to the SQLite SQL query files (e.g., export SQLITEQUERIES=$PWD'/queries/sqlite').

11.	SQLITEVTABQUERIES: Path to a custom SQLite virtual table (VTAB) SQL query files (e.g., export SQLITEVTABQUERIES=$PWD'/queries/sqlitevtab').

12.	SQLITEVTABFUNCTIONS: Path to the UDFs for SQLite virtual table (VTAB)  (e.g., export SQLITEVTABFUNCTIONS=$PWD'/queries/sqlitevtab/functions').

Variables in the Configuration file for DuckDB:
1.	DUCKDBEXEC: Path to the DuckDB executable (e.g., export  DUCKDBEXEC =$PWD'queries/duckdb/exec.py’)

2.	DUCKDBSSDPATH:  Path to the DuckDB databases stored on SSD (e.g., export DUCKDBSSDPATH= $PWD’ /databases/duckdb/’ where $PWD is /ssd/path)

3.	DUCKDBMEMPATH:   Path to the DuckDB databases stored in-memory. By default, this variable is empty (e.g., export DUCKDBMEMPATH = $PWD’ /databases/duckdb’ where $PWD is /dev/shm/path  a temporary storage path)

4.	DUCKDBHDDPATH: Path to the DuckDB databases stored on HDD. By default, this variable is empty (e.g.,  export DUCKDBHDDPATH== $PWD’ /databases/duckdb’  where $PWD is /hdd/path)

5.	DUCKDBUDFS: Path to the DuckDB UDFs (User Defined Functions) library (e.g., export  DUCKDBUDFS =$PWD'/udfs’).

6.	DUCKDBQUERIES: Path to the DuckDB SQL query files (e.g., export  DUCKDBQUERIES=$PWD'/queries/duckdb').

7.	DUCKDBCLI: Path to the DuckDB CLI (Command Line Interface) executable. The CLI is used to connect to the DuckDB  databases directly from the terminal (e.g., export DUCKDBCLI=$PWD'/databases/duckdb/cli/duckdb').

Variables in the Configuration file for PySpark:
1.	PYSPARKPATH: Path to the PySpark executable (e.g., export  PYSPARKPATH=$PWD'queries/pyspark/exec.py’).

2.	PARQUETPATH: Path to the folder where Parquet files are stored   (e.g., export PARQUETPATH=$PWD'/dataset/parquet').

3.	PYSPARKLOADS: Path to the PySpark Python file used for loading data  (e.g.,  export PYSPARKLOADS=$PWD'/dataset/load_scripts').

4.	PYSPARKSCHEMA: Path to the PySpark Python file that defines the schema for Parquet files  (e.g.,  export PYSPARKSCHEMA=$PWD'/schema')

5.	PYSPARKUDFS: Path to the Pyspark UDFs (User Defined Functions) library (e.g., export  PYSPARKUDFS =$PWD'/udfs’).

6.	PYSPARKQUERIES: Path to the Pyspark SQL query files (e.g., export  PYSPARKQUERIES=$PWD'/queries/pyspark').

7.	PYSPARK_DRIVER_PYTHON: Path to the Python 3 executable that PySpark should use for its driver program (e.g., export PYSPARK_DRIVER_PYTHON=$(which python3)).

8.	PYSPARK_PYTHON: Path to the Python 3 executable that PySpark should use for the executors (e.g., export PYSPARK_PYTHON=$(which python3)).


# 3. Install Required Ubuntu Packages:
"./utilities/README.Ubuntu.sh"

# 4. Install Python3 Dependencies:
"$PYTHONEXEC" -m pip install -r $PWD'/utilities/requirements.txt --upgrade  --user

# 5. Install, Set Up, and Run Experiment on Database Engines: : PostgreSQL, MonetDB, DuckDB, SQLite
The exec.sh script handles the download, installation, deployment, and execution of experiments for the following database systems: PostgreSQL, MonetDB, DuckDB, and SQLite. It also allows you to select parameters that are compatible with your system.

Command structure:
./exec.sh <disk> <runexp> <deploy> <download > < install > <system> [ <system2> ..]

Parameter Descriptions:
1.	Disk: Select a storage option:  ‘ssd’ ,  ‘mem’ (in-memory), or ‘hdd’  

2.	Runexp: Select ‘yes’ to run the experiment, or ‘no’ to skip it.

3.	Deploy: Select ‘yes’ to deploy the databases, or ‘no’ to skip deployment.

4.	Download: Select ‘yes’ to download the datasets from Zenodo, or ‘no’ to skip downloading.

5.	Install: Select ‘yes’ to install the required database engines, or ‘no’ to skip installation.

6.	System:  Select ‘postgres’ for PostgreSQL, ‘monetdb’ for MonetDB, ‘duckdb’ for DuckDB, or ‘sqlite3’ for SQLite3 (including SQLite with virtual tables) to install, deploy, or run the experiment. You can choose one or more systems from the list.

Example Usage:
- Download the necessary datasets, install the systems, create and deploy the databases, and run the experiment across all systems:
./exec.sh ssd yes yes yes yes postgres monetdb duckdb sqlite3

- Run this once to download datasets from zenodo:
./exec.sh ssd no no yes no 

- Install database engines, create, deploy and load the databases:
./exec.sh ssd no yes no yes postgres monetdb duckdb sqlite3

- Create and deploy the databases to pre-installed data engines:
./exec.sh ssd no yes no no  postgres monetdb duckdb sqlite3

- Run the whole benchmark across all engines:
./exec.sh ssd yes no no no postgres monetdb duckdb sqlite3


# 6. Execution of custom experiments 

While exec.sh script supports execution of the whole benchmark in default setups, 
utilities/runexperiment.sh allows for more fine tuned experimentation as the user may select specific queries, engines and setups to instantiate custom experiments with the UDFBench.   
To run experiment script (runexperiment.sh),  several parameters that control the system configuration, experiment settings, resource monitoring should be specified. Below is  a description of  each parameter with examples (scenarios) to help you run the experiment.

Command structure:
 $PWD'/utilities/runexperiment.sh' $system $database  t$nthreads $cache $disk $workload $collectl [$query1 $query2 .. ]

Parameter Descriptions:
1.	System: Select ‘postgres’ for PostgreSQL, ‘monetdb’ for MonetDB, ‘duckdb’ for DuckDB, ‘sqlite3’ for SQLite3, or ‘sqlitevtab’  for SQLite with virtual tables 
2.	Database :  Select ‘s’ for small, ‘m’ for medium, or ‘l’ for large
3.	Nthreads: Select ‘0’ to run the experiment with default threads, or select a number for the available cores on your system
4.	Cache: Select between `cold` (fresh start) or `hot` (preloaded) cache scenarios.
5.	Disk: Select between ‘ssd’, ‘mem’ (memory), or ‘hdd’ for storage
6.	Workload: Select ‘true’ to execute multiple queries to experiment with workload execution, else ‘false’ for individual queries
7.	Collectl: Select ‘true’ to monitor system resource usage (CPU, memory, disk, etc.) ,else ‘false’ to disable
8.	Query: Select one or more query numbers between 1 and 21.

Examples: 
Scenario 1 – Postgres with Large Dataset: The script will run Query 1 on PostgreSQL system, using the large dataset, with default threads, cold cache, on SSD storage, without wordload, and without collectl 
(e.g.,  $PWD'/utilities/runexperiment.sh' postgres l  t0 cold ssd false false 1)

Scenario 2 – Monetdb with Parallelism: The script will run Query 2 on MonetDB system,  using the medium dataset, with 2 thread, cold cache, on SSD storage, without wordload, and with collectl 
(e.g.,  $PWD'/utilities/runexperiment.sh' monetdb m t2 cold ssd false true 2)

Scenario 3 – DuckDB with Cache State: The script will run Queries 10-11 on the DuckDB system,  using the small dataset, with 1 thread, hot cache, on SSD storage, without wordload, and without collectl 
(e.g.,  $PWD'/utilities/runexperiment.sh' duckdb s t1  hot ssd false false 10 11)

Scenario 4a – Sqlite with Storage: The script will run Query 1 on SQLite system,  using the large dataset, with default thread, hot cache, on MEM storage, without wordload, and without collectl 
(e.g.,  $PWD'/utilities/runexperiment.sh' sqlite3 l t0  hot mem false false 1)

Scenario 4b – Sqlitevtab with Storage: The script will run Query 2 on SQLitevtab system,  using the large dataset, with default thread, cold cache, on HDD storage, without wordload, and with collectl 
(e.g.,  $PWD'/utilities/runexperiment.sh' sqlitevtab l t0  cold hdd false true 2)

Scenario 5 – Postgres with Workload: The script will run Queries 1 -5 on PostgreSQL system,  using the medium dataset, with default threads, cold cache, on SSD storage, with wordload, and without collectl 
(e.g.,  $PWD'/utilities/runexperiment.sh' postgres m  t0 cold ssd true false 1 2 3 4 5)

Scenario 6 – Monetdb with Resources: The script will run Queries 1- 7 on MonetDB system,  using the large dataset, with default threads, cold cache, on SSD storage, without wordload, and with collectl 
(e.g.,  $PWD'/utilities/runexperiment.sh' monetdb l  t0 cold ssd false true 1 2 3 4 5 6 7)


