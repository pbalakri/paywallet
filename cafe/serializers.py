from rest_framework import serializers

from cafe.models import Inventory
from product.serializers import ProductSerializer

from .models import Cafe


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ['name']


class CafeProductSerializer(serializers.ModelSerializer):
    product_information = ProductSerializer(source='product')

    class Meta:
        model = Inventory
        fields = ['product_information', 'quantity', 'price']
