import pandas as pd
import pytest

from src.clickstream_smoke_test.schema import (
    REQUIRED_COLUMNS,
    validate_required_columns,
)


def test_required_columns_present_in_schema():
    assert "customer_id" in REQUIRED_COLUMNS
    assert "converted" in REQUIRED_COLUMNS
    assert len(REQUIRED_COLUMNS) > 0


def test_validate_required_columns_passes_for_valid_dataframe():
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

    validate_required_columns(df)


def test_validate_required_columns_raises_for_missing_columns():
    df = pd.DataFrame(
        [
            {
                "run_date": "2026-04-29",
                "utc_timestamp": "2026-04-29T12:00:00+00:00",
                "customer_id": 123,
                "entry_page": "Homepage",
                "page_views": 10,
                "product_views": 3,
                "converted": 0,
                "source": "test_source",
            }
        ]
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_required_columns(df)