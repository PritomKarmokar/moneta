def format_output_success(
    status_code: dict,
    data: dict,
) -> dict:
    status_code.update({"data": data})
    return status_code