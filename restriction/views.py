from rest_framework.permissions import IsAuthenticated
from django.db.models import Value

from paywallet.permissions import IsGuardian
from product.models import Category, Product
from product.models.allergy import Allergy
from restriction.models import CategoryRestriction, DietRestriction, PaymentRestriction, ProductsRestriction
from school.models import Student
from .serializers import AllergySerializer, DietRestrictionSerializer, ProductRestrictionSerializer, CategoryPurchaseRestrictionSerializer, PaymentRestrictionSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from django.db.models import Exists, OuterRef


class StudentRestrictionsView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]

    def get(self, request, registration_number):
        try:
            diet_restriction = DietRestriction.objects.get(
                student__registration_number=registration_number)
        except DietRestriction.DoesNotExist:
            diet_restriction = None
        all_allergies = Allergy.objects.all()
        # Annotate all allergies with a boolean field set to False
        all_allergies = all_allergies.annotate(state=Value(False))
        if diet_restriction:
            all_allergies = all_allergies.annotate(
                state=Exists(
                    diet_restriction.allergies.filter(pk=OuterRef('pk'))
                )
            )
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
        diet_restriction_serializer = AllergySerializer(
            all_allergies, many=True)
        return Response({
            "payment_restriction": payment_restriction_serializer.data,
            "category_restriction": cat_restriction_serializer.data,
            "product_restriction": product_restriction_serializer.data,
            "diet_restriction": diet_restriction_serializer.data
        }, status=status.HTTP_200_OK)


class StudentPaymentRestrictionView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]

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


class GuardianRestrictionView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]

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


class AllergiesView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]

    def post(self, request):
        registration_number = request.data['registration_number']
        # From allergy objects, create an array of allergy names where state is true

        allergies = [allergy['name'] for allergy in request.data['allergies']
                     if allergy['state'] == True]

        student = Student.objects.get(registration_number=registration_number)
        allergies = Allergy.objects.filter(name__in=allergies)
        # Check if the student already has a diet restriction
        diet_restriction = DietRestriction.objects.filter(
            student=student)
        if diet_restriction:
            diet_restriction = diet_restriction[0]
            diet_restriction.allergies.set(allergies)
        else:
            diet_restriction = DietRestriction.objects.create(
                student=student)
            diet_restriction.allergies.set(allergies)
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
