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


class IncludeProductFilter(Filter):
    def filter(self, qs, value):
        if value is None:
            return qs
        summary_query = []
        for order in qs:
            positions = order.positions
            for position in positions.all():
                if position.product.id == int(value):
                    summary_query.append(order.id)
        summary_query = qs.filter(id__in=summary_query)
        return summary_query


class ProductFilter(FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    include = IncludeFilter(field_name='name')

    class Meta:
        model = Product
        fields = ['name', 'price', 'description']


class ProductReviewFilter(FilterSet):

    class Meta:
        model = ProductReview
        fields = ['author', 'product', 'creation_date']


class OrderFilter(FilterSet):
    created = DateFromToRangeFilter(field_name='creation_date')
    created_at = django_filters.DateFilter(field_name='creation_date')
    updated = DateFromToRangeFilter(field_name='updating_date')
    updated_at = django_filters.DateFilter(field_name='updating_date')
    order_sum = django_filters.NumberFilter()
    order_sum__gt = django_filters.NumberFilter(field_name='order_sum', lookup_expr='gt')
    order_sum__lt = django_filters.NumberFilter(field_name='order_sum', lookup_expr='lt')
    product = IncludeProductFilter(field_name='positions')

    class Meta:
        model = Order
        fields = ['status', 'updating_date', 'creation_date', 'order_sum', 'positions']
