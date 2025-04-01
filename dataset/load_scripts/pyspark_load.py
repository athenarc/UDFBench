import os
from pyspark.sql.types import *


def load_parquet_files(spark,folder_path,schemas):
    
    parquet_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".parquet"):
                parquet_files.append(os.path.join(root, file))



    if not parquet_files:
        print("No parquet files is this folder")
        return

    list_names = ["artifacts","artifact_citations", "projects", "projects_artifacts","artifact_authorlists","artifact_abstracts", "artifact_authors","views_stats"]
    for file in parquet_files:
        table_name = os.path.basename(file).replace(".parquet", "")

        if table_name in list_names:
            _schema = schemas.get(f"{table_name}_schema")

            df = spark.read.parquet(file, schema=_schema)  

            if table_name == "artifacts":
                df = df.toDF(*["id","title","publisher","journal","date","year","access_mode","embargo_end_date", "delayed", "authors", \
                "source", "abstract", "type", "peer_reviewed", "green","gold"])
            elif table_name == "projects":
                df = df.toDF(*["id","acronym","title","funder","fundingstring","funding_lvl0","funding_lvl1","funding_lvl2","ec39", "type", "startdate", \
                "enddate", "start_year", "end_year", "duration", "haspubs","numpubs","daysforlastpub","delayedpubs","callidentifier","code","totalcost","fundedamount","currency"])
            elif table_name == "projects_artifacts":
                df = df.toDF(*["projectid","artifactid","provenance"])
            elif table_name == "artifact_authorlists":
                df = df.toDF(*["artifactid","authorlist"])
            elif table_name == "artifact_citations":
                df = df.toDF(*["artifactid","target","citcount"])    
            elif table_name == "artifact_abstracts":
                df = df.toDF(*["artifactid","abstract"])
            elif table_name == "artifact_authors":
                df = df.toDF(*["artifactid","affiliation","fullname","name","surname","rank","authorid"])
            elif table_name == "views_stats":
                df = df.toDF(*["date","artifactid","source","repository_id","count"])
            else:
                continue
            
            df.createOrReplaceTempView(table_name)
