import django_filters
from api.models import Product


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
