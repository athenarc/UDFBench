
from udfs.aggregate.aggregate_max import Aggregate_max
from udfs.scalar import cleandate,jsonparse
import pyarrow as pa

def run_query(datasets,folder_path=None):
    artifact_authors = datasets["artifact_authors"]
    artifacts =  datasets["artifacts"]
    projects =  datasets["projects"]
    projects_artifacts =  datasets["projects_artifacts"]
    artifact_authors =  datasets["artifact_authors"]

    artifact_authors_new = artifact_authors.filter(expr="affiliation != '[]' and authorid != '[]'")
    aa = artifact_authors_new.map_batches(lambda batch: pa.table({
        "artifactid": batch["artifactid"],
        "authorid":  batch["authorid"],
        "affiliation":  batch["affiliation"],
        "rank":  batch["rank"],
        "authoridvalue": jsonparse(batch["authorid"],key='value'),
        "affiliationvalue": jsonparse(batch["affiliation"],key='value')
    }), batch_format="pyarrow")

    aa = aa.filter(expr="rank == 1")
    a = artifacts.map_batches(
        lambda batch: pa.table({
        "artifactid": batch["id"],
        "cleandate":  cleandate(batch["date"])
    }), batch_format="pyarrow")
    projects_artifacts = projects_artifacts.select_columns(["artifactid","projectid"])

    p = projects.filter(expr="funder == 'European Commission'")\
    .select_columns(["id"]).rename_columns({"id": "projectid"})

    aa_a = aa.join(a,
    on=("artifactid",), right_on=("artifactid",), join_type="inner",num_partitions=4).materialize()

    aa_a_pr = aa_a.join(
        projects_artifacts, on=("artifactid",),
        right_on=("artifactid",), join_type="inner",num_partitions=4).materialize()
    
    full_join = aa_a_pr.join(p,
    on=("projectid",), right_on=("projectid",), join_type="inner",num_partitions=4).materialize()

    max_dates = (
        artifact_authors.filter(expr="rank == 1")
        .select_columns(["authorid","artifactid"])
        .join(a, on=("artifactid",), right_on=("artifactid",), join_type="inner",num_partitions=4)
        .groupby("authorid")
        .aggregate(Aggregate_max(on="cleandate"))
    )

    aa_a_with_max = full_join.join(
        max_dates,
        on=("authorid", "cleandate",),
        right_on=("authorid", "max(cleandate)",),
        join_type="inner",
        num_partitions=4
    )
    res = aa_a_with_max.select_columns(["authoridvalue","affiliationvalue"])
    return res

