from rest_framework import serializers

from cafe.serializers import CafeSerializer
from wallet.models import Wallet
from .models import Attendance, School, Student, Announcement
import datetime
from django.db.models import Sum


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class AttendanceViewSerializer(serializers.ModelSerializer):
    checkin_date = serializers.SerializerMethodField('get_in_date')
    checkin_time = serializers.SerializerMethodField('get_in_time')
    checkout_date = serializers.SerializerMethodField('get_out_date')
    checkout_time = serializers.SerializerMethodField('get_out_time')

    def get_in_date(self, obj):
        return obj.in_time.date()

    def get_in_time(self, obj):
        return obj.in_time.strftime('%H:%M')

    def get_out_date(self, obj):
        return obj.out_time.date() if obj.out_time else None

    def get_out_time(self, obj):
        return obj.out_time.strftime('%H:%M') if obj.out_time else None

    class Meta:
        model = Attendance
        fields = ['checkin_date', 'checkin_time',
                  'checkout_time', 'checkout_date']


class SchoolSerializer(serializers.ModelSerializer):
    cafe_information = serializers.SerializerMethodField('get_cafe_name')

    def get_cafe_name(self, obj):
        return CafeSerializer(obj.cafe).data if hasattr(obj, 'cafe') else None

    class Meta:
        model = School
        fields = ['id', 'name', 'address', 'cafe_information']


class StudentSerializer(serializers.ModelSerializer):
    school_information = SchoolSerializer(source='school')
    wallet_information = serializers.SerializerMethodField('get_wallet')

    def get_wallet(self, obj):
        try:
            wallet = Wallet.objects.get(bracelet=obj.bracelet)
            balance = wallet.balance
            monthly_spend = wallet.transaction_set.filter(
                date__month=datetime.datetime.now().month).aggregate(Sum('amount'))
            weekly_spend = wallet.transaction_set.filter(
                date__week=datetime.datetime.now().isocalendar()[1]).aggregate(Sum('amount'))
            daily_spend = wallet.transaction_set.filter(
                date__day=datetime.datetime.now().day).aggregate(Sum('amount'))
            return {
                "active": wallet.active,
                "balance": balance,
                "spend": {
                    'monthly': monthly_spend['amount__sum'] if monthly_spend['amount__sum'] else 0,
                    'weekly': weekly_spend['amount__sum'] if weekly_spend['amount__sum'] else 0,
                    'daily': daily_spend['amount__sum'] if daily_spend['amount__sum'] else 0
                }
            }
        except Wallet.DoesNotExist:
            return {
                "active": False,
                "balance": 0,
                "spend": {
                    "monthly": 0,
                    "weekly": 0,
                    "daily": 0
                }
            }

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'image',
                  'school_information', 'wallet_information', 'registration_number']


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
