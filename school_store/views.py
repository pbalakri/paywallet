from rest_framework.views import APIView
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class GetProductsView(APIView):

    # Get products per school
    def get(self, request, school_id):
        try:
            products = Product.objects.filter(school_id=school_id)
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


class GetProduct(APIView):
    # Get product details
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCategories(APIView):
    # Get categories per school
    def get(self, request, school_id):
        try:
            categories = Category.objects.filter(school_id=school_id)
        except Category.DoesNotExist:
            return Response({'error': 'Categories not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
