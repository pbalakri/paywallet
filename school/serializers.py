from rest_framework import serializers

from school.models import Student
from wallet.models import Wallet
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
    balance = serializers.SerializerMethodField('get_balance')
    school_name = serializers.CharField(source='school.name')

    def get_balance(self, obj):
        try:
            wallet = Wallet.objects.get(bracelet=obj.bracelet)
            return wallet.balance
        except Wallet.DoesNotExist:
            return 0

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'image',
                  'school_name', 'balance']
