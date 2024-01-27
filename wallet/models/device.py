from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from guardian.models import Guardian


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
