import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    aws_region: str
    s3_bucket: str
    s3_prefix: str
    row_count: int
    source_name: str
    run_date: str | None = None


def get_settings() -> Settings:
    return Settings(
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
        s3_bucket=os.getenv("S3_BUCKET", ""),
        s3_prefix=os.getenv("S3_PREFIX", ""),
        row_count=int(os.getenv("ROW_COUNT", "100")),
        source_name=os.getenv("SOURCE_NAME", "codespaces_smoke_test"),
        run_date=os.getenv("RUN_DATE") or None,
    )