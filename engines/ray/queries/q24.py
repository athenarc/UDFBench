import os

import pandas as pd
import ray


def run_query(datasets, folder_path=None):
    from udfs.scalar.deep_similarity_score import deep_similarity_score
    from udfs.table.file import file
    from udfs.table.aggregate_top import aggregate_top

    # ------------------------------------------------------------------
    # Load the two input datasets using the existing custom file UDF.
    # ------------------------------------------------------------------

    arxiv = (
        file(
            None,
            os.path.join(folder_path, "arxiv.csv"),
            "csv",
        )
        .to_pandas()
        .dropna()
    )

    arxiv.columns = ["arxivid", "abstract"]

    pubmed = (
        file(
            None,
            os.path.join(folder_path, "pubmed.txt"),
            "json",
        )
        .to_pandas()[["id", "abstract"]]
        .dropna()
        .rename(columns={"id": "pubmedid"})
    )

    # ------------------------------------------------------------------
    # Put PubMed in the Ray object store.
    #
    # Every Ray worker can access the same immutable PubMed table without
    # us repeatedly serializing it as part of every batch.
    # ------------------------------------------------------------------

    pubmed_ref = ray.put(pubmed)

    # ------------------------------------------------------------------
    # Convert Arxiv to a Ray Dataset.
    # ------------------------------------------------------------------

    arxiv_ds = ray.data.from_pandas(
        arxiv[["arxivid", "abstract"]]
    )

    # ------------------------------------------------------------------
    # For each Arxiv batch, generate:
    #
    #     batch_size(arxiv) x len(pubmed)
    #
    # pairs.
    #
    # This is still the necessary Cartesian product, but the work is
    # performed independently and in parallel by Ray workers rather than
    # by a Python list comprehension on the driver.
    # ------------------------------------------------------------------

    def make_pairs(batch: pd.DataFrame) -> pd.DataFrame:
        pubmed_df = ray.get(pubmed_ref)

        n_arxiv = len(batch)
        n_pubmed = len(pubmed_df)

        if n_arxiv == 0 or n_pubmed == 0:
            return pd.DataFrame(
                {
                    "arxivid": pd.Series(dtype=batch["arxivid"].dtype),
                    "arxiv_abstract": pd.Series(dtype=batch["abstract"].dtype),
                    "pubmedid": pd.Series(dtype=pubmed_df["pubmedid"].dtype),
                    "pubmed_abstract": pd.Series(
                        dtype=pubmed_df["abstract"].dtype
                    ),
                }
            )

        return pd.DataFrame(
            {
                "arxivid": batch["arxivid"].to_numpy().repeat(n_pubmed),
                "arxiv_abstract": batch["abstract"].to_numpy().repeat(n_pubmed),
                "pubmedid": pd.Series(
                    pubmed_df["pubmedid"].to_numpy()
                ).repeat(n_arxiv).to_numpy(),
                "pubmed_abstract": pd.Series(
                    pubmed_df["abstract"].to_numpy()
                ).repeat(n_arxiv).to_numpy(),
            }
        )

    pairs_ds = arxiv_ds.map_batches(
        make_pairs,
        batch_format="pandas",
        # Tune this according to the size of pubmed and available memory.
        batch_size=200
    )

    # ------------------------------------------------------------------
    # Compute the UDF in parallel.
    #
    # deep_similarity_score remains completely unchanged.
    # ------------------------------------------------------------------

    def compute_similarity(batch: pd.DataFrame) -> pd.DataFrame:
        batch = batch.copy()

        batch["similarity"] = deep_similarity_score(
            batch["arxiv_abstract"].to_numpy(),
            batch["pubmed_abstract"].to_numpy(),
            "sentence-transformers/all-MiniLM-L6-v2",
            "cpu",
        )

        return batch[
            [
                "arxivid",
                "arxiv_abstract",
                "pubmedid",
                "pubmed_abstract",
                "similarity",
            ]
        ]

    similarity_ds = pairs_ds.map_batches(
        compute_similarity,
        batch_format="pandas",
        batch_size=200,
        num_cpus=20
    )

    # ------------------------------------------------------------------
    # aggregate_top is also executed inside Ray.
    #
    # Each arxivid becomes one group, so we don't need:
    #
    #     similarity_ds.to_pandas()
    #
    # on the driver.
    # ------------------------------------------------------------------

    result_ds = similarity_ds.groupby("arxivid").map_groups(
        lambda df: aggregate_top(
            df,
            "arxivid",
            "similarity",
            5,
        ),
        batch_format="pandas",
    )

    # ------------------------------------------------------------------
    # Keep the same output schema as the original implementation.
    # ------------------------------------------------------------------

    return result_ds.select_columns(
        ["arxivid", "pubmedid", "similarity"]
    )
