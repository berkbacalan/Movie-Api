from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class SmallPagination(PageNumberPagination):
    page_size = '10'


class LargePagination(PageNumberPagination):
    page_size = '2'


class CustomPagination(PageNumberPagination):
    '''Custom pagination usage.'''
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
