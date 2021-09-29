from rest_framework import filters
from django.db.models.functions import Length
from django.db.models import Case, IntegerField, Value, When


class CustomFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        flag_params = {'0': 'false', '1': 'true'}
        is_favorited = request.query_params.get('is_favorited')
        is_in_shopping_cart = request.query_params.get('is_in_shopping_cart')
        author_id = request.query_params.get('author')
        tags = request.query_params.getlist('tags')
        if is_favorited:
            queryset = queryset.filter(is_favorited=flag_params[is_favorited])
        if is_in_shopping_cart:
            queryset = queryset.filter(is_in_shopping_cart=flag_params[is_favorited])
        if author_id:
            queryset = queryset.filter(author_id=int(author_id))
        if tags:
            queryset = queryset.filter(tags__slug__in=tags)

        return queryset


class CustomSearch(filters.SearchFilter):
    search_param = 'name'

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = request.query_params.get('name')

        if not search_fields or not search_terms:
            return queryset

        return queryset.filter(
            name__icontains=search_terms
        ).annotate(flag=Case(When(
            name__startswith=search_terms, then=Value(0)
        ), output_field=IntegerField(), default=Value(1)
        )
        ).order_by('flag', 'name')
