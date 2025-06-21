import duckdb
from duckdb.typing import *
import sys
import numpy.core.multiarray
import re
import os
import pyarrow as pa
import pandas as pd
import numpy as np
import time
import json
import nltk
import math
import heapq
from collections import Counter
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords
import itertools

from sklearn.cluster import KMeans

from itertools import combinations
from itertools import product
import warnings
warnings.filterwarnings("ignore")

from threading import Thread, current_thread
import random

def createfunctions(con,UDFs,UDAFs,UDTFs):

    try:
        # Scalar UDFs
        con.create_function('addnoise', UDFs.addnoise)
        con.create_function('clean', UDFs.clean, [VARCHAR], VARCHAR)
        con.create_function('cleandate', UDFs.cleandate, [VARCHAR], VARCHAR)
        con.create_function('converttoeuro', UDFs.converttoeuro, [DOUBLE,VARCHAR],DOUBLE )
        con.create_function('extractclass', UDFs.extractclass, [VARCHAR], VARCHAR)
        con.create_function('extractcode', UDFs.extractcode, [VARCHAR], VARCHAR)
        con.create_function('extractday', UDFs.extractday, [VARCHAR], BIGINT)
        con.create_function('extractfunder', UDFs.extractfunder, [VARCHAR], VARCHAR)
        con.create_function('extractid', UDFs.extractid, [VARCHAR], VARCHAR)
        con.create_function('extractmonth', UDFs.extractmonth, [VARCHAR], BIGINT)
        con.create_function('extractprojectid', UDFs.extractprojectid, [VARCHAR], VARCHAR)
        con.create_function('extractyear', UDFs.extractyear, [VARCHAR], BIGINT)
        con.create_function('filterstopwords', UDFs.filterstopwords, [VARCHAR], VARCHAR)
        con.create_function('frequentterms', UDFs.frequentterms, [VARCHAR,BIGINT],VARCHAR )
        con.create_function('jaccard_udf', UDFs.jaccard, [VARCHAR,VARCHAR],DOUBLE )
        con.create_function('jpack', UDFs.jpack, [VARCHAR],VARCHAR )
        con.create_function('jsoncount', UDFs.jsoncount, [VARCHAR], BIGINT)
        con.create_function('jsonparse_q14', UDFs.jsonparse, [VARCHAR,VARCHAR], VARCHAR)
        con.create_function('jsort', UDFs.jsort, [VARCHAR],VARCHAR )
        con.create_function('jsortvalues', UDFs.jsortvalues, [VARCHAR],VARCHAR )
        con.create_function('keywords', UDFs.keywords, [VARCHAR], VARCHAR)
        con.create_function('log_10', UDFs.log_10, [DOUBLE], DOUBLE)
        con.create_function('lowerize', UDFs.lowerize, [VARCHAR], VARCHAR)
        con.create_function('removeshortterms', UDFs.removeshortterms, [VARCHAR], VARCHAR)
        con.create_function('stem', UDFs.stem, [VARCHAR], VARCHAR)

        # Aggregate UDFs 
        con.create_function('aggregate_avg', UDAFs.aggregate_avg)
        aggavg_type = con.struct_type({'grp': VARCHAR,'mean': VARCHAR})
        con.create_function('aggregate_avg_v2',UDAFs.aggregate_avg_v2,None,con.list_type(aggavg_type) )
       
        aggcount_type = con.struct_type({'grp': VARCHAR,'count': VARCHAR})
        con.create_function('aggregate_count', UDAFs.aggregate_count)
        con.create_function('aggregate_count_v2', UDAFs.aggregate_count_v2 ,None,con.list_type(aggcount_type))

        aggmax_type = con.struct_type({'grp': VARCHAR,'max': VARCHAR})
        con.create_function('aggregate_max', UDAFs.aggregate_max,None,con.list_type(aggmax_type) )
        con.create_function('aggregate_max_v2', UDAFs.aggregate_max_v2 )

        aggmedian_type = con.struct_type({'grp': VARCHAR,'median': VARCHAR})
        con.create_function('aggregate_median', UDAFs.aggregate_median )
        con.create_function('aggregate_median_v2', UDAFs.aggregate_median_v2 ,None,con.list_type(aggmedian_type))

        # Table UDFs

        date_type = con.struct_type({'year': DOUBLE, 'month': DOUBLE, 'day': DOUBLE})
        con.create_function('extractfromdate', UDTFs.extractfromdate,[VARCHAR],date_type,type='arrow')


        jsonparse_type = con.struct_type({'publicationdoi': VARCHAR, 'fundinginfo': VARCHAR})
        con.create_function('jsonparse', UDTFs.jsonparse, [VARCHAR,VARCHAR,VARCHAR], jsonparse_type)

        con.create_function('combinations', UDTFs.combinations, [VARCHAR,BIGINT] ,con.list_type(VARCHAR),type='arrow')


        extractkeys_type = con.struct_type({'key1': VARCHAR, 'key2': VARCHAR})
        con.create_function('extractkeys', UDTFs.extractkeys, [VARCHAR,VARCHAR,VARCHAR], extractkeys_type, type='arrow')
        
        strsplitv_type = con.struct_type({'term': con.list_type(VARCHAR)})
        con.create_function('strsplitv', UDTFs.strsplitv, [VARCHAR] ,con.struct_type({'term': con.list_type(VARCHAR)}), type='arrow')

        jgroup_type = con.struct_type({'docid': VARCHAR,'jcount':BIGINT,'term':VARCHAR,'tf':DOUBLE})

        con.create_function('JGROUPORDERED', UDTFs.jgroupordered, [VARCHAR,VARCHAR,VARCHAR], con.list_type(jgroup_type),type='arrow')

        kmeans_type = con.struct_type({'cluster_id': BIGINT, 'fundedamount': DOUBLE,'id': VARCHAR, 'type': VARCHAR})
        con.create_function('kmeans_iterative', UDTFs.kmeans_iterative,[VARCHAR,BIGINT,VARCHAR,VARCHAR,VARCHAR],con.list_type(kmeans_type),type='arrow')
        con.create_function('kmeans_recursive', UDTFs.kmeans_recursive,[VARCHAR,BIGINT,VARCHAR,VARCHAR,VARCHAR],con.list_type(kmeans_type),type='arrow')
        
        con.create_function('xmlparser', UDTFs.xmlparser, [VARCHAR,VARCHAR], con.list_type(VARCHAR), type='arrow')

        pivot_type = con.struct_type({'_pid':VARCHAR,'dataset': BIGINT,'other':BIGINT,'publication':BIGINT,'software':BIGINT})
        con.create_function('pivot_udf', UDTFs.pivot, [VARCHAR,VARCHAR,VARCHAR,VARCHAR],  con.list_type(pivot_type),type='arrow')

        top_type = con.struct_type({'arxivid':VARCHAR,'pubmedid':VARCHAR,'similarity':DOUBLE})
        con.create_function('aggregate_top', UDTFs.aggregate_top, [VARCHAR,VARCHAR,VARCHAR,BIGINT],  con.list_type(top_type), type='arrow')

        con.create_function('file', UDTFs.file, [VARCHAR,VARCHAR], con.list_type(VARCHAR), type='arrow')

        file_type_q6 = con.struct_type({'doi': VARCHAR,'amount':VARCHAR,'totalpubs':VARCHAR,'sdate':VARCHAR})
        con.create_function('file_q6', UDTFs.file,None,con.list_type(VARCHAR),type='arrow')

        file_type_q7 = con.struct_type({'authors':VARCHAR,'citations': VARCHAR,'id':VARCHAR})
        con.create_function('file_q7', UDTFs.file, [VARCHAR,VARCHAR], con.list_type(file_type_q7), type='arrow')
        
        file_type_text = con.struct_type({'line':VARCHAR})
        con.create_function('file_q13', UDTFs.file, [VARCHAR,VARCHAR], con.list_type(file_type_text), type='arrow')
        con.create_function('file_q15', UDTFs.file, [VARCHAR,VARCHAR], con.list_type(file_type_text), type='arrow')

        file_type_q18a = con.struct_type({'column0':VARCHAR,'column1':VARCHAR})
        file_type_q18b = con.struct_type({'abstract':VARCHAR,'id':VARCHAR})

        con.create_function('file_q18', UDTFs.file, [VARCHAR,VARCHAR], con.list_type(file_type_q18a), type='arrow')
        con.create_function('file_q18b', UDTFs.file, [VARCHAR,VARCHAR], con.list_type(file_type_q18b), type='arrow')

        con.create_function('output', UDTFs.output, type='arrow')
        con.create_function('getstats', UDTFs.getstats,None,con.struct_type({'avg':DOUBLE,'median':DOUBLE}), type='arrow')
        return True
    except:
        return False



