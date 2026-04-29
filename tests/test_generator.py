from src.clickstream_smoke_test.generator import generate_clickstream_data
from src.clickstream_smoke_test.schema import REQUIRED_COLUMNS


def test_generator_returns_expected_shape_and_columns():
    df = generate_clickstream_data(100)

    assert df.shape[0] == 100
    assert set(REQUIRED_COLUMNS).issubset(df.columns)


def test_customer_ids_are_in_valid_range_and_unique_for_run():
    df = generate_clickstream_data(100)

    assert df["customer_id"].between(1, 1000).all()
    assert df["customer_id"].nunique() == 100


def test_entry_page_values_are_valid():
    df = generate_clickstream_data(100)

    valid_pages = {"Homepage", "Deals", "Product"}
    assert set(df["entry_page"]).issubset(valid_pages)


def test_page_views_and_product_views_are_in_valid_ranges():
    df = generate_clickstream_data(100)

    assert df["page_views"].between(1, 50).all()
    assert df["product_views"].between(1, 20).all()


def test_conversion_probability_is_bounded():
    df = generate_clickstream_data(100)

    assert df["conversion_probability"].between(0.0005, 0.05).all()


def test_converted_is_binary():
    df = generate_clickstream_data(100)

    assert set(df["converted"]).issubset({0, 1})


def test_source_name_and_run_date_can_be_overridden():
    df = generate_clickstream_data(
        row_count=10,
        source_name="test_source",
        run_date="2026-04-29",
    )

    assert (df["source"] == "test_source").all()
    assert (df["run_date"] == "2026-04-29").all()