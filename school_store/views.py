from rest_framework.views import APIView

from paywallet.permissions import IsGuardian
from .models import Category, Order, Product
from .serializers import OrderedCategorySerializer, OrderSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class GetProductsView(APIView):

    # Get products per school
    def get(self, request, school_id):
        try:
            products = Product.objects.filter(school_guid=school_id)
        except Product.DoesNotExist:
            return Response({'error': 'Products not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProductsPerCategoryView(APIView):
    # Get products per school per category
    def get(self, request, school_id, category_id):
        try:
            products = Product.objects.filter(
                school_guid=school_id, category_id=category_id)
        except Product.DoesNotExist:
            return Response({'error': 'Products not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProducts(APIView):
    # Get products per school
    def get(self, request, school_id):
        try:
            products = Product.objects.filter(school__guid=school_id)
        except Product.DoesNotExist:
            return Response({'error': 'Products not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProduct(APIView):
    # Get product details
    def get(self, request, school_id, product_id):
        try:
            product = Product.objects.get(
                school__guid=school_id, id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCategories(APIView):
    # Get categories per school
    def get(self, request, school_id):
        try:
            categories = Category.objects.filter(school_guid=school_id)
        except Category.DoesNotExist:
            return Response({'error': 'Categories not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderedCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetOrders(APIView):
    permission_classes = [IsGuardian, IsAuthenticated]

    def get(self, request):
        try:
            orders = Order.objects.filter(
                customer__user=request.user
            )
        except Order.DoesNotExist:
            return Response({'error': 'Orders not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