def checkforexternals(filename):
    try:
        with open(filename, 'r') as query:
            sqlFile = query.read()
            if 'file' in sqlFile:
                return True
            else:
                return False

    except:
        print("File not found. Please check the file path.")
        return False


def executeScriptsFromFile(filename, conn,output=False):
    try:
        with open(filename, 'r') as query:
            sqlFile = query.read()

        if sqlFile.count(';') >1:
            sqlCommands = re.split(r'(?<=;)', sqlFile)
            # print(sqlCommands)
            for command in sqlCommands:
                if command:
                    if command.strip('\n')[0]=='-':
                        continue
                    try:
                        res = conn.execute(command).fetchdf()
                        if output:
                            print(res)
                    except:
                        print("Command skipped.")
        else:
            try:

                res = conn.execute(sqlFile).fetchdf()
        

                if output:
                    # pd.set_option("display.max_rows", None)
                    print(res)
            except:        
                print("Command skipped.")
    except FileNotFoundError:
        print("Wrong arguments. Please check the file path.")
        sys.exit(2)
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(2)

if __name__ == "__main__":
    import argparse

    import sys
    import os
    import time

    start = time.time()
    startpt = time.process_time()

    parser = argparse.ArgumentParser(description='Run Duckdb UDF benchmarks')
    parser.add_argument('--createdb', help='Create the Duckdb database', action='store_true')
    parser.add_argument('--profiling', help='Enable profiling', action='store_true')
    parser.add_argument('--duckdb-cli', help='Path to the Duckdb cli')
    parser.add_argument('--nthreads', help='Number of threads')
    parser.add_argument('--duckdb-schema', help='Path to the Duckdb schema')
    parser.add_argument('--duckdb-loads', help='Path to the Duckdb loads')
    parser.add_argument('--duckdb-csvs', help='Path to the Duckdb csvs')
    parser.add_argument('--duckdb-external', help='Path to the external files')
    parser.add_argument('--duckdb-sql', help='Path to the Duckdb sql query')
    parser.add_argument('--duckdb-dbfile', help='Path to the Duckdb database file')
    parser.add_argument('--duckdb-udfs', help='Path to the Duckdb UDFs library')
    parser.add_argument('--print-results', help='Print the query results', action='store_true')

    args = parser.parse_args()
    run_duckdb = False
    print_results = False
    createdb = False
    profiling = False
    external_path = None

    if args.createdb:  
        if args.duckdb_cli and  args.duckdb_dbfile and args.duckdb_schema and args.duckdb_loads and args.duckdb_csvs:
            try:
                print('Creating DuckDB database ')
                DUCKDB_CLI = str(args.duckdb_cli)
                DATABASE_PATH  = str(args.duckdb_dbfile)
                DATABASE_SCHEMA = str(args.duckdb_schema)
                DATABASE_LOADS = str(args.duckdb_loads)
                DATABASE_CSVS = str(args.duckdb_csvs)
                os.system(f"""{DUCKDB_CLI} {DATABASE_PATH} < {DATABASE_SCHEMA}""")
                os.system(f"""cd {DATABASE_CSVS}; {DUCKDB_CLI} {DATABASE_PATH} < {DATABASE_LOADS}""")
            except FileNotFoundError:
                print("Wrong arguments. Please check the file path.")
                sys.exit(2)
            except Exception as e:
                print("An error occurred:", e)
                sys.exit(2)

        else:
            print("--duckdb-cli, --duckdb-dbfile, --duckdb-schmema, --duckdb-loads and --duckdb-csvs need to be specified together", file=sys.stderr)
            sys.exit(2)
    
    if args.duckdb_sql:

        if bool(args.duckdb_sql) != bool(args.duckdb_dbfile) or bool(args.duckdb_dbfile) != bool(args.duckdb_udfs):
            print("--duckdb-sql, --duckdb-dbfile, --duckdb-udfs need to be specified together", file=sys.stderr)
            sys.exit(2)


        if args.duckdb_dbfile and args.duckdb_udfs and args.duckdb_sql:
            DATABASE_PATH = str(args.duckdb_dbfile)
            UDFS_PATH = str(args.duckdb_udfs)
            QUERY_PATH = str(args.duckdb_sql)

            library_paths = [
            UDFS_PATH+'/aggregate',
            UDFS_PATH+'/scalar',
            UDFS_PATH+'/table',
            ]
            for path in library_paths:
                sys.path.append(path)
            
            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

            from  udfs.scalar import Scalar
            from  udfs.aggregate import Aggregate
            from  udfs.table import Table

            try:
                conn = duckdb.connect(database=DATABASE_PATH, read_only=False)
            except:
                print("Wrong arguments. Please check the database path.")
                sys.exit(2)

            run_duckdb = True
            if checkforexternals(QUERY_PATH):
                if args.duckdb_external:
                    if os.path.exists(args.duckdb_external):
                        external_path = str(args.duckdb_external)
                    else:
                        print("External directory does not exist")
                        sys.exit(2)


                else:
                    print("--duckdb-sql, --duckdb-dbfile, --duckdb-udfs and -duckdb-external need to be specified together", file=sys.stderr)
                    sys.exit(2)


            scalar = Scalar()
            tbl = Table(conn,external_path)
            agg = Aggregate(conn)

        if run_duckdb:
            if createfunctions(conn,scalar,agg,tbl):
                if args.print_results:
                    print_results = True


                if args.profiling:  
  
                    conn.execute("PRAGMA enable_profiling='json';")
                    conn.execute("PRAGMA profiling_mode = 'detailed';")
                    
                if args.nthreads:
                    try:
                        nthreads = int(args.nthreads)
                        conn.execute(f"PRAGMA threads={nthreads};")  

                    except:
                        print("Wrong arguments. Please provide a valid integer value for nthreads.")
                
                executeScriptsFromFile(QUERY_PATH, conn,print_results)
   
            else:
                print("Error creating UDFs")
                
            conn.close()


    end = time.time()
    endpt = time.process_time()
    print(f'Execution Time: {(end-start)*1000:.3f} ms\n')
    print(f'Process Time: {(endpt-startpt)*1000:.3f} ms\n')


    sys.exit(0)

