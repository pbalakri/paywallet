from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.db import transaction
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from paywallet.permissions import IsGuardian
from restriction.models import CategoryRestriction, PaymentRestriction, ProductsRestriction
from restriction.serializers import CategoryPurchaseRestrictionSerializer, PaymentRestrictionSerializer, ProductRestrictionSerializer
from school.models import Student, School
from wallet.models import Transaction
from wallet.serializers import TransactionGetSerializer
from .models import Device, Guardian
from .serializers import ReadGuardianSerializer, WriteGuardianSerializer, WriteUserSerializer


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

    def get(self, request, student_id):
        try:
            bracelet = Guardian.objects.get(
                user=request.user).student.get(id=student_id).bracelet
            transactions = Transaction.objects.filter(
                wallet__bracelet=bracelet).order_by('-date')
        except Guardian.DoesNotExist:
            return Response({'error': 'Guardian not found'}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TransactionGetSerializer(transactions, many=True)
        return Response({"transactions": serializer.data}, status=status.HTTP_200_OK)


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

# class GuardianUpdateView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             guardian_obj = Guardian.objects.get(user=request.user)
#         except Guardian.DoesNotExist:
#             return Response({'error': 'Guardian not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = GuardianSerializer(guardian_obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status': 'success'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
