from rest_framework.views import APIView
from cafe.models import Cafe
from restriction.models import CategoryRestriction, PaymentRestriction, ProductsRestriction
from restriction.serializers import ProductRestrictionSerializer, CategoryPurchaseRestrictionSerializer, PaymentRestrictionSerializer
from .serializers import TransactionGetSerializer, TransactionPostSerializer
from .models import Wallet, Transaction
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from paywallet.permissions import IsGuardian, isVendor
from rest_framework import status
from django.db import transaction
from .helpers.restrictions import get_restrictions


class BalanceView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]

    def get(self, request, rfid):
        wallet = Wallet.objects.get(rfid=rfid)
        return Response({"balance": wallet.balance})


class TransactionsView(APIView):
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsGuardian()]
        elif self.request.method == 'POST':
            return [IsAuthenticated(), isVendor()]
        return []

    def get(self, request, rfid):
        paginator = PageNumberPagination()

        transactions = Transaction.objects.filter(
            wallet__rfid=rfid).order_by('-date')
        page = paginator.paginate_queryset(transactions, request)
        if page is not None:
            transaction_serializer = TransactionGetSerializer(
                page, many=True)
            return paginator.get_paginated_response(transaction_serializer.data)

        transaction_serializer = TransactionGetSerializer(
            transactions, many=True)
        return Response({"transactions": transaction_serializer.data})

    def post(self, request, rfid):
        # Create a transaction
        try:
            wallet = Wallet.objects.get(bracelet_rfid=rfid)
        except Wallet.DoesNotExist:
            return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            merchant = Cafe.objects.get(vendor_admin=request.user)
        except Cafe.DoesNotExist:
            return Response({'error': 'Merchant not found'}, status=status.HTTP_404_NOT_FOUND)
        transaction_type = request.data.get('type')
        if transaction_type not in ['debit', 'credit']:
            return Response({'error': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)
        amount = request.data.get('amount')
        if transaction_type == 'debit':
            restrictions = get_restrictions(wallet.bracelet)
            if wallet.balance < amount:
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                wallet.balance -= amount
        else:
            wallet.balance += amount
        with transaction.atomic():
            wallet.save()
            transaction_data = {'type': transaction_type,
                                'amount': amount, 'wallet': wallet.id, 'merchant_id': merchant.id, 'reference': "sdf"}
            transaction_serializer = TransactionPostSerializer(
                data=transaction_data)
            if transaction_serializer.is_valid():
                transaction_serializer.save()
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseRestrictionView(APIView):
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
        cat_restriction_serializer = CategoryPurchaseRestrictionSerializer(
            catـrestriction, many=True)
        product_restriction_serializer = ProductRestrictionSerializer(
            product_restriction, many=True)
        return Response({
            "payment_restriction": payment_restriction_serializer.data,
            "category_restriction": cat_restriction_serializer.data,
            "product_restriction": product_restriction_serializer.data
        }, status=status.HTTP_200_OK)
