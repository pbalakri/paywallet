from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from paywallet.permissions import IsGuardian, IsSchoolAdmin
from .models import Student, Attendance, School
from .serializers import AttendanceSerializer, AttendanceViewSerializer, SchoolSerializer


class CheckInView(APIView):
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def post(self, request, registration_number):
        try:
            student_obj = Student.objects.get(
                registration_number=registration_number)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        attendance_data = {'student_id': student_obj.id}
        attendance_serializer = AttendanceSerializer(data=attendance_data)

        if attendance_serializer.is_valid():
            attendance_serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, registration_number):
        try:
            student_obj = Student.objects.get(
                registration_number=registration_number)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            attendance_obj = Attendance.objects.filter(
                student_id=student_obj).latest('in_time')
        except Attendance.DoesNotExist:
            return Response({'error': 'Student not checked in'}, status=status.HTTP_400_BAD_REQUEST)

        attendance_obj.checkout = datetime.now()
        attendance_obj.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class SchoolView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]

    def get(self, request):
        try:
            school_obj = School.objects.all()
            serializer = SchoolSerializer(school_obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except School.DoesNotExist:
            return Response({'error': 'School not found'}, status=status.HTTP_404_NOT_FOUND)


class AttendanceView(APIView):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, IsGuardian]

    def get(self, request, registration_number):
        try:
            student_obj = Student.objects.get(
                registration_number=registration_number)
            paginator = PageNumberPagination()
            attendance_list = Attendance.objects.filter(
                student_id=student_obj).order_by('-in_time')
            page = paginator.paginate_queryset(attendance_list, request)
            serializer = AttendanceViewSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)


class AttendanceMonthView(APIView):
    permission_classes = [IsAuthenticated, IsGuardian]

    def get(self, request, registration_number, month):
        current_year = datetime.now().year
        previous_year = current_year - 1
        input_year = month+"-"+str(current_year)
        if datetime.strptime(input_year, '%B-%Y') > datetime.now():
            input_year = month+"-"+str(previous_year)

        try:
            start_date = datetime.strptime(
                input_year, '%B-%Y') - timedelta(days=1)
            end_date = datetime.strptime(
                input_year, '%B-%Y') + timedelta(days=31)
            student_obj = Student.objects.get(
                registration_number=registration_number)
            attendance_list = Attendance.objects.filter(
                student_id=student_obj, in_time__gte=start_date, in_time__lte=end_date).order_by('-in_time')
            serializer = AttendanceViewSerializer(attendance_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
