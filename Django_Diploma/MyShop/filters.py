import django_filters
from .models import Product, ProductReview, Order
from django_filters.rest_framework import FilterSet
from django_filters import DateFromToRangeFilter
from django_filters import Filter


class IncludeFilter(Filter):
    def filter(self, qs, value):
        if value is None:
            return qs
        name_query = qs.filter(name__contains=value)
        description_query = qs.filter(description__contains=value)
        summary_query = name_query | description_query
        return summary_query


class ProductFilter(FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    include = IncludeFilter(field_name='name')
    # print(include)
    # if include is False:

    class Meta:
        model = Product
        fields = ['name', 'price', 'description']


class ProductReviewFilter(FilterSet):
    creation_date = DateFromToRangeFilter()

    class Meta:
        model = ProductReview
        fields = ['author', 'product', 'creation_date']


class OrderFilter(FilterSet):
    creation_date = DateFromToRangeFilter()
    updating_date = DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ['status', 'updating_date', 'creation_date']


