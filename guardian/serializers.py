from rest_framework import serializers
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

    class Meta:
        model = Guardian
        fields = ['user', 'phone_number']
