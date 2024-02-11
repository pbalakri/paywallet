from django.contrib import admin
from .models import Guardian, GuardianAdmin, Device, DeviceAdmin
# Register your models here.

admin.site.register(Guardian, GuardianAdmin)
admin.site.register(Device, DeviceAdmin)
