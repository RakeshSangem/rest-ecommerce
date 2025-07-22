import django_filters
from api.models import Product, Order
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


class OrderFilter(django_filters.FilterSet):
    """
    Filter for orders.
    """
    # This enables filtering by date of order.
    created_at = django_filters.DateFilter(field_name='created_at__date')

    class Meta:
        """
        Meta class for OrderFilter.
        """
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['exact', 'lt', 'gt', 'range'],
            'user': ['exact'],
        }
