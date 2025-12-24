
from udfs.scalar import extractprojectid
from udfs.table import file, jsonparse

import pyarrow as pa
import ray
import sys
def run_query(datasets,folder_path=None):

    if folder_path:
        ds =ray.data.from_items([1])

        ds_file = ds.map_batches(
            file,
            batch_format="pyarrow",
            fn_kwargs={"file_path": f"{folder_path}/crossref.txt", "file_type": "text"}
        )

        crossref = (ds_file
                .map_batches(
                jsonparse,
                batch_format="pyarrow",
                fn_kwargs={"key1":"publicationdoi", "key2":"fundinginfo"}
                )
                .map_batches(lambda batch: pa.table({
                "publicationdoi":  batch["publicationdoi"],
                "projectid":  extractprojectid(batch["fundinginfo"]),
                }), batch_format="pyarrow"
                )
        )   

        return crossref
    else:
        print("Error, --ray-query, --ray-external need to be specified together", file=sys.stderr)
        sys.exit(2)
