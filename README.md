# UDF Benchmark  

Welcome to the **UDF Benchmark** repository! This benchmark provides datasets, queries, and UDF implementations to evaluate the performance of User-Defined Functions across multiple database engines.  

Datasets are hosted on **[Zenodo](https://zenodo.org/records/14260428)** for easy access.  

---

## Datasets  

For easy deployment one can use the embedeed tiny dataset that is available in the `dataset` folder. For large scale experiments, one needs to download the files from Zenodo.

Three dataset sizes are available to suit different benchmarking needs:  

- **Small**  
- **Medium**  
- **Large**  

Each dataset consists of **10 CSV files** with the same schema:  


<img src="https://github.com/johnfouf/udfbench/blob/main/figs/schema.png" alt="Dataset Schema" width="600px">

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

##  How to Use  

For installation and execution instructions, please refer to the **[README.txt](README.txt)** file in the repository.  

---



Thank you for exploring the UDFBench!   
