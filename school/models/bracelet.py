import uuid
from django.db import models
from .student import Student
from django.contrib import admin

from .school import School
from django.utils.translation import gettext_lazy as _


class Bracelet(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, verbose_name=_("ID"))
    model_name = models.CharField(
        max_length=100, verbose_name=_("Bracelet Model"))
    rfid = models.CharField(max_length=100, unique=True,
                            verbose_name=_("RFID"))
    school = models.ForeignKey(
        School, on_delete=models.RESTRICT, verbose_name=_("School"))
    student = models.ForeignKey(
        Student, on_delete=models.RESTRICT, blank=True, null=True, verbose_name=_("Student"))

    def __str__(self):
        return self.rfid

    class Meta:
        verbose_name = _("Bracelet")
        verbose_name_plural = _("Bracelets")


class BraceletAdmin(admin.ModelAdmin):
    # If user is not super user all fields EXCEPT Student is readonly
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return [f.name for f in self.model._meta.fields if f.name != "student"]
    list_display = ('rfid', 'model_name', 'student')
    list_editable = ('student',)
