from rest_framework.response import Response
from rest_framework import status as rest_status


class SuccessResponse(Response):
    def __init__(self, status=rest_status.HTTP_200_OK, message='succeed', data={}):
        results = {
            'results': {
                'status_code': status,
                'message': message,
            }
        }
        if data:
            results['results']['data'] = data

        super(SuccessResponse, self).__init__(data=results, status=status)


class ErrorResponse(Response):
    def __init__(self, status=rest_status.HTTP_404_NOT_FOUND, message='error', data={}):
        results = {
            'error': {
                'status_code': status,
                'message': message
            }
        }
        if data:
            results['error']['data'] = data

        super(ErrorResponse, self).__init__(data=results, status=status)
