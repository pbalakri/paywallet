import uuid
from django.db import models
from django.contrib import admin

from .school import School
from django.utils.translation import gettext_lazy as _


class Bracelet(models.Model):
    rfid = models.CharField(primary_key=True, max_length=100, unique=True,
                            verbose_name=_("RFID"))
    model_name = models.CharField(
        max_length=100, verbose_name=_("Bracelet Model"))
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, verbose_name=_("School"))
    ACTIVE = 'assigned'
    UNASSIGNED = 'unassigned'
    DEACTIVATED = 'deactivated'
    STATUS_CHOICES = [
        (ACTIVE, _('Assigned')),
        (UNASSIGNED, _('Unassigned')),
        (DEACTIVATED, _('Deactivated')),
    ]
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=UNASSIGNED, verbose_name=_("Status"))

    def __str__(self):
        return self.rfid

    class Meta:
        verbose_name = _("Bracelet")
        verbose_name_plural = _("Bracelets")
        unique_together = ("rfid", "school")
        permissions = [('import_bracelet', 'Can import Bracelets'),
                       ('export_bracelet', 'Can export Bracelets')]
