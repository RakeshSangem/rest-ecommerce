from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, Product
from api.serializers import (OrderCreateSerializer, OrderSerializer,
                             ProductInfoSerializer, ProductSerializer)


# All of this Generic API Views are Read-Only views.
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()  # pylint: disable=no-member
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
    ]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock']

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    # @api_view(["GET"])
    # def product_list(request):
    #     products = Product.objects.all()
    #     serializer = ProductSerializer(products, many=True)
    #     return Response(serializer.data)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view is used to retrieve, update, and delete a product.
    """
    queryset = Product.objects.all()  # pylint: disable=no-member
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    # @api_view(['GET'])
    # def product_detail(request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """
    This viewset is used to create, retrieve, update, and delete orders.
    """
    queryset = Order.objects.prefetch_related(  # pylint: disable=no-member
        "items__product")

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # can also check for POST - self.request.method == 'POST'
        if self.action == 'create' or self.action == 'update':
            return OrderCreateSerializer
        # elif self.action == 'update':
        #     return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        """
        Get the queryset for the current user.
        If the user is not staff, only return orders for the current user.
        """
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    @action(
        detail=False,
        methods=['get'],
        url_path='user-orders',
        # permission_classes=[IsAuthenticated]
    )
    def user_orders(self, request):
        """
        Get all orders for the current user.
        """

        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    # @api_view(["GET"])
    # def order_list(request):
    #     orders = Order.objects.prefetch_related("items__product")
    #     serializer = OrderSerializer(orders, many=True)
    #     return Response(serializer.data)


class UserOrdersAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related(  # pylint: disable=no-member
        "items__product")  # pylint: disable=no-member
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class ProductInfoAPIView(APIView):
    """
    This view is used to get the product info.
    """

    def get(self, request):
        """
        This view is used to get the product info.
        """
        products = Product.objects.all()  # pylint: disable=no-member
        serializer = ProductInfoSerializer({
            "products": products,
            "count": len(products),
            "max_price": products.aggregate(max_price=Max('price'))['max_price']
        })

        return Response(serializer.data)
        # @api_view(['GET'])
        # def product_info(request):
        #     products = Product.objects.all()
        #     serializer = ProductInfoSerializer({
        #         "products": products,
        #         "count": len(products),
        #         "max_price": products.aggregate(max_price=Max('price'))['max_price']
        #     })

        #     return Response(serializer.data)
