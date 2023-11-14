from django.db import models
from django.utils.translation import gettext_lazy as _


class DietaryRestriction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Dietary Restriction")
        verbose_name_plural = _("Dietary Restrictions")
