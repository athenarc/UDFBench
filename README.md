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

## Query Descriptions  

**Q1 - Date Extraction with Scalar UDFs**  
- **Description**: Extract the year, month, and day from a date using three scalar UDFs.  
- **Input**: 1 string.  
- **Output**: 3 integer values.  

**Q2 - Date Extraction with Table UDF**  
- **Description**: Extract the year, month, and day from a date using a single table-returning UDF.  
- **Input**: 1 string column.  
- **Output**: 3 integer columns.  

**Q3 - Multi-language Scalar UDFs**  
- **Description**: Extract the year, month, and day from a date using scalar UDFs implemented in different languages.  
- **Input**: 1 string.  
- **Output**: 3 integer values.  

**Q4 - Average and Median with Aggregate UDFs**  
- **Description**: Compute the average and median author count per artifact using two aggregate UDFs.  
- **Input**: 1 integer.  
- **Output**: 2 float values.  

**Q5 - Aggregate Calculations with Table UDF**  
- **Description**: Compute the average and median author count per artifact using a single table-returning UDF.  
- **Input**: 1 integer.  
- **Output**: 2 float values.  

**Q6 - File Format Conversion**  
- **Description**: Convert and union two disk files (XML and JSON formats) into a single CSV file.  
- **Input**: 2 file paths.  
- **Output**: 1 CSV file.  

**Q7 - JSON File Analysis**  
- **Description**: Analyze a JSON file with publication metadata to compute the average citation and author counts.  
- **Input**: 1 file path.  
- **Output**: 2 float values.  

**Q8 - Publication Metadata Analysis**  
- **Description**: Analyze publication metadata from two tables (author lists and citations) to compute the average citation and author counts.  
- **Input**: 2 tables.  
- **Output**: 2 float values.  

**Q9 - Author Pair Counting**  
- **Description**: Clean author list data and count all possible author pairs for publications with fewer than 50 authors.  
- **Input**: 1 table.  
- **Output**: 1 integer value.  

**Q10 - Iterative k-Means Clustering**  
- **Description**: Perform iterative k-means clustering on publications grouped by type, based on funding amounts accessed through funding projects.  
- **Input**: 2 tables.  
- **Output**: 3 values (1 string, 1 integer, 1 float).  

**Q11 - Recursive k-Means Clustering**  
- **Description**: Perform recursive k-means clustering on publications grouped by type, based on funding amounts accessed through funding projects.  
- **Input**: 2 tables.  
- **Output**: 3 values (1 string, 1 integer, 1 float).  

**Q12 - Noisy Artifact Rankings**  
- **Description**: Return the 10 most-viewed artifacts from the past year, adding Gaussian noise to the counts.  
- **Input**: 1 table.  
- **Output**: 1 string, 1 float.  

**Q13 - JSON Link Extraction**  
- **Description**: Extract links between publications and projects from an external JSON file.  
- **Input**: 1 file.  
- **Output**: 2 string values.  

**Q14 - Recent Author Affiliations**  
- **Description**: Return the most recent affiliation of the first author for publications funded by the European Commission.  
- **Input**: 4 tables.  
- **Output**: 2 string values.  

**Q15 - XML Link Extraction**  
- **Description**: Extract links between publications and projects from an external XML file, excluding links that already exist in the database.  
- **Input**: 1 file.  
- **Output**: 2 string values.  

**Q16 - Author Collaboration Analysis**  
- **Description**: Analyze author collaborations within projects by computing:  
  - Author pairs collaborating during the project.  
  - Author pairs collaborating before the project.  
  - Author pairs collaborating after the project.  
- **Input**: 4 tables.  
- **Output**: 3 string columns and 3 integer columns.  

**Q17 - TF/IDF Computation**  
- **Description**: Compute the term frequency-inverse document frequency (TF/IDF) for each term in artifact abstracts.  
- **Input**: 1 table.  
- **Output**: 2 string values.  

**Q18 - Jaccard Similarity**  
- **Description**: Compute Jaccard similarity between document abstracts from two external files and return the top 5 similar documents per source document.  
- **Input**: 2 files.  
- **Output**: 2 strings, 1 float.  

**Q19 - Project Artifact Linking**  
- **Description**: Return the pivoted count of links to artifacts of different types for each project.  
- **Input**: 2 tables.  
- **Output**: 1 string, 4 integers.  

**Q20 - Date Cleaning and Updating**  
- **Description**: Update artifact table dates after cleaning.  
- **Input**: 1 table.  
- **Output**: Updated table.  

**Q21 - JSON Link Insertion**  
- **Description**: Extract links between publications and projects from a JSON file and insert them into the `projects_artifacts` table.  
- **Input**: 1 file.  
- **Output**: Updated table.  

##  How to Use  

For installation and execution instructions, please refer to the **[README.txt](README.txt)** file in the repository.  

---



Thank you for exploring the UDFBench!   
