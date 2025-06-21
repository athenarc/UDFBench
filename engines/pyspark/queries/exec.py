

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import udtf,pandas_udf,PandasUDFType,udf
import importlib
import inspect

import sys
import re
import os
import pandas as pd
import numpy as np
import time
import json
import nltk
import math
import heapq
from collections import Counter

import itertools


from itertools import combinations
from itertools import product
import warnings
warnings.filterwarnings("ignore")

import random

def createfunctions(spark,UDFs,UDAFs,UDTFs):

    try:
        # Scalar UDFs

        spark.udf.register("addnoise", udf(UDFs["addnoise"].addnoise,  DoubleType()))
        spark.udf.register("clean", udf(UDFs["clean"].clean,  StringType()))
        spark.udf.register("cleandate",  udf(UDFs["cleandate"].cleandate,  StringType()))
        spark.udf.register("converttoeuro", udf(UDFs["converttoeuro"].converttoeuro,  DoubleType()))
        spark.udf.register("extractclass", udf(UDFs["extractclass"].extractclass,  StringType()))
        spark.udf.register("extractcode", udf(UDFs["extractcode"].extractcode,  StringType()))
        spark.udf.register("extractday",  udf(UDFs["extractday"].extractday, IntegerType()))
        spark.udf.register("extractfunder",  udf(UDFs["extractfunder"].extractfunder,  StringType()))
        spark.udf.register("extractid",  udf(UDFs["extractid"].extractid,  StringType()))
        spark.udf.register("extractmonth", udf(UDFs["extractmonth"].extractmonth, IntegerType()))
        spark.udf.register("extractprojectid", udf(UDFs["extractprojectid"].extractprojectid, StringType()))
        spark.udf.register("extractyear", udf(UDFs["extractyear"].extractyear, IntegerType()))
        spark.udf.register("filterstopwords", udf(UDFs["filterstopwords"].filterstopwords, StringType()))
        spark.udf.register("frequentterms", udf(UDFs["frequentterms"].frequentterms, StringType()))
        spark.udf.register("jaccard", udf(UDFs["jaccard"].jaccard,  DoubleType()))
        spark.udf.register("jpack", udf(UDFs["jpack"].jpack, StringType()))
        spark.udf.register("jsoncount", udf(UDFs["jsoncount"].jsoncount,  LongType()))
        spark.udf.register("jsonparse_q14", udf(UDFs["jsonparse"].jsonparse,  StringType()))
        spark.udf.register("jsort", udf(UDFs["jsort"].jsort,  StringType()))
        spark.udf.register("jsortvalues", udf(UDFs["jsortvalues"].jsortvalues,  StringType()))
        spark.udf.register("keywords", udf(UDFs["keywords"].keywords,  StringType()))
        spark.udf.register("log_10", udf(UDFs["log_10"].log_10,  DoubleType()))
        spark.udf.register("lowerize", udf(UDFs["lowerize"].lowerize,  StringType()))
        spark.udf.register("removeshortterms", udf(UDFs["removeshortterms"].removeshortterms,  StringType()))
        spark.udf.register("stem", udf(UDFs["stem"].stem,  StringType()))
        
        spark.udf.registerJavaFunction("extractmonth_java", "com.example.udfs.ExtractmonthJava", IntegerType())
        spark.udf.registerJavaFunction("extractday_scala", "com.example.scalaudfs.ExtractdayScala", IntegerType())
    
        # Aggregate UDFs 

        spark.udf.register("aggregate_avg", UDAFs["aggregate_avg"].aggregate_avg)
        spark.udf.register("aggregate_count", UDAFs["aggregate_count"].aggregate_count)
        spark.udf.register("aggregate_max", UDAFs["aggregate_max"].aggregate_max)
        spark.udf.register("aggregate_median", UDAFs["aggregate_median"].aggregate_median)
 
        # Table UDFs

        spark.udtf.register("extractfromdate", UDTFs["extractfromdate"].ExtractFromDate)
        spark.udtf.register("jsonparse", UDTFs["jsonparse"].JsonParse)
        spark.udtf.register("combinations", UDTFs["combinations"].Combinations)
        spark.udtf.register("combinations_q16", UDTFs["combinations_q16"].Combinations_q16)
        spark.udtf.register("extractkeys", UDTFs["extractkeys"].Extractkeys)
        spark.udtf.register("xmlparser", UDTFs["xmlparser"].Xmlparser)
        spark.udtf.register("aggregate_top",UDTFs["aggregate_top"].AggregateTop)
        spark.udtf.register("file_q7", UDTFs["file_q7"].File_q7)
        spark.udtf.register("file_q13", UDTFs["file_q13"].File_q13)
        spark.udtf.register("file_q18", UDTFs["file_q18"].File_q18)
        return True
    except:
        return False





