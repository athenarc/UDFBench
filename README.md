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

## Detailed info for queries and UDFs

### Query List  

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


### UDF List


| ID   | Name            | Description                                                                                                                                  | Type  | #Inputs | Input Type | #Outputs | Output Type | Pipeline | Blocking | Parallelizable | Side Effect | State | Languages | Cost       |
|------|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------|-------|---------|------------|----------|-------------|----------|----------|----------------|-------------|-------|-----------|------------|
| **Scalar UDF**                                                                                                                |
| U1   | Addnoise        | Adds Gaussian noise to a value and returns a float                                                                                         | S-1   | 1       | numeric    | 1        | float       | x        |          | x              |             |       |           | O(n)       |
| U2   | Clean           | Performs a data cleaning task on the string tokens of a JSON list                                                                          | S-1   | 1       | string     | 1        | string      | x        |          | x              |             | x     |           | O(n)       |
| U3   | Cleandate       | Reads a date and converts it to a common format (if needed) and handles problem dates                                                      | S-1   | 1       | string     | 1        | string      | x        |          | x              |             | x     |           | O(n)       |
| U4   | Converttoeuro   | Converts currency to euro, returns a float                                                                                                | S-1   | 1       | numeric    | 1        | float       | x        |          | x              |             |       |           | O(n)       |
| U5   | Extractclass    | Extracts class from a string with format `funder::class::projectid`                                                                         | S-1   | 1       | string     | 1        | string      | x        |          | x              |             |       |           | O(n)       |
| U6   | Extractcode     | Extracts project ID from a structured string containing the funder's ID, funding class, and project ID                                     | S-1   | 1       | string     | 1        | string      | x        |          | x              |             | x     |           | O(n)       |
| U7   | Extractday      | Reads a date (as a string) and extracts an integer with the day                                                                            | S-1   | 1       | string     | 1        | int         | x        |          | x              |             | x     |           | O(n)       |
| U8   | Extractfunder   | Extracts funder from a string with format `funder::class::projectid`                                                                        | S-1   | 1       | string     | 1        | string      | x        |          | x              |             |       |           | O(n)       |
| U9   | Extractid       | Extracts project ID from a string with format `funder::class::projectid`                                                                   | S-1   | 1       | string     | 1        | string      | x        |          | x              |             |       |           | O(n)       |
| U10  | Extractmonth    | Reads a date (as a string) and extracts an integer with the month                                                                          | S-1   | 1       | string     | 1        | int         | x        |          | x              |             | x     |           | O(n)       |
| U11  | Extractprojectid | Processes a text snippet and extracts a 6-digit project identifier                                                                        | S-1   | 1       | string     | 1        | string      | x        |          | x              |             | x     |           | O(n)       |
| U12  | Extractyear     | Reads a date (as a string) and extracts an integer with the year                                                                           | S-1   | 1       | string     | 1        | int         | x        |          | x              |             | x     |           | O(n)       |
| U13  | Filterstopwords | Removes stopwords from the input text                                                                                                      | S-1   | 1       | string     | 1        | string      | x        |          | x              |             | x     |           | O(n)       |
| U14  | Frequentterms   | Returns a space-separated text containing the most N% frequent tokens                                                                      | S-1   | 1       | string     | 1        | string      | x        |          | x              |             |       |           | O(n)       |
| U15  | Jaccard         | Processes two JSON lists with tokens and calculates the Jaccard distance                                                                   | S-1   | 2       | json       | 1        | float       | x        |          | x              |             |       |           | O(n*k)     |
| U16  | Jpack           | Converts a string to a JSON list with tokens                                                                                              | S-1   | P       | P          | 1        | json        | x        |          | x              |             |       |           | O(n*k)     |
| U17  | Jsoncount       | Returns the length of a JSON list                                                                                                         | S-1   | 1       | json       | 1        | int         | x        |          | x              |             |       |           | O(n)       |
| U18  | Jsort           | Processes a JSON list and returns a sorted JSON list                                                                                      | S-1   | 1       | string     | 1        | string      | x        |          | x              |             |       |           | O(n)       |
| U19  | Jsortvalues     | Processes a JSON list, if a value contains more than one token it sorts the value tokens                                                  | S-1   | 1       | string     | 1        | string      | x        |          | x              |             |       |           | O(n)       |
| U20  | Keywords        | Removes punctuation from text and returns the keywords in one string                                                                     | S-1   | 1       | string     | 1        | string      | x        |          | x              |             | x     |           | O(n)       |
| U21  | Log10           | Computes and returns the logarithm                                                                                                        | S-1   | 1       | numeric    | 1        | float       | x        |          | x              |             |       |           | O(n)       |
| U22  | Lower           | Converts the input text to lowercase                                                                                                      | S-1   | 1       | string     | 1        | string      | x        |          | x              |             |       |           | O(n)       |
| U23  | Removeshortterms | Processes a JSON list, if a value contains more than one token it removes tokens with length less than 3 chars                           | S-1   | 1       | string     | 1        | string      | x        |          | x              |             |       |           | O(n)       |
| U24  | Stem            | Stems the input text                                                                                                                     | S-1   | 1       | string     | 1        | string      | x        |          | x              |             | x     |           | O(n)       |
| **Aggregate UDF**                                                                                                              |
| U25  | Avg             | Computes average                                                                                                                         | A-2   | 1       | numeric    | 1        | float       | x        |          | x              |             |       |           | O(n)       |
| U26  | Count           | Computes count                                                                                                                           | A-2   | 1       | P          | 1        | int         | x        |          | x              |             |       |           | O(n)       |
| U27  | Max             | Computes max                                                                                                                             | A-2   | 1       | P          | 1        | int         | x        |          | x              |             | x     |           | O(n)       |
| U28  | Median          | Computes median                                                                                                                          | A-2   | 1       | numeric    | 1        | numeric     |          | x        |                |             |       |           | O(nlogn)   |
| **Table UDF**                                                                                                                 |
| U29  | Extractfromdate | Reads a date (as string), returns 3 column values (day, month, year)                                                       | T-3   | 1       | string     | 3        | rset        | x        |          | x              |             | x     |           | O(n)       |
| U30  | Jsonparse       | Parses a JSON dict per time and returns a tuple with the values                                                             | T-3   | 1       | json       | P        | P           | x        |          | x              |             |       |           | O(n*k)     |
| U31  | Combinations    | Reads a JSON list and returns a table with all the combinations per an integer parameter                                   | T-4   | 1       | json       | P        | P           | x        |          | x              |             |       |           | O(n*k^2)   |
| U32  | Extractkeys     | Selects keys from XML parsed input                                                                                          | T-2   | 1       | xml        | P        | rset        | x        |          | x              |             |       |           | O(n)       |
| U33  | Strsplitv       | Processes a string at a time and returns its tokens in separate rows                                                       | T-4   | 1       | string     | 1        | string      | x        |          | x              |             |       |           | O(n*k)     |
| U34  | Jgroupordered   | Performs a group by with an aggregate defined as a (named) parameter on a subquery ordered by an attribute                 | T-5   | P       | P          | P        | rset        | x        |          | x              |             |       |           | O(n)       |
| U35  | Kmeans          | Iterative version of the kmeans function                                                                                   | T-5   | P       | numeric    | P        | P           | x        | x        |                |             |       |           | O(n^2)     |
| U36  | Kmeans          | Clusters input data using recursive kmeans, returns cluster id and data point                                               | T-5   | P       | numeric    | P        | P           | x        | x        |                | x           |       |           | O(n^2)     |
| U37  | Xmlparse        | Parses XML input and returns a table                                                                                       | T-5   | 1       | xml        | P        | P           | x        | x        |                |             |       |           | O(n)       |
| U38  | Pivot           | Converts rows of a specific attribute (optionally grouped by another attribute) into columns, while applying an aggregation within the transformed dataset, and returns one tuple per input group | T-6   | P       | P          | P        | rset        | x        |          |                |             |       |           | O(n*k)     |
| U39  | Top             | Processes one group at a time and returns the top N values of an attribute                                                | T-7   | P       | P          | P        | rset        | x        |          |                |             |       |           | O(n*logk)  |
| U40  | File            | Parses an external file (CSV, XML, JSON) and returns a table                                                                | T-8   | 1       | string     | P        | P           | x        |          |                |             |       |           | O(n)       |
| U41  | Output          | Exports the results of a subquery to local storage in various formats and returns true if it succeeds                      | T-9   | P       | P          | 1        | bool        | x        |          | x              |             |       |           | O(n)       |
| U42  | getstats        | Inputs a table with integer values and returns the avg and the median for each input column                               | T-10  | P       | numeric    | P        | float       | x        | x        |                |             |       |           | O(n*logn)  |



--- 





Thank you for exploring the UDFBench!   
