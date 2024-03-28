from rest_framework import serializers
from product.serializers import CategorySerializer, ProductSerializer

from restriction.models import CategoryRestriction, PaymentRestriction, ProductsRestriction


class PaymentRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRestriction
        fields = ['count_per_period', 'frequency']


class CategoryPurchaseRestrictionSerializer(serializers.ModelSerializer):
    category_information = CategorySerializer(source='category')

    class Meta:
        model = CategoryRestriction
        fields = ['category_information',
                  'count_per_period', 'frequency']


class CategoryViewRestrictionSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(source='category.id')

    class Meta:
        model = CategoryRestriction
        fields = ['category_id',
                  'count_per_period', 'frequency']


class ProductRestrictionSerializer(serializers.ModelSerializer):
    product_information = ProductSerializer(source='product')

    class Meta:
        model = ProductsRestriction
        fields = ['product_information', 'count_per_period', 'frequency']
