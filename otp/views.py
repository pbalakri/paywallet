from django.shortcuts import render
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from otp.models import OTP
from rest_framework import status
import datetime
import re
# Create your views here.


@authentication_classes([])
@permission_classes([])
class OTPGenerateView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        clean_phone_number = re.sub('[^0-9]', '', phone_number)
        otp_objs = OTP.objects.filter(
            phone_number=clean_phone_number, expires_at__gt=datetime.datetime.now())
        if otp_objs:
            return Response({'message': 'OTP already sent'}, status=status.HTTP_400_BAD_REQUEST)
        OTP.objects.create(phone_number=clean_phone_number)
        return Response({'message': 'OTP sent'}, status=status.HTTP_200_OK)


@authentication_classes([])
@permission_classes([])
class OTPValidateView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        clean_phone_number = re.sub('[^0-9]', '', phone_number)
        otp = request.data.get('otp')
        otp_obj = OTP.objects.filter(
            phone_number=clean_phone_number, otp=otp, validated=False, expires_at__gt=datetime.datetime.now()).first()
        if otp_obj:
            otp_obj.validated = True
            otp_obj.save()
            return Response({'message': 'OTP validated'}, status=status.HTTP_200_OK)
        return Response({'message': 'OTP validation failed'}, status=status.HTTP_400_BAD_REQUEST)
