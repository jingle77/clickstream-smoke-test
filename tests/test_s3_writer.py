import pandas as pd

from src.clickstream_smoke_test.s3_writer import (
    build_s3_key,
    write_dataframe_to_parquet,
)


def test_build_s3_key():
    key = build_s3_key(
        prefix="synthetic_clickstream_daily",
        ingest_date="2026-04-29",
        filename="part-2026-04-29T12-00-00Z.parquet",
    )

    assert key == (
        "synthetic_clickstream_daily/"
        "ingest_date=2026-04-29/"
        "part-2026-04-29T12-00-00Z.parquet"
    )


def test_write_dataframe_to_parquet(tmp_path):
    df = pd.DataFrame(
        [
            {
                "run_date": "2026-04-29",
                "utc_timestamp": "2026-04-29T12:00:00+00:00",
                "customer_id": 123,
                "entry_page": "Homepage",
                "page_views": 10,
                "product_views": 3,
                "conversion_probability": 0.02,
                "converted": 0,
                "source": "test_source",
            }
        ]
    )

    file_path = write_dataframe_to_parquet(
        df=df,
        output_dir=str(tmp_path),
        filename="sample.parquet",
    )

    assert file_path.exists()
    assert file_path.suffix == ".parquet"

    reloaded_df = pd.read_parquet(file_path)
    assert reloaded_df.shape == (1, 9)
    assert list(reloaded_df.columns) == list(df.columns)