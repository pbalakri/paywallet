from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from cafe.models import Cafe
from django.db.utils import IntegrityError
from wallet.helpers.payment_restrictions import check_for_payment_restrictions
from .serializers import TransactionGetSerializer, TransactionPostSerializer
from .models import Bracelet, Transaction, Device
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from paywallet.permissions import IsGuardian, isVendor
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db import transaction


# Create your views here.

# GET /api/v1/wallets/<char:rfid>/balance/
# GET /api/v1/wallets/<char:rfid>/transactions/
# POST /api/v1/wallets/<char:rfid>/transactions/


class BalanceView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsGuardian]

    def get(self, request, rfid):
        bracelet = Bracelet.objects.get(rfid=rfid)
        return Response({"balance": bracelet.balance})


class TransactionsView(APIView):
    authentication_classes = [SessionAuthentication]
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
            bracelet__rfid=rfid).order_by('-date')
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
            bracelet = Bracelet.objects.get(rfid=rfid)
        except Bracelet.DoesNotExist:
            return Response({'error': 'Bracelet not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            merchant = Cafe.objects.get(vendor_admin=request.user)
        except Cafe.DoesNotExist:
            return Response({'error': 'Merchant not found'}, status=status.HTTP_404_NOT_FOUND)
        transaction_type = request.data.get('type')
        if transaction_type not in ['debit', 'credit']:
            return Response({'error': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)
        amount = request.data.get('amount')
        if transaction_type == 'debit':
            check_for_payment_restrictions(bracelet)
            if bracelet.balance < amount:
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                bracelet.balance -= amount
        else:
            bracelet.balance += amount
        with transaction.atomic():
            bracelet.save()
            transaction_data = {'type': transaction_type,
                                'amount': amount, 'bracelet': bracelet.id, 'merchant_id': merchant.id, 'reference': "sdf"}
            transaction_serializer = TransactionPostSerializer(
                data=transaction_data)
            if transaction_serializer.is_valid():
                transaction_serializer.save()
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


# Register guardian as a user with Guardian role
class GuardianView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        device_fcm_token = request.data.get('device_fcm_token')

        required_fields = [username, password, first_name,
                           last_name, email, phone_number, device_fcm_token]
        if any(field is None or field == '' for field in required_fields):
            raise ValidationError(
                {'status': 'error', 'message': 'All fields are required'})

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                Device.objects.create(
                    guardian=user, device_fcm_token=device_fcm_token, phone_number=phone_number)
                user.groups.add(Group.objects.get(name='Guardian'))
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'status': 'username already exists'}, status=status.HTTP_400_BAD_REQUEST)
