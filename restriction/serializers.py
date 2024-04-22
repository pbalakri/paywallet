from rest_framework import serializers
from product.models.allergy import Allergy
from product.serializers import CategorySerializer, ProductSerializer

from restriction.models import CategoryRestriction, DietRestriction, PaymentRestriction, ProductsRestriction


class PaymentRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRestriction
        fields = ['total_per_period', 'frequency']


class CategoryPurchaseRestrictionSerializer(serializers.ModelSerializer):
    category_information = CategorySerializer(source='category')

    class Meta:
        model = CategoryRestriction
        fields = ['category_information',
                  'total_per_period', 'frequency']


class CategoryViewRestrictionSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(source='category.id')

    class Meta:
        model = CategoryRestriction
        fields = ['category_id',
                  'total_per_period', 'frequency']


class ProductRestrictionSerializer(serializers.ModelSerializer):
    product_information = ProductSerializer(source='product')

    class Meta:
        model = ProductsRestriction
        fields = ['product_information', 'total_per_period', 'frequency']


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ['name', 'image']


class DietRestrictionSerializer(serializers.ModelSerializer):
    allergy_information = AllergySerializer(source='allergies', many=True)

    class Meta:
        model = DietRestriction
        fields = ['allergy_information']
