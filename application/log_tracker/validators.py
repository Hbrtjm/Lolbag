from django.db import models
from django.core.exceptions import ValidationError

# Custom validator for the level field
def validate_log_level(value):
    valid_levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']
    if value not in valid_levels:
        raise ValidationError(f"{value} is not a valid log level. Choose from {valid_levels}.")
