import uuid
from django.db import models
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
    ACTIVE = 'assigned'
    INACTIVE = 'inactive'
    UNASSIGNED = 'unassigned'
    STATUS_CHOICES = [
        (ACTIVE, _('Assigned')),
        (INACTIVE, _('Inactive')),
        (UNASSIGNED, _('Unassigned')),
    ]
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=UNASSIGNED, verbose_name=_("Status"))

    def __str__(self):
        return self.rfid

    class Meta:
        verbose_name = _("Bracelet")
        verbose_name_plural = _("Bracelets")
        unique_together = ("rfid", "school")
