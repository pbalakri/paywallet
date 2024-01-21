from typing import Any
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from cafe.models import Cafe


class Operator(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('Operator')
        verbose_name_plural = _('Operators')


class OperatorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone',
                    'email', 'password', 'cafe')
    fields = ('cafe', ('first_name', 'last_name'), 'phone',
              ('email', 'password'))
    search_fields = ('first_name', 'last_name', 'phone',
                     'email', 'password')

    def save_model(self, request, obj, form, change) -> None:
        # Create user object
        user = User.objects.create_user(
            username=obj.email,
            email=obj.email,
            password=obj.password,
            first_name=obj.first_name,
            last_name=obj.last_name,
        )
        user.is_staff = True
        operator_group = Group.objects.get(name='Vendor Operator')
        user.groups.add(operator_group)
        user.save()
        obj.user = user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(OperatorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "cafe":
            kwargs["queryset"] = Cafe.objects.filter(
                vendor_admin=request.user)
            return super(OperatorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super(OperatorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
