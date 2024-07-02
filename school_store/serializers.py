from rest_framework import serializers

from .models import Category, Product, OrderItem, Order


class OrderedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    category = OrderedCategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'school',
                  'category', 'price', 'stock', 'is_active']


class OrderedProductSerializer(serializers.ModelSerializer):
    category = OrderedCategorySerializer()

    class Meta:
        model = Product
        fields = ['name', 'image',
                  'category']


class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.SerializerMethodField('get_line_total')

    def get_line_total(self, obj):
        return obj.quantity * obj.unit_price
    product = OrderedProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['line_total', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)

    order_total = serializers.SerializerMethodField('get_order_total')

    def get_order_total(self, obj):
        total = 0
        orderitems = obj.orderitem_set.all()
        for item in orderitems:
            total += item.quantity * item.unit_price
        return total
    date = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Order
        fields = ['id', 'customer', 'date', 'updated_date',
                  'order_total', 'status', 'orderitem_set']
