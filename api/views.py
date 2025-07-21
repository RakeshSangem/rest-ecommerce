from django.db.models import Max
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView

from api.models import Product, Order


# All of this Generic API Views are Read-Only views.
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()  # pylint: disable=no-member
    serializer_class = ProductSerializer

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


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related(  # pylint: disable=no-member
        "items__product")  # pylint: disable=no-member
    serializer_class = OrderSerializer
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
