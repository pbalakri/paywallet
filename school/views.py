import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from paywallet.permissions import IsGuardian, IsSchoolAdmin
from .models import Student, Attendance, School
from .serializers import AttendanceSerializer, SchoolSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class CheckInView(APIView):
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def post(self, request, pk):
        try:
            student_obj = Student.objects.get(registration_number=pk)
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

    def post(self, request, pk):
        try:
            student_obj = Student.objects.get(registration_number=pk)
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
            # Get all Schools
            school_obj = School.objects.all()
            serializer = SchoolSerializer(school_obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except School.DoesNotExist:
            return Response({'error': 'School not found'}, status=status.HTTP_404_NOT_FOUND)
