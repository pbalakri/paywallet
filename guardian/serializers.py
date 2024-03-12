from rest_framework import serializers
from school.models import Student

from school.serializers import StudentSerializer
from .models import Guardian
from django.contrib.auth.models import User


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class WriteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'username']


class WriteGuardianSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guardian
        fields = ['user', 'phone_number']


class ReadGuardianSerializer(serializers.ModelSerializer):
    user = ReadUserSerializer(read_only=True)
    student = StudentSerializer(read_only=True, many=True)

    class Meta:
        model = Guardian
        fields = ['user', 'phone_number', 'student']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['registration_number', 'school_id', 'image']
