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

VALID_TOKEN_NOT_PROVIDED = {
    "code": "MONETA_VTNP_400",
    "message": "Invalid token provided.",
    "lang": "en",
}

USER_ALREADY_EXISTS = {
    "code": "MONETA_UAE_400",
    "message": "An user with this email already exists.",
    "lang": "en",
}

CATEGORY_NOT_EXISTS = {
    "code": "MONETA_CDNE_404",
    "message": "This Category not found. Either create this category or Please check the category and try again.",
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

CATEGORY_OBJECT_CREATION_FAILED = {
    "code": "MONETA_COCF_400",
    "message": "Failed to Create New Category.",
    "lang": "en"
}

EXPENSE_OBJECT_CREATION_FAILED = {
    "code": "MONETA_EOC_400",
    "message": "Failed to Create New Expense.",
    "lang": "en"
}

CATEGORY_OBJECT_UPDATE_FAILED = {
    "code": "MONETA_COCF_400",
    "message": "Failed to Update the existing Category.",
    "lang": "en"
}

EXPENSE_OBJECT_UPDATE_FAILED = {
    "code": "MONETA_COCF_400",
    "message": "Failed to Update the existing Expense.",
    "lang": "en"
}

NO_CATEGORIES_FOUND = {
    "code": "MONETA_NCF_204",
    "message": "No Categories Found",
    "lang": "en"
}

EXPENSE_UPDATE_NO_FIELDS_PROVIDED = {
    "code": "MONETA_EUNFP_400",
    "message": "Please provide at least one of: category, amount, or description to update the expense.",
    "lang": "en"
}

NO_EXPENSE_OBJECT_FOUND = {
    "code": "MONETA_NEOF_404",
    "message": "No Expense Object Found",
    "lang": "en"
}

VALIDATION_ERROR_DICT = {
    "UAE_403": USER_ALREADY_EXISTS,
    "IEF_403": INVALID_EMAIL_FORMAT,
    "CDNE_404": CATEGORY_NOT_EXISTS,
    "EUNFP_400": EXPENSE_UPDATE_NO_FIELDS_PROVIDED,
}