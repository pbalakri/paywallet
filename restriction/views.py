from rest_framework.permissions import IsAuthenticated

from paywallet.permissions import IsGuardian
from product.models import Category, Product
from restriction.models import CategoryRestriction, DietRestriction, PaymentRestriction, ProductsRestriction
from school.models import Student
from .serializers import DietRestrictionSerializer, ProductRestrictionSerializer, CategoryPurchaseRestrictionSerializer, PaymentRestrictionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
# Create your views here.


class StudentRestrictionsView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]

    def get(self, request, registration_number):
        # bracelet = Guardian.objects.get(
        #     user=request.user).student.get(registration_number=registration_number).bracelet
        diet_restriction = DietRestriction.objects.filter(
            student__registration_number=registration_number)
        catـrestriction = CategoryRestriction.objects.filter(
            student__registration_number=registration_number)
        product_restriction = ProductsRestriction.objects.filter(
            student__registration_number=registration_number)
        payment_restriction = PaymentRestriction.objects.filter(
            student__registration_number=registration_number)
        payment_restriction_serializer = PaymentRestrictionSerializer(
            payment_restriction, many=True)
        cat_restriction_serializer = CategoryPurchaseRestrictionSerializer(
            catـrestriction, many=True)
        product_restriction_serializer = ProductRestrictionSerializer(
            product_restriction, many=True)
        diet_restriction_serializer = DietRestrictionSerializer(
            diet_restriction, many=True)
        return Response({
            "diet_restriction": diet_restriction_serializer.data,
            "payment_restriction": payment_restriction_serializer.data,
            "category_restriction": cat_restriction_serializer.data,
            "product_restriction": product_restriction_serializer.data
        }, status=status.HTTP_200_OK)

        # elif restriction_type == 'category':


class StudentPaymentRestrictionView(APIView):
    def post(self, request, student_id):
        frequency = request.data['frequency']
        total_per_period = request.data['total_per_period']
        PaymentRestriction.objects.create(
            student=Student.objects.get(id=student_id), frequency=frequency, total_per_period=total_per_period)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    def get(self, request, registration_number):
        payment_restriction = PaymentRestriction.objects.filter(
            student__registration_number=registration_number)
        payment_restriction_serializer = PaymentRestrictionSerializer(
            payment_restriction, many=True)
        return Response({
            "payment_restriction": payment_restriction_serializer.data
        }, status=status.HTTP_200_OK)


class StudentCategoryRestrictionView(APIView):
    def post(self, request, student_id):
        frequency = request.data['frequency']
        total_per_period = request.data['total_per_period']
        category = Category.objects.get(id=request.data['category_id'])
        CategoryRestriction.objects.create(
            student=Student.objects.get(id=student_id), frequency=frequency, total_per_period=total_per_period, category=category)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class StudentProductRestrictionView(APIView):
    def post(self, request, student_id):
        frequency = request.data['frequency']
        total_per_period = request.data['total_per_period']
        product = Product.objects.get(id=request.data['product_id'])
        ProductsRestriction.objects.create(
            student=Student.objects.get(id=student_id), frequency=frequency, total_per_period=total_per_period, product=product)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


@authentication_classes([])
@permission_classes([])
class GuardianRestrictionView(APIView):
    # permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        rfid = request.query_params['rfid']
        catـrestriction = CategoryRestriction.objects.filter(
            student__bracelet__rfid=rfid)
        product_restriction = ProductsRestriction.objects.filter(
            student__bracelet__rfid=rfid)
        payment_restriction = PaymentRestriction.objects.filter(
            student__bracelet__rfid=rfid)
        payment_restriction_serializer = PaymentRestrictionSerializer(
            payment_restriction)
        cat_restriction_serializer = CategoryPurchaseRestrictionSerializer(
            catـrestriction, many=True)
        product_restriction_serializer = ProductRestrictionSerializer(
            product_restriction, many=True)
        return Response({
            "payment_restriction": payment_restriction_serializer.data,
            "category_restriction": cat_restriction_serializer.data,
            "product_restriction": product_restriction_serializer.data
        }, status=status.HTTP_200_OK)
