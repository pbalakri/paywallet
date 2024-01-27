import uuid
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class School(models.Model):
    id = models.AutoField(primary_key=True)
    guid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    primary_email = models.CharField(max_length=100)
    school_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, limit_choices_to={
                                     'groups__name': 'School Admin'})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'guid', 'address', 'city', 'phone_number',
                    'school_admin')
    fields = ('name', ('address', 'city'), 'phone_number', 'school_admin')
    list_filter = ('city',)
    search_fields = ('name', 'phone_number')

    def get_queryset(self, request):
        qs = super(SchoolAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(school_admin=request.user)
