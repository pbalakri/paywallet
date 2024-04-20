from rest_framework import serializers

from cafe.models import Inventory
from cafe.models.order import Order, OrderItem
from product.serializers import ProductSerializer

from .models import Cafe


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ['id', 'name']


class CafeProductSerializer(serializers.ModelSerializer):
    product_information = ProductSerializer(source='product')

    class Meta:
        model = Inventory
        fields = ['product_information', 'quantity', 'price']


class CafeOrderedProductSerializer(serializers.ModelSerializer):
    product_information = ProductSerializer(source='product')

    class Meta:
        model = Inventory
        fields = ['product_information']


class CafeOrderItemSerializer(serializers.ModelSerializer):
    # item = CafeOrderedProductSerializer(source='product')
    item = ProductSerializer(source='product.product')

    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']


class CafeOrderSerializer(serializers.ModelSerializer):
    items = CafeOrderItemSerializer(source='orderitem_set', many=True)
    total = serializers.SerializerMethodField('get_total')

    def get_total(self, obj):
        return obj.get_total()

    class Meta:
        model = Order
        fields = ['id', 'date',
                  'payment_method', 'items', 'total']
