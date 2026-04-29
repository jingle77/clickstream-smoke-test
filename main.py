from src.clickstream_smoke_test.config import get_settings


def main() -> None:
    settings = get_settings()

    print("Clickstream smoke test scaffold is set up.")
    print(f"AWS region: {settings.aws_region}")
    print(f"S3 bucket: {settings.s3_bucket or '[not set]'}")
    print(f"S3 prefix: {settings.s3_prefix}")
    print(f"Row count: {settings.row_count}")
    print(f"Source name: {settings.source_name}")
    print(f"Run date override: {settings.run_date or '[auto]'}")


if __name__ == "__main__":
    main()