def executeScriptsFromFile(filename, conn,output=False):
    try:
        with open(filename, 'r') as query:
            sqlFile = query.read()

        if sqlFile.count(';') >1:
            sqlCommands = re.split(r'(?<=;)', sqlFile)
            for command in sqlCommands:
                if command:
                    if command.strip('\n')[0]=='-':
                        continue
                    try:
                        def proceess_row(df):
                            pass
                        res= spark.sql(command)
                        res.foreach(proceess_row)
                        if output:
                            print(res.show())
                    except:
                        print("Command skipped.")
        else:
            try:
                       
                def proceess_row(df):
                    pass
                res = spark.sql(sqlFile)
                res.foreach(proceess_row)
                if output:
                    print(res.show())

            except:        
                print("Command skipped.")
    except FileNotFoundError:
        print("Wrong arguments. Please check the file path.")
        sys.exit(2)
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(2)


def load_modules_from_folder(folder_path):
    modules = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and not filename.startswith("__"):

            file_path = os.path.join(folder_path, filename)
            module_name = filename[:-3]

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                modules[module_name] = module

    return modules

if __name__ == "__main__":
    import argparse

    import sys
    import os
    import time


    parser = argparse.ArgumentParser(description='Run PySpark UDF benchmarks')
    parser.add_argument('--pyspark-schema', help='Path to the PySpark schema')
    parser.add_argument('--pyspark-loads', help='Path to the PySpark loads')
    parser.add_argument('--pyspark-parquet', help='Path to the PySpark parquet')
    parser.add_argument('--pyspark-sql', help='Path to the PySpark sql query')
    parser.add_argument('--pyspark-udfs', help='Path to the PySpark UDFs library')
    parser.add_argument('--print-results', help='Print the query results', action='store_true')

    args = parser.parse_args()
    run_pyspark = False
    print_results = False
    
    if args.pyspark_sql:

        if args.pyspark_schema and args.pyspark_loads and args.pyspark_parquet:
            try:
                SCHEMA_PATH = str(args.pyspark_schema)
                LOADS_PATH = str(args.pyspark_loads)
                PARQUET_PATH = str(args.pyspark_parquet)
                
            except FileNotFoundError:
                print("Wrong arguments. Please check the file path.")
                sys.exit(2)
            except Exception as e:
                print("An error occurred:", e)
                sys.exit(2)

        else:
            print(" --pyspark-schmema, --pyspark-loads and --pyspark-parquet need to be specified together", file=sys.stderr)
            sys.exit(2)

        if bool(args.pyspark_sql) != bool(args.pyspark_loads) or bool(args.pyspark_sql) != bool(args.pyspark_udfs):
            print("--pyspark-sql, --pyspark-loads, --pyspark-udfs need to be specified together", file=sys.stderr)
            sys.exit(2)


        if args.pyspark_udfs and args.pyspark_sql:
            UDFS_PATH = str(args.pyspark_udfs)
            QUERY_PATH = str(args.pyspark_sql)

            library_paths = [
            UDFS_PATH+'/aggregate',
            UDFS_PATH+'/scalar',
            UDFS_PATH+'/table',
            SCHEMA_PATH,
            LOADS_PATH,
            ]
            for path in library_paths:
                sys.path.append(path)

            from pyspark_load import load_parquet_files
            from pyspark_schema import schemas

            try:
                spark = SparkSession.builder.appName("UDFBench").config("spark.jars", f"{UDFS_PATH}/scalar/extractday_scala/target/ScalaUDFjarfile.jar, {UDFS_PATH}/scalar/extractmonth_java/target/JavaUDFjarfile.jar").config("spark.driver.memory","58g").getOrCreate() 

  
                load_parquet_files(spark,PARQUET_PATH,schemas)
            except Exception as e:
                    print("An error occurred:", e)
                    sys.exit(2)



            run_pyspark = True

            UDFs=load_modules_from_folder(f"{UDFS_PATH}/scalar")
            UDAFs=load_modules_from_folder(f"{UDFS_PATH}/aggregate")
            UDTFs=load_modules_from_folder(f"{UDFS_PATH}/table")

        if run_pyspark:
            if createfunctions(spark,UDFs,UDAFs,UDTFs):
                if args.print_results:
                    print_results = True

                start = time.time()
                startpt = time.process_time()
                print("start execution")
                executeScriptsFromFile(QUERY_PATH, spark,print_results)
                end = time.time()
                endpt = time.process_time()
                print(f'Execution Time: {(end-start)*1000:.3f} ms\n')
                print(f'Process Time: {(endpt-startpt)*1000:.3f} ms\n')

            else:
                print("Error creating UDFs")

            spark.stop()
            spark.catalog.clearCache()




    sys.exit(0)

