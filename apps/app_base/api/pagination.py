from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import Response


def paginated_response(instance, data):
    return Response({
        'results': {
            'links': {
                'next': instance.get_next_link(),
                'previous': instance.get_previous_link()
            },
            'total_items': instance.count,
            'item_per_page': instance.limit,
            "data": data,
        }
    })


class StandardResultsSetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10

    def get_paginated_response(self, data):
        return paginated_response(instance=self, data=data)


class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 20

    def get_paginated_response(self, data):
        return paginated_response(instance=self, data=data)
