# Before execute the exec file make the follow step:

# 1. Grant Execute Permissions to Bash Files:
find . -type f -name "*.sh" -exec  chmod +x {} \;

# 2. Update the configuration file as needed, then apply the changes with::
source $PWD'/utilities/config.sh'

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

- Run this once to download all necessary datasets:
./exec.sh ssd no no no yes 

- Install all systems, create and deploy the databases:
./exec.sh ssd no yes yes no postgres monetdb duckdb sqlite3

- Create and deploy the databases to an existing system:
./exec.sh ssd no yes no no  postgres monetdb duckdb sqlite3

- Run the experiment across all systems:
./exec.sh ssd yes no no no postgres monetdb duckdb sqlite3




