from django.contrib import admin

from .models import OTP, OTPAdmin

# Register your models here.
admin.site.register(OTP, OTPAdmin)
