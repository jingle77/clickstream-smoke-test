from src.clickstream_smoke_test.config import get_settings


def test_get_settings_defaults():
    settings = get_settings()

    assert settings.aws_region
    assert settings.s3_prefix
    assert settings.row_count > 0
    assert settings.source_name