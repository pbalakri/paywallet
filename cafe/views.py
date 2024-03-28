from django.shortcuts import render

# Create your views here.

from rest_framework.permissions import IsAuthenticated
from .serializers import CafeProductSerializer
from cafe.models import Inventory
from paywallet.permissions import IsVendor
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.


class GetMerchantProducts(APIView):
    permission_classes = [IsAuthenticated, IsVendor]

    def get(self, request, merchant_id):
        try:
            products = Inventory.objects.filter(cafe__admin=request.user)
            inventorySerializer = CafeProductSerializer(products, many=True)
            return Response(inventorySerializer.data, status=status.HTTP_200_OK)

        except Inventory.DoesNotExist:
            return Response({'error': 'Products not found'}, status=status.HTTP_404_NOT_FOUND)
