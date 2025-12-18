TRANSACTION_FAILED = {
    "code": "TF4007",
    "message": "Transaction failed",
    "lang": "en",
}

USER_PROFILE_CREATION_FAILED = {
    "code": "MONETA_UPCF_404",
    "message": "Couldn't create new user profile.",
    "lang": "en",
}

VALID_DATA_NOT_FOUND = {
    "code": "MONETA_VDNF_400",
    "message": "Valid data not found",
    "lang": "en",
}


USER_ALREADY_EXISTS = {
    "code": "MONETA_UAE_400",
    "message": "An user with this email already exists.",
    "lang": "en",
}

INVALID_EMAIL_FORMAT = {
    "code": "MONETA_IEF_400",
    "message": "The provided email is not in valid format.",
    "lang": "en",
}

INVALID_LOGIN_CREDENTIALS = {
    "code": "MONETA_ILC_401",
    "message": "The provided login credentials (username or password) are invalid.",
    "lang": "en"
}

VALIDATION_ERROR_DICT = {
    "UAE_403": USER_ALREADY_EXISTS,
    "IEF_403": INVALID_EMAIL_FORMAT,
}