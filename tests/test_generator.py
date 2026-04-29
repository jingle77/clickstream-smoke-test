from src.clickstream_smoke_test.generator import generate_clickstream_data


def test_generator_returns_dataframe():
    df = generate_clickstream_data(100)
    assert hasattr(df, "shape")