from rest_framework.views import exception_handler

from .response import ErrorResponse


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        return ErrorResponse(message=response.data.pop('detail'), status=response.status_code)

    return response
