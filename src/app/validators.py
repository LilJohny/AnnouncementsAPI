from datetime import datetime

from app.constants import DATETIME_FORMAT, DATETIME_VALIDATION_VIOLATED_MESSAGE, DATETIME_FIELD, \
    TICKET_PRICE_VALIDATION_VIOLATED_MESSAGE, TICKET_PRICE_FIELD
from app.validation_error import ValidationError


def validate_str_datetime(date_time_str: str, errors: list):
    try:
        _ = datetime.strptime(date_time_str, DATETIME_FORMAT)
    except ValueError:
        error = ValidationError(DATETIME_FIELD, DATETIME_VALIDATION_VIOLATED_MESSAGE)
        errors.append(error.error_message)


def validate_str_float(float_str_val: str, errors: list):
    try:
        _ = float(float_str_val)
    except ValueError:
        error = ValidationError(TICKET_PRICE_FIELD, TICKET_PRICE_VALIDATION_VIOLATED_MESSAGE)
        errors.append(error.error_message)
