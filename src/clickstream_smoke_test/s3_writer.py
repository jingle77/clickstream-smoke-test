def build_s3_key(prefix: str, run_date: str, filename: str) -> str:
    return f"{prefix}/run_date={run_date}/{filename}"


def upload_bytes_to_s3(*args, **kwargs) -> None:
    """
    Placeholder for S3 upload logic.
    Real implementation will be added later.
    """
    raise NotImplementedError("S3 upload logic has not been implemented yet.")