from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param
from rest_framework.utils.urls import replace_query_param


class BasePagination(PageNumberPagination):
    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.get_full_path()
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.get_full_path()
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_next_number(self):
        if not self.page.has_next():
            return None

        return self.page.next_page_number()

    def get_previous_number(self):
        if not self.page.has_previous():
            return None

        return self.page.previous_page_number()

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {"next": self.get_next_link(), "previous": self.get_previous_link()},
                "numbers": {
                    "current": self.page.number,
                    "previous": self.get_previous_number(),
                    "next": self.get_next_number(),
                },
                "count": self.page.paginator.count,
                "page_size": self.page_size,
                "results": data,
            }
        )
