from applibs.status import (
    VALIDATION_ERROR_DICT,
    VALID_DATA_NOT_FOUND
)

def format_output_success(
    status_code: dict,
    data: dict,
) -> dict:
    status_code.update({"data": data})
    return status_code

def handle_validation_error(errors):
    for error in errors.items():
        return error[1][0].code

    return None

def render_serializer_error(errors):
    error_code = handle_validation_error(errors)
    return VALIDATION_ERROR_DICT.get(error_code, VALID_DATA_NOT_FOUND)