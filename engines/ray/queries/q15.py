
from udfs.scalar import extractprojectid,extractcode
from udfs.table import file, xmlparser, extractkeys

import pyarrow as pa
import ray
import sys
def run_query(datasets,folder_path=None):
    if folder_path:

        artifacts =  datasets["artifacts"]
        projects =  datasets["projects"]
        projects_artifacts =  datasets["projects_artifacts"]

        ds =ray.data.from_items([1])

        ds_file = ds.map_batches(
            file,
            batch_format="pyarrow",
            fn_kwargs={"file_path": f"{folder_path}/crossref.xml", "file_type": "text"}
        )

        crossref = (ds_file
                .map_batches(
                    xmlparser,
                    batch_format="pyarrow",
                    fn_kwargs={"root_name":"publication"}
                )
                .map_batches(
                    extractkeys,
                    batch_format="pyarrow",
                    fn_kwargs={"key1":"publicationdoi","key2":"fundinginfo"}
                )
                .map_batches(lambda batch: pa.table({
                    "publicationdoi":  batch["publicationdoi"],
                    "projectid_fund":  extractprojectid(batch["fundinginfo"]),
                    }), batch_format="pyarrow"
                )
        )   

        projects_clean = projects.map_batches(
            lambda b: pa.table({
                "id": b["id"],
                "projectid_fund": extractcode(b["fundingstring"])
            }),
            batch_format="pyarrow"
        )
        joined = crossref.join(artifacts.select_columns(["id"]),
            on=("publicationdoi",),
            right_on=("id",),
            join_type="inner",
            num_partitions = 4)


        left_res = (
            joined.select_columns(["publicationdoi"])
            .join(
                projects_artifacts.select_columns(["artifactid","projectid"]),
                on=("publicationdoi",),
                right_on=("artifactid",),
                join_type="inner",
                num_partitions = 4
            )
            .join(
                projects_clean,
                on=("projectid",),
                right_on=("id",),
                join_type="inner",
                num_partitions = 4
            )
        )
        joined = joined.join(
                left_res.select_columns(["projectid_fund"]),
                on=("projectid_fund",),
                join_type="left_anti",
                num_partitions = 4
            )
        return joined

    else:
        print("Error, --ray-query, --ray-external need to be specified together", file=sys.stderr)
        sys.exit(2)
