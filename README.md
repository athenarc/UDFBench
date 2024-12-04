# UDFBench

Welcome to the **UDFBench** repository! This benchmark provides datasets, queries, and UDF implementations to evaluate the performance of User-Defined Functions across multiple database engines.  

Datasets are hosted on **[Zenodo](https://zenodo.org/records/14260428)** for easy access.  

---

## Datasets  

For easy deployment one can use the embedeed tiny dataset that is available in the `dataset` folder. For large scale experiments, one needs to download the files from Zenodo.

Three dataset sizes are available to suit different benchmarking needs:  

- **Small**  
- **Medium**  
- **Large**  

Each dataset consists of **10 CSV files** with the same schema:  


<img src="https://github.com/johnfouf/udfbench/blob/main/figs/schema.png" alt="Dataset Schema" width="1000px">

Additionally, external files used in queries are available in the same Zenodo repository.  

---

## Queries  

This benchmark includes:  

- **21 queries** implemented for four database engines:  
  - **MonetDB**  
  - **PostgreSQL**  
  - **DuckDB**  
  - **SQLite**  

You can find the queries organized by engine in the `queries` folder.  

---

## UDFs  

A comprehensive suite of **42 UDFs** is included, categorized as follows:  

- **24 Scalar UDFs**  
- **4 Aggregate UDFs**  
- **14 Table UDFs**, covering various subtypes  

The UDFs are implemented for all supported engines and are organized by type and engine in the `udfs` folder.  

---

## What Experiments Does UDFBench Offer?  

UDFBench provides a flexible framework for running experiments on various database engines. Users can perform comprehensive evaluations using the available **queries** and **UDFs** in their respective directories, with the ability to configure the following settings:  

1. **Dataset Size**: Choose between `small`, `medium`, or `large` datasets to match your benchmarking requirements.  
2. **Threading**: Control the number of threads to run, allowing for parallelism testing.  
3. **Cache State**: Select between `cold` (fresh start) or `hot` (preloaded) cache scenarios.  
4. **Storage Medium**: Test performance on different storage types:  
   - **SSD**  
   - **HDD**  
   - **Memory**  
5. **Workload Execution**: Execute multiple queries in sequence to simulate real-world workloads.  
6. **Resource Utilization Monitoring**:  
   - Optionally run **[collectl](https://collectl.sourceforge.net/)** to monitor system resource usage (CPU, memory, disk, etc.).  
   - Store the results for post-experiment analysis.  

These customizable settings enable users to tailor experiments to specific performance scenarios, providing valuable insights into UDF and query performance.  


##  How to Use  

For installation and execution instructions, please refer to the **[README.txt](README.txt)** file in the repository.  

---



Thank you for exploring the UDFBench!   
