import random

import pandas as pd

from src.clickstream_smoke_test.utils import get_utc_run_date, get_utc_timestamp


ENTRY_PAGE_WEIGHTS = {
    "Homepage": 0.55,
    "Deals": 0.30,
    "Product": 0.15,
}

ENTRY_PAGE_BASE_PROPENSITY = {
    "Homepage": 0.003,
    "Deals": 0.012,
    "Product": 0.025,
}


def _choose_entry_page() -> str:
    pages = list(ENTRY_PAGE_WEIGHTS.keys())
    weights = list(ENTRY_PAGE_WEIGHTS.values())
    return random.choices(pages, weights=weights, k=1)[0]


def _calculate_conversion_probability(
    entry_page: str,
    page_views: int,
    product_views: int,
) -> float:
    base_propensity = ENTRY_PAGE_BASE_PROPENSITY[entry_page]
    page_view_effect = 0.0002 * (page_views - 1)
    product_view_effect = 0.0010 * product_views
    random_noise = random.uniform(-0.003, 0.003)

    probability = (
        base_propensity
        + page_view_effect
        + product_view_effect
        + random_noise
    )

    return min(max(probability, 0.0005), 0.05)


def generate_clickstream_data(
    row_count: int,
    source_name: str = "codespaces_smoke_test",
    run_date: str | None = None,
) -> pd.DataFrame:
    if row_count <= 0:
        raise ValueError("row_count must be greater than 0")

    resolved_run_date = run_date or get_utc_run_date()
    utc_timestamp = get_utc_timestamp()

    sampled_customer_ids = random.sample(range(1, 1001), k=row_count)

    records = []

    for customer_id in sampled_customer_ids:
        entry_page = _choose_entry_page()
        page_views = random.randint(1, 50)
        product_views = random.randint(1, 20)

        conversion_probability = _calculate_conversion_probability(
            entry_page=entry_page,
            page_views=page_views,
            product_views=product_views,
        )

        converted = int(random.random() < conversion_probability)

        records.append(
            {
                "run_date": resolved_run_date,
                "utc_timestamp": utc_timestamp,
                "customer_id": customer_id,
                "entry_page": entry_page,
                "page_views": page_views,
                "product_views": product_views,
                "conversion_probability": round(conversion_probability, 6),
                "converted": converted,
                "source": source_name,
            }
        )

    return pd.DataFrame(records)