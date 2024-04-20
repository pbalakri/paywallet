from rest_framework import serializers

from cafe.serializers import CafeOrderSerializer, CafeSerializer

from .models import Wallet, Transaction
from django.utils import timezone


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class TransactionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionGetSerializer(serializers.ModelSerializer):
    merchant_information = CafeSerializer(source='merchant')
    transaction_date = serializers.SerializerMethodField('get_date')
    order_information = CafeOrderSerializer(source='order')
    # transaction_information =

    def get_date(self, obj):
        return timezone.localtime(obj.date).date()

    class Meta:
        model = Transaction
        fields = ['id', 'type', 'amount', 'transaction_date',
                  'reference', 'wallet', 'merchant_information', 'order_information']
