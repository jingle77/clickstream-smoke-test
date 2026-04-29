import pandas as pd


REQUIRED_COLUMNS = [
    "run_date",
    "utc_timestamp",
    "customer_id",
    "entry_page",
    "page_views",
    "product_views",
    "conversion_probability",
    "converted",
    "source",
]


def validate_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")