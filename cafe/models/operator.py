from typing import Any
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django import forms
from cafe.models import Cafe


class Operator(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=20)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = _('Operator')
        verbose_name_plural = _('Operators')


class OperatorAdminForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['first_name'].initial = instance.user.first_name
            self.fields['last_name'].initial = instance.user.last_name
            self.fields['email'].initial = instance.user.email

    class Meta:
        model = Operator
        fields = ('phone', 'cafe')


class OperatorAdmin(admin.ModelAdmin):
    form = OperatorAdminForm
    list_display = ('name', 'phone', 'cafe')
    # fields = ('cafe', 'first_name', 'last_name', 'phone', 'email', 'password')
    fields = ('cafe', ('first_name', 'last_name'), 'phone',
              ('email', 'password'))

    def get_fields(self, request, obj):
        if request.user.is_superuser:
            return ('cafe', ('first_name', 'last_name'), 'phone', ('email', 'password'))
        elif request.user.groups.filter(name='Vendor Admin').exists():
            return (('first_name', 'last_name'), 'phone', ('email', 'password'))

    def name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        if (change):
            user = obj.user
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()
            obj.save()
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.is_staff = True
            operator_group = Group.objects.get(name='Vendor Operator')
            user.groups.add(operator_group)
            user.save()
            cafe = Cafe.objects.get(
                admin=request.user)
            obj.cafe = cafe
            obj.user = user
            obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(OperatorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "cafe":
            kwargs["queryset"] = Cafe.objects.filter(
                admin=request.user)
            return super(OperatorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super(OperatorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):

        qs = super(OperatorAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        elif request.user.groups.filter(name='Vendor Admin').exists():
            # Return operators of the cafe of the vendor admin
            return qs.filter(cafe__admin=request.user)
        else:
            return qs.none()
