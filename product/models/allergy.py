from django.db import models
from django.utils.translation import gettext_lazy as _

from paywallet.storage_backends import PublicMediaStorage


class Allergy(models.Model):
    # Add a name field with localized string
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    image = models.ImageField(storage=PublicMediaStorage(),
                              upload_to='allergies/',  blank=True, verbose_name=_("Image"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Allergy')
        verbose_name_plural = _('Allergies')
