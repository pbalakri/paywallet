import uuid
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class Cafe(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='vendor_admin', on_delete=models.RESTRICT, limit_choices_to={
        'groups__name': 'Vendor Admin'})
    operators = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='vendor_users', limit_choices_to={'groups__name__in': ['Vendor Admin', 'Vendor Operator']})

    class Meta:
        verbose_name = _("Café")
        verbose_name_plural = _("Café")
        unique_together = ('name', 'address')

    def __str__(self):
        return self.name


class CafeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'admin')
    search_fields = ('name', 'address')
    autocomplete_fields = ['admin']

    def get_queryset(self, request):
        qs = super(CafeAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return qs
        else:
            return qs.filter(admin=request.user)
