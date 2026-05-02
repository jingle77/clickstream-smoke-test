from src.clickstream_smoke_test.config import get_settings
from src.clickstream_smoke_test.generator import generate_clickstream_data
from src.clickstream_smoke_test.s3_writer import (
    build_s3_key,
    upload_file_to_s3,
    write_dataframe_to_parquet,
)
from src.clickstream_smoke_test.schema import validate_required_columns
from src.clickstream_smoke_test.utils import get_utc_run_date, get_utc_timestamp


def main() -> None:
    settings = get_settings()

    if not settings.s3_bucket:
        raise ValueError("S3_BUCKET is required but was not provided.")

    if not settings.s3_prefix:
        raise ValueError("S3_PREFIX is required but was not provided.")

    resolved_run_date = settings.run_date or get_utc_run_date()
    ingest_date = resolved_run_date
    file_timestamp = get_utc_timestamp().replace(":", "-")
    filename = f"part-{file_timestamp}.parquet"

    df = generate_clickstream_data(
        row_count=settings.row_count,
        source_name=settings.source_name,
        run_date=resolved_run_date,
    )

    validate_required_columns(df)

    file_path = write_dataframe_to_parquet(
        df=df,
        output_dir="local_output",
        filename=filename,
    )

    s3_key = build_s3_key(
        prefix=settings.s3_prefix,
        ingest_date=ingest_date,
        filename=filename,
    )

    upload_file_to_s3(
        file_path=file_path,
        bucket=settings.s3_bucket,
        key=s3_key,
        aws_region=settings.aws_region,
    )

    print("Clickstream smoke test run completed.")
    print("Schema validation passed.")
    print(f"AWS region: {settings.aws_region}")
    print(f"S3 bucket: {settings.s3_bucket}")
    print(f"S3 key: {s3_key}")
    print(f"Run date: {resolved_run_date}")
    print(f"Ingest date: {ingest_date}")
    print(f"Row count requested: {settings.row_count}")
    print(f"Rows generated: {len(df)}")
    print(f"Local parquet output: {file_path}")
    print()
    print("Preview:")
    print(df.head())


if __name__ == "__main__":
    main()