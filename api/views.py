from django.db.models import Max
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


# All of this Generic API Views are Read-Only views.
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # @api_view(["GET"])
    # def product_list(request):
    #     products = Product.objects.all()
    #     serializer = ProductSerializer(products, many=True)
    #     return Response(serializer.data)


class ProductDetailAPIView(generics.RetrieveAPIView):
    # queryset = Product.objects.all()
    queryset = Product.objects.filter(stock__gt=0)  # ORM query lookup syntax.
    serializer_class = ProductSerializer

    # @api_view(['GET'])
    # def product_detail(request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    # @api_view(["GET"])
    # def order_list(request):
    #     orders = Order.objects.prefetch_related("items__product")
    #     serializer = OrderSerializer(orders, many=True)
    #     return Response(serializer.data)


class UserOrdersAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        "products": products,
        "count": len(products),
        "max_price": products.aggregate(max_price=Max('price'))['max_price']
    })

    return Response(serializer.data)
