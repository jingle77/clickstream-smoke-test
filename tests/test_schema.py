from src.clickstream_smoke_test.schema import REQUIRED_COLUMNS


def test_required_columns_present_in_schema():
    assert "customer_id" in REQUIRED_COLUMNS
    assert "converted" in REQUIRED_COLUMNS
    assert len(REQUIRED_COLUMNS) > 0