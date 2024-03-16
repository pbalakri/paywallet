from rest_framework import serializers

from school.models import Student
from .models import Attendance, School


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'address']


class StudentSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name',
                  'registration_number', 'school', 'date_of_birth']
