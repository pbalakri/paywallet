from django.db import models
from django.contrib import admin

# Create your models here.


class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    # Expires in 5 minutes
    expires_at = models.DateTimeField(blank=True, null=True)
    validated = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number


class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'otp', 'validated')
    search_fields = ('phone_number',)
