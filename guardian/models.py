from typing import Any
import uuid
from django.db import models
from django.contrib.auth.models import User, Group
from school.models import Student
from django.contrib import admin


class Guardian(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, blank=True)
    device_fcm_token = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class GuardianAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone_number',
                     'student__first_name', 'student__last_name', 'student__registration_number')
