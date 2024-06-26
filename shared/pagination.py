from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_parm = 'page_size'
    max_page_size = 100


    def get_paginated_response(self, data):
        return Response({
            'next':self.get_next_link(),
            'previus':self.get_previous_link(),
            'count':self.page.paginator.count,
            'result':data,
        })