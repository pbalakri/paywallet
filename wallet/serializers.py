from rest_framework import serializers

from cafe.serializers import CafeSerializer

from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class TransactionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionGetSerializer(serializers.ModelSerializer):
    merchant_name = CafeSerializer(source='merchant')

    class Meta:
        model = Transaction
        fields = ['id', 'type', 'amount',
                  'reference', 'wallet', 'merchant_name', 'order']
