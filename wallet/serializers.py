from rest_framework import serializers

from cafe.serializers import CafeSerializer

from .models import Wallet, Transaction
from restriction.models import CategoryRestriction, PaymentRestriction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class TransactionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionGetSerializer(serializers.ModelSerializer):
    merchant = CafeSerializer(source='merchant')

    class Meta:
        model = Transaction
        fields = ['id', 'type', 'amount',
                  'reference', 'wallet', 'merchant']
