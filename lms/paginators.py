from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    """Пагинатор для отображения данных постранично"""

    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 10
