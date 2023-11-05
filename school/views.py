import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from school.models import Student, Attendance

# Create your views here.


# POST /api/v1/students/<int:student_id>/checkin
# POST /api/v1/students/<int:student_id>/checkout

@api_view(['GET'])
def check_in(request, pk, format=json):
    student_obj = Student.objects.get(registration_number=pk)
    Attendance.objects.create(student_id=student_obj)
    return Response({'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def check_out(request, pk, format=json):
    student_obj = Student.objects.get(registration_number=pk)
    latest_attendance = Attendance.objects.filter(
        student_id=student_obj).latest('in_time')
    if latest_attendance.out_time is None:
        latest_attendance.out_time = datetime.now()
        latest_attendance.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'error'}, status=status.HTTP_412_PRECONDITION_FAILED)
