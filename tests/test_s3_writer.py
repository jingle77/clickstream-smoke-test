from src.clickstream_smoke_test.s3_writer import build_s3_key


def test_build_s3_key():
    key = build_s3_key(
        prefix="synthetic_clickstream_daily",
        run_date="2026-04-29",
        filename="part-2026-04-29T12-00-00Z.parquet",
    )

    assert key == (
        "synthetic_clickstream_daily/"
        "run_date=2026-04-29/"
        "part-2026-04-29T12-00-00Z.parquet"
    )