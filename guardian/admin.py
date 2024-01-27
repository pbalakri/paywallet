from django.contrib import admin
from .models import Guardian, GuardianAdmin
# Register your models here.

admin.site.register(Guardian, GuardianAdmin)
