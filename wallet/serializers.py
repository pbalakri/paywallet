from rest_framework import serializers

from cafe.serializers import CafeSerializer

from .models import Bracelet, PaymentRestriction, Transaction, CategoryRestriction


class BraceletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bracelet
        fields = '__all__'


class PaymentRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRestriction
        fields = '__all__'


class CategoryRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRestriction
        fields = '__all__'


class TransactionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionGetSerializer(serializers.ModelSerializer):
    merchant = CafeSerializer(source='merchant_id')

    class Meta:
        model = Transaction
        fields = ['id', 'type', 'amount',
                  'reference', 'bracelet', 'merchant']
