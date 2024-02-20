from typing import Any
from django.db import models
from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext
from datetime import datetime
from .student import Student


from .school import School
from django.utils.translation import gettext_lazy as _


class Bracelet(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_("ID"))
    model_name = models.CharField(max_length=100, verbose_name=_("Model Name"))
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
