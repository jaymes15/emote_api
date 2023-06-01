from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import Response, exception_handler


def custom_exception_handler(message, context):
    # Call REST framework's default exception handler first
    # to get the standard error response.

    response = exception_handler(message, context)

    if isinstance(message, IntegrityError) and not response:
        # if there is an IntegrityError and the error response
        # hasn't already been generated
        response = Response(
            {"message": str(message)}, status=status.HTTP_400_BAD_REQUEST
        )

    elif isinstance(message, ValidationError) and not response:
        # if there is an ValidationError and the error response
        # hasn't already been generated
        response = Response(
            {"message": str(message)}, status=status.HTTP_400_BAD_REQUEST
        )

    return response


def validation_error(message, code=None, field="__all__", params=None):
    """
    standardizes validation errors
    """
    if code is not None:
        return ValidationError(
            message,
            code=code,
        )
    return ValidationError({field: message}, params=params)
