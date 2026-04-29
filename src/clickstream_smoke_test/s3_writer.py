from pathlib import Path

import boto3
import pandas as pd


def build_s3_key(prefix: str, run_date: str, filename: str) -> str:
    return f"{prefix}/run_date={run_date}/{filename}"


def write_dataframe_to_parquet(
    df: pd.DataFrame,
    output_dir: str,
    filename: str,
) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / filename
    df.to_parquet(file_path, index=False)

    return file_path


def upload_file_to_s3(
    file_path: str | Path,
    bucket: str,
    key: str,
    aws_region: str,
) -> None:
    resolved_path = Path(file_path)

    if not resolved_path.exists():
        raise FileNotFoundError(f"Local file does not exist: {resolved_path}")

    s3_client = boto3.client("s3", region_name=aws_region)
    s3_client.upload_file(str(resolved_path), bucket, key)