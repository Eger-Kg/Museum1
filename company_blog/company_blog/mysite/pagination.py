from rest_framework.pagination import LimitOffsetPagination


class ListPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 1000