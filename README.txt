# Before executing the exec file, follow these steps:

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

9.	SQLITEQUERIES: Path to the SQLite SQL query files (e.g., export SQLITEQUERIES=$PWD'/queries/sqlite').

10.	SQLITEVTABQUERIES: Path to a custom SQLite virtual table (VTAB) SQL query files (e.g., export SQLITEVTABQUERIES=$PWD'/queries/sqlitevtab').

Variables in the Configuration file for DuckDB:
1.	DUCKDBEXEC: Path to the DuckDB executable (e.g., export  DUCKDBEXEC =$PWD'queries/duckdb/exec.py’)

2.	DUCKDBSSDPATH:  Path to the DuckDB databases stored on SSD (e.g., export DUCKDBSSDPATH= $PWD’ /databases/duckdb/’ where $PWD is /ssd/path)

3.	DUCKDBMEMPATH:   Path to the DuckDB databases stored in-memory. By default, this variable is empty (e.g., export DUCKDBMEMPATH = $PWD’ /databases/duckdb’ where $PWD is /dev/shm/path  a temporary storage path)

4.	DUCKDBHDDPATH: Path to the DuckDB databases stored on HDD. By default, this variable is empty (e.g.,  export DUCKDBHDDPATH== $PWD’ /databases/duckdb’  where $PWD is /hdd/path)

5.	DUCKDBUDFS: Path to the DuckDB UDFs (User Defined Functions) library (e.g., export  DUCKDBUDFS =$PWD'/udfs’).

6.	DUCKDBQUERIES: Path to the DuckDB SQL query files (e.g., export  DUCKDBQUERIES=$PWD'/queries/duckdb').

7.	DUCKDBCLI: Path to the DuckDB CLI (Command Line Interface) executable. The CLI is used to connect to the DuckDB  databases directly from the terminal (e.g., export DUCKDBCLI=$PWD'/databases/duckdb/cli/duckdb').


How to set up Duckdb:
For this experiment, we used DuckDB v1.0.0. for both CLI and DuckDB library. The path for the CLI to create/deploy a new database should be specified. If you are using a different version, make sure the paths in your configuration file are set to the correct cli executable and database locations.

Duckdb execution file parameters to run a query :
--duckdb-dbfile : Path to the Duckdb database file (*Required with file path)
--duckdb-udfs : Path to the Duckdb UDFs library (*Required with folder path)
--duckdb-sql : Path to the Duckdb SQL query (*Required with file path)
--duckdb-external: Path to external files (*Required  with folder path, for queries with external files)
--print-results : Prints the query results in a DataFrame format(Optional)
--profiling: Enable profiling (Optional)
--nthreads: Set number of threads (Optional)

Example command to run a query:
"$PYTHONEXEC" "$DUCKDBEXEC" --duckdb-dbfile "$DUCKDBSSDPATH/large.db  \
          --duckdb-udfs "$DUCKDBUDFS" --duckdb-external "$EXTERNALPATH/large.db" \
          --duckdb-sql "$DUCKDBQUERIES/q1.sql"  --print-results –nthreads 1
The above example sets the number of threads to 1, runs query 1 for the large database, and prints the results.

To create and deploy the databases from scratch, use these parameters:
--createdb: Flag to indicate that a new database should be created. (*Required flag)
--duckdb-dbfile : Path to the database file where the new database will be created (*Required with a file path)
--duckdb-schema: Path to the schema SQL file that defines the structure of your database  (*Required with a file path)
--duckdb-cli : Path to the DuckDB CLI executable. (*Required with a file path)
--duckdb-loads: Path to the load SQL file (*Required with a file path)
--duckdb-csvs: Path to the folder containing the CSV files to be loaded into the database (*Required with a folder path referenced in the load SQL file)

Example command to create/deploy a database:
"$PYTHONEXEC" "$DUCKDBEXEC" –createdb –duckdb-cli $DUCKDBCLI \
         --duckdb-dbfile "$DUCKDBSSDPATH/large.db" --duckdb-schema $PWD’/schema/duckdb_schema.sql’ \
         --duckdb-loads $PWD’/dataset/load_scripts/duckdb_load.sql’ --duckdb-csvs $CSVSPATH/large/
The above example  will create a new database (large.db) and load data from the CSV files for the large dataset.


.....




# 3. Install Required Ubuntu Packages:
"./utilities/README.Ubuntu.sh"

# 4. Install Python3 Dependencies:
"$PYTHONEXEC" -m pip install -r $PWD'/utilities/requirements.txt --upgrade  --user

# Install DuckDB, PostGreSQL,Sqlite and Monetdb System

<!-- ./exec.sh <disk> <runexp> <deploy> <install> <download> <system> [ <system2> ..]
    for <disk> options are ssh, hdd or mem  (Choose the disk type)
    for <runexp> options are yes or no (Run the experiment or not)
    for <deploy> options are yes or no (Deploy the databases or not)
    for <install> options are yes or no (Install dependencies or not)
    for <download> options are yes or no  (Download  datasets or not)
    for <system> options are postgres, monetdb and duckdb  (Choose one or more systems)-->

Example Usage:
- Download the necessary datasets, install the systems, create and deploy the databases, and run the experiment across all systems:
./exec.sh ssd yes yes yes yes postgres monetdb duckdb sqlite3

- Run this once to download datasets from zenodo:
./exec.sh ssd no no no yes 

- Install database engines, create, deploy and load the databases:
./exec.sh ssd no yes yes no postgres monetdb duckdb sqlite3

- Create and deploy the databases to pre-installed data engines:
./exec.sh ssd no yes no no  postgres monetdb duckdb sqlite3

- Run the whole benchmark across all engines:
./exec.sh ssd yes no no no postgres monetdb duckdb sqlite3





