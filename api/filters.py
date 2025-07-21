import django_filters
from api.models import Product
from rest_framework import filters


class InStockFilterBackend(filters.BaseFilterBackend):
    """
    Filter for products that are in stock.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)


class ProductFilter(django_filters.FilterSet):
    """
    Filter for products.
    """

    class Meta:
        """
        Meta class for ProductFilter.
        """
        model = Product
        fields = {
            'name': ['iexact', 'icontains'],
            'price': ['exact', 'lt', 'gt', 'range'],
        }
