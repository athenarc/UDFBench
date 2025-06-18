# UDFBench Setup and Usage Guide

This repository provides scripts and configurations to install, configure, and run benchmarks across multiple database systems using UDFs.

---

## 🔧 Installation Steps

### 1. Grant Execute Permissions
```bash
find . -type f -name "*.sh" -exec chmod +x {} \;
```

### 2. Configure Environment
Update the configuration and apply the updates:
```bash
./automations/config_udfbench.sh
```
Set variables such as UDF paths, queries, database storage directories, etc., according to your system setup. Default config files are provided per engine.

<details>


#### Common Variables:
- `PYTHONEXEC`: Path to Python executable (e.g., `python3.10`)
- `EXTERNALPATHSSD`, `EXTERNALPATHMEM`, `EXTERNALPATHHDD`: Paths to CSV/XML/JSON files on different storage media.
- `DATASETSPATHSSD`, `DATASETSPATHMEM`, `DATASETSPATHHDD`: Paths to folders containing CSV and Parquet files for loading.

</details>

<details>


Includes detailed variable definitions for:

- PostgreSQL
- MonetDB
- DuckDB
- SQLite / SQLitevtab
- PySpark

</details>

---

### 3. Install Required Ubuntu Packages
```bash
./automations/ubuntu_requirements.sh
```

### 4. Install Python Dependencies
```bash
$PYTHONEXEC -m pip install -r $PWD/automations/requirements.txt --upgrade --user
```

---

## 🚀 Deploy Database Engines

Use the following script to deploy:
```bash
./automations/deploy_udfbench.sh <disk> <deploy> <download> <install> <system> [<system2>...]
```

### Parameters:
- `disk`: `ssd`, `mem`, or `hdd`
- `deploy`: `yes` or `no` to skip deployment
- `download`: `yes` or `no` to skip dataset download
- `install`: `yes` or `no` to skip data engine installation
- `system`: One or more of `postgres`, `monetdb`, `duckdb`, `sqlite`, `sqlitevtab`, `pyspark`

### Example:
```bash
./automations/deploy_udfbench.sh ssd yes yes yes postgres monetdb duckdb sqlite sqlitevtab pyspark
```

---

## 🧪 Run Experiments

Execute benchmarks using:
```bash
./automations/run_udfbench.sh <system> <dbsize> t<nthreads> <cache> <disk> <collectl> [<query1> <query2>...]
```

### Parameters:
- `system`: e.g., `postgres`, `monetdb`, `duckdb`, `sqlite3`, `sqlitevtab`
- `dbsize`: `s`, `m`, or `l`
- `nthreads`: e.g., `t0` (default), `t2` (two threads)
- `cache`: `hot` or `cold`
- `disk`: `ssd`, `mem`, `hdd`
- `collectl`: `true` or `false`
- `queries`: Optional list (1–21), If not selected, all queries will run. 

### Example Scenarios:

- **Run all Postgres queries with large dataset:**
  ```bash
  ./automations/run_udfbench.sh postgres l t0 cold ssd false
  ```

- **Run Query 2 on MonetDB with collectl:**
  ```bash
  ./automations/run_udfbench.sh monetdb m t2 cold ssd true 2
  ```

- **Run Queries 10–11 on DuckDB with hot cache:**
  ```bash
  ./automations/run_udfbench.sh duckdb s t1 hot ssd false 10 11
  ```

---

## 📊 Collect Results

Aggregate results into a CSV:
```bash
./collectl_results.sh <results_csv_path>
```

### Example:
```bash
./collectl_results.sh $RESULTSPATH/results.csv
```

---

## 📁 Folder Structure

```
.
├── automations/
│   ├── config_udfbench.sh
│   ├── deploy_udfbench.sh
│   ├── run_udfbench.sh
│   ├── ubuntu_requirements.sh
│   └── requirements.txt
├── databases/
├── dataset/
├── engines/
│   ├── postgres/
│   ├── monetdb/
│   ├── duckdb/
│   ├── sqlite/
│   ├── sqlitevtab/
│   └── pyspark/
├── results/
└── README.md
```

---

## 📌 Notes
- Ensure all storage paths (`/ssd`, `/dev/shm`, `/hdd`) exist and have read/write access.
- The `collectl` tool is used for fine-grained resource monitoring.
- UDF support varies per system—ensure each engine supports the desired operations.
