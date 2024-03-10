from typing import Any
import uuid
from django.db import models
from django.contrib.auth.models import User, Group
from paywallet.storage_backends import PublicMediaStorage
from school.models import Student
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class Guardian(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, blank=True)
    image = models.ImageField(
        storage=PublicMediaStorage, upload_to='guardian/', blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class GuardianAdmin(admin.ModelAdmin):
    list_display = ('image', 'user', 'phone_number')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone_number',
                     'student__first_name', 'student__last_name', 'student__registration_number')


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    guardian = models.ForeignKey(
        Guardian, related_name='guardian_user', on_delete=models.RESTRICT)
    device_fcm_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device_fcm_token

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('guardian', 'device_fcm_token', 'created_at')
    search_fields = ('guardian__username', 'device_fcm_token')
