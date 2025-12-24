
import ray
from udfs.scalar import extractfunder,extractclass,extractid,jsoncount,lowerize,removeshortterms,jsortvalues,jsort,cleandate
from udfs.table import combinations_q16
from ray.data.expressions import col
from ray.data.aggregate import Sum

import pyarrow as pa
import pyarrow.compute as pc

def run_query(datasets,folder_path=None):
    artifacts =  datasets["artifacts"]
    projects =  datasets["projects"]
    projects_artifacts =  datasets["projects_artifacts"]
    artifact_authorlists =  datasets["artifact_authorlists"]


    NUM_PARTS = 16
    projects = projects.map_batches(
        lambda b: pa.table({
            "projectid_join": b["id"],
            "projectstart": b["startdate"],
            "projectend": b["enddate"],
            "funder": extractfunder(b["fundingstring"]),
                    "class": extractclass(b["fundingstring"]),
                            "projectid": extractid(b["fundingstring"])
        }),
        batch_format="pyarrow", zero_copy_batch=True,
    )

    artifact_authorlists = (artifact_authorlists.map_batches(
        lambda b: pa.table({
            "artifactid": b["artifactid"],
            "authorlist": b["authorlist"],
            "jsoncount": jsoncount(b["authorlist"])
        }),
        batch_format="pyarrow", zero_copy_batch=True,
    ).filter(expr=col("jsoncount") < 7).map_batches(
        lambda b: pa.table({
            "artifactid": b["artifactid"],
            "authorlist": lowerize(b["authorlist"])
        }),
        batch_format="pyarrow")
        .map_batches(lambda b: pa.table({
            "artifactid": b["artifactid"],
            "authorlist": removeshortterms(b["authorlist"])
        }), batch_format="pyarrow")
        .map_batches(lambda b: pa.table({
            "artifactid": b["artifactid"],
            "authorlist": jsortvalues(b["authorlist"])
        }), batch_format="pyarrow")
        .map_batches(lambda b: pa.table({
            "artifactid": b["artifactid"],
            "authorlist": jsort(b["authorlist"])
        }), batch_format="pyarrow")

    )


    projects_artifacts = projects_artifacts.map_batches(
        lambda b: pa.table({
            "projectid_join": b["projectid"],
            "artifactid": b["artifactid"],
        }),
        batch_format="pyarrow", zero_copy_batch=True,
    )

    artifacts = artifacts.map_batches(
        lambda b: pa.table({
            "artifactid": b["id"],
            "date": b["date"],
        }),
        batch_format="pyarrow", zero_copy_batch=True,
    )


    pairs = (
    projects_artifacts\
    .join(projects, on=("projectid_join",),join_type="inner",num_partitions=NUM_PARTS)\
    .join(artifacts, on=("artifactid",),join_type="inner",num_partitions=NUM_PARTS)\
    .join(artifact_authorlists, on=("artifactid",),join_type="inner",num_partitions=NUM_PARTS)

    ).map_batches(
        combinations_q16, 
        batch_format="pyarrow",
        fn_kwargs={"N": 2}
    ).materialize()

    projectpairs = pairs.filter(expr=(col("projectid").is_not_null()))\
        .map_batches(
                lambda b: pa.table({
                "authorpair": b["authorpair"],
                "funder": b["funder"],
                "class": b["class"],
                "projectid": b["projectid"],
                "pstartcleaned":cleandate(b["projectstart"]),
                "pendcleaned": cleandate(b["projectend"]),
            }),
            batch_format="pyarrow", zero_copy_batch=True,
        )
    pairs = pairs.map_batches(
                lambda b: pa.table({
                "authorpair": b["authorpair"],
                "pubdate": b["pubdate"],
            }),
            batch_format="pyarrow", zero_copy_batch=True,
        )
    inner_pairs = pairs.join(projectpairs,on=("authorpair",),join_type="inner",num_partitions=NUM_PARTS)
    inner_pairs = inner_pairs.map_batches(
                    lambda b: pa.table({

            "funder": b["funder"],
                "class": b["class"],
                "projectid": b["projectid"],
                "pubdate": cleandate(b["pubdate"]),
                "pstartcleaned": b["pstartcleaned"],
                "pendcleaned": b["pendcleaned"],}),    
                batch_format="pyarrow"



    ).map_batches(
        lambda batch: pa.table({
            "funder": batch["funder"],
                "class": batch["class"],
                "projectid": batch["projectid"],
            "authors_during": pc.if_else(
                pc.and_(
                    pc.greater_equal(batch["pubdate"], batch["pstartcleaned"]),
                    pc.less_equal(batch["pubdate"], batch["pendcleaned"])
                ),
                pa.scalar(1, pa.int32()),
                pa.scalar(None, pa.int32())
            ),
            "authors_before": pc.if_else(
                pc.less(batch["pubdate"], batch["pstartcleaned"])
                ,
                pa.scalar(1, pa.int32()),
                pa.scalar(None, pa.int32())
            ),
                    "authors_after": pc.if_else(
                
                    pc.greater(batch["pubdate"], batch["pendcleaned"]),
                
                pa.scalar(1, pa.int32()),
                pa.scalar(None, pa.int32())
            )
        }),
        batch_format="pyarrow"
    )
    result = inner_pairs.groupby(["funder", "class", "projectid"])\
    .aggregate(Sum(on="authors_during"),Sum(on="authors_before"),Sum(on="authors_after"))

    return result
