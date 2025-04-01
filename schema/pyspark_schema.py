from pyspark.sql.types import *

schemas = {
"artifacts_schema" : StructType([
    StructField("id", StringType(), nullable=True),
    StructField("title", StringType()),
    StructField("publisher", StringType()),
    StructField("journal", StringType()),
    StructField("date", StringType()),
    StructField("year", IntegerType()),
    StructField("access_mode", StringType()),
    StructField("embargo_end_date", StringType()),
    StructField("delayed", BooleanType()),
    StructField("authors", IntegerType()),
    StructField("source", StringType()),
    StructField("abstract", BooleanType()),
    StructField("type", StringType()),
    StructField("peer_reviewed", BooleanType()),
    StructField("green", BooleanType()),
    StructField("gold", BooleanType())
]),

"artifact_charges_schema" : StructType([
    StructField("artifactid", StringType(),nullable=True),
    StructField("amount", FloatType()),
    StructField("currency", StringType())
]),

"artifact_abstracts_schema" : StructType([
    StructField("artifactid", StringType(),nullable=True),
    StructField("abstract", StringType())
]),

"artifact_authorlists_schema" : StructType([
    StructField("artifactid", StringType(),nullable=True),
    StructField("authorlist", StringType())
]),

"artifact_authors_schema": StructType([
    StructField("artifactid", StringType(),nullable=True),
    StructField("affiliation" , StringType()),
    StructField("fullname" , StringType()),
    StructField("name", StringType()),
    StructField("surname" , StringType()), 
    StructField("rank",     LongType()), 
    StructField("authorid" , StringType())
]),

"artifact_citations_schema": StructType([
    StructField("artifactid", StringType(), nullable=False),
    StructField("target", StringType()),
    StructField("citcount", LongType())
]),


"projects_schema" : StructType([
    StructField("id", StringType(), nullable=False),
    StructField("acronym", StringType()),
    StructField("title", StringType()),
    StructField("funder", StringType()),
    StructField("fundingstring", StringType()),
    StructField("funding_lvl0", StringType()),
    StructField("funding_lvl1", StringType()),
    StructField("funding_lvl2", StringType()),
    StructField("ec39", BooleanType()),
    StructField("type", StringType()),
    StructField("startdate", StringType()),
    StructField("enddate", StringType()),
    StructField("start_year", DoubleType()),
    StructField("end_year", DoubleType()),
    StructField("duration", DoubleType()),
    StructField("haspubs", StringType()),
    StructField("numpubs", LongType()),
    StructField("daysforlastpub", LongType()),
    StructField("delayedpubs", LongType()),
    StructField("callidentifier", StringType()),
    StructField("code", StringType()),
    StructField("totalcost", FloatType()),
    StructField("fundedamount", FloatType()),
    StructField("currency", StringType())
]),

"projects_artifacts_schema": StructType([
    StructField("projectid",StringType(), nullable=False),
    StructField("artifactid",StringType(), nullable=False),
    StructField("provenance",StringType())
]),

"project_artifactcount_schema" : StructType([
    StructField("projectid",StringType(), nullable=False),
    StructField("publications",LongType()),
    StructField("datasets",LongType()),
    StructField("software",LongType()),
    StructField("other",LongType())
]),

"views_stats_schema" : StructType([
    StructField("date",StringType(), nullable=False),
    StructField("artifactid",StringType()),
    StructField("source",StringType()),
    StructField("repository_id",StringType()), 
    StructField("count",LongType())
])
}

