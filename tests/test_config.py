from src.clickstream_smoke_test.config import get_settings


def test_get_settings_defaults(monkeypatch):
    monkeypatch.delenv("AWS_REGION", raising=False)
    monkeypatch.delenv("S3_BUCKET", raising=False)
    monkeypatch.delenv("S3_PREFIX", raising=False)
    monkeypatch.delenv("ROW_COUNT", raising=False)
    monkeypatch.delenv("SOURCE_NAME", raising=False)
    monkeypatch.delenv("RUN_DATE", raising=False)

    settings = get_settings()

    assert settings.aws_region == "us-east-1"
    assert settings.s3_bucket == ""
    assert settings.s3_prefix == ""
    assert settings.row_count == 100
    assert settings.source_name == "codespaces_smoke_test"
    assert settings.run_date is None


def test_get_settings_reads_environment_overrides(monkeypatch):
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("S3_BUCKET", "jacob-data-ingestion-smoke-test")
    monkeypatch.setenv("S3_PREFIX", "synthetic_clickstream_daily")
    monkeypatch.setenv("ROW_COUNT", "250")
    monkeypatch.setenv("SOURCE_NAME", "integration_test_source")
    monkeypatch.setenv("RUN_DATE", "2026-04-29")

    settings = get_settings()

    assert settings.aws_region == "us-east-1"
    assert settings.s3_bucket == "jacob-data-ingestion-smoke-test"
    assert settings.s3_prefix == "synthetic_clickstream_daily"
    assert settings.row_count == 250
    assert settings.source_name == "integration_test_source"
    assert settings.run_date == "2026-04-29"