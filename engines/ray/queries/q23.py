import os

import pandas as pd
import ray


def run_query(datasets, folder_path=None):
    from udfs.scalar.deep_embed import deep_embed
    from udfs.scalar.deep_cosine import deep_cosine
    from udfs.table.file import file
    from udfs.table.aggregate_top import aggregate_top

    # ------------------------------------------------------------------
    # Load input data
    # ------------------------------------------------------------------

    arxiv = file(
        None,
        file_path=os.path.join(folder_path, "arxiv.csv"),
        file_type="csv",
    ).to_pandas()

    arxiv.columns = ["arxivid", "abstract"]
    arxiv = arxiv[["arxivid", "abstract"]].dropna()

    pubmed = (
        file(
            None,
            file_path=os.path.join(folder_path, "pubmed.txt"),
            file_type="json",
        )
        .to_pandas()[["id", "abstract"]]
        .dropna()
        .rename(columns={"id": "pubmedid"})
    )

    # ------------------------------------------------------------------
    # Convert the two inputs independently to Ray datasets.
    # ------------------------------------------------------------------

    arxiv_ds = ray.data.from_pandas(
        arxiv[["arxivid", "abstract"]]
    )

    pubmed_ds = ray.data.from_pandas(
        pubmed[["pubmedid", "abstract"]]
    )

    # ------------------------------------------------------------------
    # Compute each embedding ONLY ONCE.
    # ------------------------------------------------------------------

    def embed_arxiv(batch: pd.DataFrame) -> pd.DataFrame:
        batch = batch.copy()

        batch["arxiv_embedding"] = deep_embed(
            batch["abstract"].to_numpy(),
            "sentence-transformers/all-MiniLM-L6-v2",
            "cuda",
        )

        return batch.rename(
            columns={"abstract": "arxiv_abstract"}
        )

    arxiv_embedded = arxiv_ds.map_batches(
        embed_arxiv,
        batch_format="pandas",
        num_gpus=1,
        batch_size = 200
    )

    def embed_pubmed(batch: pd.DataFrame) -> pd.DataFrame:
        batch = batch.copy()

        batch["pubmed_embedding"] = deep_embed(
            batch["abstract"].to_numpy(),
            "sentence-transformers/all-MiniLM-L6-v2",
            "cuda"
        )

        return batch.rename(
            columns={"abstract": "pubmed_abstract"}
        )

    pubmed_embedded = pubmed_ds.map_batches(
        embed_pubmed,
        batch_format="pandas",
        num_gpus=1,
        batch_size = 200

    )

    # ------------------------------------------------------------------
    # Put PubMed embeddings in the Ray object store.
    #
    # ArXiv is streamed through Ray batches; each batch is crossed with
    # the complete PubMed embedding table.
    # ------------------------------------------------------------------

    pubmed_df = pubmed_embedded.to_pandas()
    pubmed_ref = ray.put(pubmed_df)

    # ------------------------------------------------------------------
    # Cartesian product.
    #
    # Importantly, this happens AFTER embedding, so we don't duplicate
    # the expensive deep_embed() computation.
    # ------------------------------------------------------------------

    def make_pairs(batch: pd.DataFrame) -> pd.DataFrame:
        pubmed_df = ray.get(pubmed_ref)

        left = batch[
            ["arxivid", "arxiv_abstract", "arxiv_embedding"]
        ].copy()

        right = pubmed_df[
            ["pubmedid", "pubmed_abstract", "pubmed_embedding"]
        ].copy()

        left["_key"] = 1
        right["_key"] = 1

        pairs = left.merge(
            right,
            on="_key",
            how="outer",
        ).drop(columns="_key")

        return pairs

    pairs_ds = arxiv_embedded.map_batches(
        make_pairs,
        batch_format="pandas",
        batch_size=200,
    )

    # ------------------------------------------------------------------
    # Compute cosine similarity in parallel.
    # ------------------------------------------------------------------

    def compute_similarity(batch: pd.DataFrame) -> pd.DataFrame:
        batch = batch.copy()

        batch["similarity"] = deep_cosine(
            batch["arxiv_embedding"].to_numpy(),
            batch["pubmed_embedding"].to_numpy(),
        )

        return batch[
            [
                "arxivid",
                "pubmedid",
                "similarity",
            ]
        ]

    similarity_ds = pairs_ds.map_batches(
        compute_similarity,
        batch_format="pandas",
        batch_size = 100
        #num_gpus=1
    )

    # ------------------------------------------------------------------
    # Top-5 per Arxiv document.
    #
    # This executes as a Ray group operation rather than converting the
    # complete similarity dataset to Pandas on the driver.
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

    return result_ds.select_columns(
        ["arxivid", "pubmedid", "similarity"]
    )
