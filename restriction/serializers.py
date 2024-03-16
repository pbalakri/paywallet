from rest_framework import serializers

from restriction.models import CategoryRestriction, PaymentRestriction, ProductsRestriction


class PaymentRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRestriction
        fields = ['count_per_period', 'frequency']


class CategoryRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRestriction
        fields = ['category', 'count_per_period', 'frequency']


class ProductRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsRestriction
        fields = ['product', 'count_per_period', 'frequency']
