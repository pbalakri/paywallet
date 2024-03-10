from typing import Any
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django import forms
from . import School


class SchoolAdministrator(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = _('School Administrator')
        verbose_name_plural = _('School Administrators')


class SchoolAdministratorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['first_name'].initial = instance.user.first_name
            self.fields['last_name'].initial = instance.user.last_name
            self.fields['email'].initial = instance.user.email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('password', "Passwords don't match")
            self.add_error('confirm_password', "Passwords don't match")

        return cleaned_data

    class Meta:
        model = SchoolAdministrator
        fields = ('phone', 'school')


class SchoolAdministratorAdmin(admin.ModelAdmin):
    form = SchoolAdministratorForm
    list_display = ('name', 'phone', 'school')
    fields = ('school', ('first_name', 'last_name'),
              ('phone', 'email'), ('password', 'confirm_password'))

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
            school_admin_group = Group.objects.get(name='School Admin')
            user.groups.add(school_admin_group)
            user.save()
            obj.school = form.cleaned_data.get('school')
            obj.user = user
            obj.save()
