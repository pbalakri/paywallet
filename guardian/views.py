from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db import transaction
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from paywallet.permissions import IsGuardian
from restriction.models import CategoryRestriction, PaymentRestriction, ProductsRestriction
from restriction.serializers import CategoryPurchaseRestrictionSerializer, PaymentRestrictionSerializer, ProductRestrictionSerializer
from school.models import Student, School
from school_store.models import Product
from wallet.models import Transaction, TopUp
from wallet.serializers import TopupGetSerializer, TransactionGetSerializer
from .models import Device, Guardian
from .serializers import ReadGuardianSerializer, WriteGuardianSerializer, WriteUserSerializer
from wallet.helpers.gateway import create_buy_request, create_top_up_request


class GuardianView(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        try:
            guardians = Guardian.objects.get(user=request.user)
        except Guardian.DoesNotExist:
            return Response({'error': 'Guardians not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReadGuardianSerializer(guardians)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([])
@permission_classes([])
class GuardianRegisterView(APIView):
    def post(self, request):
        # Check if user with Guardian role exists
        try:
            User.objects.get(username=request.data['email'])
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass
        userSerializer = WriteUserSerializer(data={
            "username": request.data['email'],
            "password": make_password(request.data['password']),
            "email": request.data['email'],
            "first_name": request.data['first_name'],
            "last_name": request.data['last_name'],
        })
        with transaction.atomic():
            if (userSerializer.is_valid()):
                new_user = userSerializer.save()
                guardian_group = Group.objects.get(name='Guardian')
                guardian_group.user_set.add(new_user)

                guardianSerializer = WriteGuardianSerializer(
                    data={"user": new_user.pk, "phone_number": request.data["phone_number"]})
                if guardianSerializer.is_valid():
                    new_guardian = guardianSerializer.save()
                # Get device token and save it and connect it to the newly created Guardian object
                if ('device_fcm_token' in request.data):
                    Device.objects.create(
                        guardian=new_guardian, device_fcm_token=request.data['device_fcm_token'])
                    device = Device.objects.get(
                        device_fcm_token=request.data['device_fcm_token'])
                    device.guardian = Guardian.objects.get(user=new_user)
                    device.save()
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class GuardianStudentTransactionsView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]
    pagination_class = PageNumberPagination

    def get(self, request, registration_number):
        try:
            paginator = PageNumberPagination()
            bracelet = Guardian.objects.get(
                user=request.user).student.get(registration_number=registration_number).bracelet
            transactions = Transaction.objects.filter(
                wallet__bracelet=bracelet).order_by('-date')
            page = paginator.paginate_queryset(transactions, request)
        except Guardian.DoesNotExist:
            return Response({'error': 'Guardian not found'}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        if page is not None:
            serializer = TransactionGetSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)


class GuardianStudentOrdersView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]
    pagination_class = PageNumberPagination

    def post(self, request, registration_number):
        try:
            product_id = request.data['product_id']
            quantity = request.data['quantity']
            product = Product.objects.get(id=product_id)
            guardian = Guardian.objects.get(user=request.user)
            student = guardian.student.get(
                registration_number=registration_number)
            order_link_response = create_buy_request(
                guardian=guardian, student=student, product=product, quantity=quantity)
        except Guardian.DoesNotExist:
            return Response({'error': 'Guardian not found'}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(order_link_response, status=status.HTTP_200_OK)


class GuardianStudentTopupsView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]
    pagination_class = PageNumberPagination

    def get(self, request, registration_number):
        try:
            paginator = PageNumberPagination()
            bracelet = Guardian.objects.get(
                user=request.user).student.get(registration_number=registration_number).bracelet
            topups = TopUp.objects.filter(
                wallet__bracelet=bracelet).order_by('-created_at')
            page = paginator.paginate_queryset(topups, request)
        except Guardian.DoesNotExist:
            return Response({'error': 'Guardian not found'}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        if page is not None:
            serializer = TopupGetSerializer(
                page, many=True)
            return paginator.get_paginated_response(serializer.data)

    def post(self, request, registration_number):
        try:
            topup_amount = request.data['amount']
            guardian = Guardian.objects.get(user=request.user)
            student = guardian.student.get(
                registration_number=registration_number)
            bracelet = student.bracelet
            top_up_link_response = create_top_up_request(
                guardian=guardian, student=student, amount=topup_amount)

        except Guardian.DoesNotExist:
            return Response({'error': 'Guardian not found'}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(top_up_link_response, status=status.HTTP_200_OK)


class GuardianStudentAddView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]

    def post(self, request):
        try:
            guardian_obj = Guardian.objects.get(user=request.user)
            school = School.objects.get(
                name=request.data['school'], address=request.data['address'])
            student = Student.objects.get(
                registration_number=request.data['registration_number'], school_id=school.id)
            guardian_obj.student.add(student)
            guardian_obj.save()
        except Guardian.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        except School.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'status': 'success'}, status=status.HTTP_200_OK)
