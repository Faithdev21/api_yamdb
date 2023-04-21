import re

from rest_framework import status
from rest_framework.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            'me is not valid username!'
        )
    if not bool(re.match(r'^[\w.@+-]+$', value)):
        raise ValidationError(
            'Incorrect symbols fot username'
        )
    return value


def validate_username_length(value):
    if len(value) > 150:
        raise ValidationError('The length of the field must not exceed 150',
                              code=status.HTTP_400_BAD_REQUEST)


def validate_email_length(value):
    if len(value) > 254:
        raise ValidationError('The length of the field must not exceed 254',
                              code=status.HTTP_400_BAD_REQUEST)
