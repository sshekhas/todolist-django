import math
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class XlPageNumberPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page-size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("page_size", self.max_page_size),
                    (
                        "pages_count",
                        math.ceil(self.page.paginator.count / self.max_page_size),
                    ),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )