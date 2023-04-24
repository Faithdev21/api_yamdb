import re

from api import constants
from rest_framework import status
from rest_framework.exceptions import ValidationError


def validate_username(value: str) -> str:
    """Checking the username is not 'me'."""
    if value.lower() == 'me':
        raise ValidationError(
            'me is not valid username!'
        )
    if not bool(re.match(r'^[\w.@+-]+$', value)):
        raise ValidationError(
            'Incorrect symbols fot username'
        )
    return value


def validate_username_length(value: str) -> None:
    """Checking the username length."""
    if len(value) > constants.USER_USERNAME_MAX_LENGTH:
        raise ValidationError('The length of the field must not exceed 150',
                              code=status.HTTP_400_BAD_REQUEST)


def validate_email_length(value: str) -> None:
    """Checking the email length."""
    if len(value) > constants.USER_EMAIL_MAX_LENGTH:
        raise ValidationError('The length of the field must not exceed 254',
                              code=status.HTTP_400_BAD_REQUEST)
