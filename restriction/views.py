from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from restriction.models import CategoryRestriction, PaymentRestriction, ProductsRestriction
from .serializers import ProductRestrictionSerializer, CategoryRestrictionSerializer, PaymentRestrictionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
# Create your views here.


@authentication_classes([])
@permission_classes([])
class RestrictionView(APIView):
    # permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        rfid = request.query_params['rfid']
        catـrestriction = CategoryRestriction.objects.filter(
            student__bracelet__rfid=rfid)
        product_restriction = ProductsRestriction.objects.filter(
            student__bracelet__rfid=rfid)
        payment_restriction = PaymentRestriction.objects.filter(
            student__bracelet__rfid=rfid)
        payment_restriction_serializer = PaymentRestrictionSerializer(
            payment_restriction)
        cat_restriction_serializer = CategoryRestrictionSerializer(
            catـrestriction, many=True)
        product_restriction_serializer = ProductRestrictionSerializer(
            product_restriction)
        return Response({
            "payment_restriction": payment_restriction_serializer.data,
            "category_restriction": cat_restriction_serializer.data,
            "product_restriction": product_restriction_serializer.data
        }, status=status.HTTP_200_OK)
