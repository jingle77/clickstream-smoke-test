from datetime import datetime, timezone


def get_utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_utc_run_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()