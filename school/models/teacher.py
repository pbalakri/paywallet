from typing import Any
from django.db import models
from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext
from datetime import datetime
from paywallet.widgets.widget import PastCustomDatePickerWidget
from .bracelet import Bracelet


from .school import School
from django.utils.translation import gettext_lazy as _


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    registration_number = models.CharField(max_length=100, verbose_name=_(
        "Registration Number"))
    grade = models.IntegerField(default=0, verbose_name=_("Grade"))
    school = models.ForeignKey(
        School, on_delete=models.RESTRICT, verbose_name=_("School"))
    bracelet = models.ForeignKey(
        Bracelet, on_delete=models.RESTRICT, default=None)

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.registration_number + ")"

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
        unique_together = ('registration_number', 'school')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'first_name', 'last_name')
    fields = (('first_name', 'last_name'),
              ('registration_number', 'school'), 'bracelet')
    search_fields = ('first_name', 'last_name', 'registration_number')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(TeacherAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "school":
            kwargs["queryset"] = School.objects.filter(
                school_admin=request.user)
            return super(TeacherAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super(TeacherAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(TeacherAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(school_id__school_admin=request.user)

    def save_form(self, request: Any, form: Any, change: Any) -> Any:
        if request.user.is_superuser:
            return super().save_form(request, form, change)
        schools = School.objects.filter(school_admin=request.user)
        if len(schools) == 0:
            raise Exception("You are not an admin of any schools")
        else:
            form.instance.school_id = schools[0]
            return super().save_form(request, form, change)
