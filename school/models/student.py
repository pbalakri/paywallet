from typing import Any
from django.db import models
from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext
from datetime import datetime


from .school import School
from django.utils.translation import gettext_lazy as _


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    grade = models.IntegerField(default=0)
    date_of_birth = models.DateField(default=None)
    school = models.ForeignKey(School, on_delete=models.RESTRICT)

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.registration_number + ")"

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")


class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'first_name', 'last_name',
                    'date_of_birth', 'current_status')
    fields = (('first_name', 'last_name'),
              ('date_of_birth', 'registration_number'), 'school')
    search_fields = ('first_name', 'last_name', 'registration_number')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(StudentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "school":
            kwargs["queryset"] = School.objects.filter(
                school_admin=request.user)
            return super(StudentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        else:
            return super(StudentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def current_status(self, obj):
        latest_attendance = Attendance.objects.filter(
            student_id=obj).latest('in_time')
        if latest_attendance.out_time is None:
            in_time = latest_attendance.in_time
            return mark_safe('<span style="color:green;">Checked In: ' + str(in_time.date()) + " " + str(in_time.strftime('%H:%M')) + '</span>')
        else:
            out_time = latest_attendance.out_time
            return mark_safe('<span style="color:red;">Checked Out: ' + str(out_time.date()) + " " + str(out_time.strftime('%H:%M')) + '</span>')

    @admin.action(description='Check Out Selected Students')
    def perform_check_out(self, request, queryset):
        # Validate that the latest attendance record student is checked in and update it
        updated_count = 0
        # Get total records to be updated
        total_count = queryset.count()
        for obj in queryset:
            #
            latest_attendance = Attendance.objects.filter(
                student_id=obj).latest('in_time')
            if latest_attendance.out_time is None:
                latest_attendance.out_time = datetime.now()
                latest_attendance.save()
                updated_count += 1
        self.message_user(
            request,
            ngettext(
                '%(updated_count)d/%(total_count)d student was successfully checked out.',
                '%(updated_count)d/%(total_count)d students were successfully checked out.',
                updated_count
            )
            % {"updated_count": updated_count, "total_count": total_count},
            messages.SUCCESS,
        )

    @admin.action(description='Check In Selected Students')
    def perform_check_in(self, request, queryset):
        created_count = 0
        total_count = queryset.count()
        for obj in queryset:
            Attendance.objects.create(student_id=obj)
            created_count += 1
        self.message_user(
            request,
            ngettext(
                '%(created_count)d/%(total_count)d student was successfully checked in.',
                '%(created_count)d/%(total_count)d students were successfully checked in.',
                created_count)
            % {"created_count": created_count, "total_count": total_count},
            messages.SUCCESS,
        )

    actions = [perform_check_out, perform_check_in]

    def get_queryset(self, request):
        qs = super(StudentAdmin, self).get_queryset(request)
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


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.RESTRICT)
    in_time = models.DateTimeField(auto_now_add=True)
    out_time = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return self.student_id.first_name + " " + self.student_id.last_name + " (" + self.student_id.registration_number + ")"

    class Meta:
        verbose_name_plural = _("Attendance")
        verbose_name = _("Attendance")


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'in_time', 'out_time')
    list_filter = ('in_time', 'out_time')
    search_fields = ('student_id__first_name', 'student_id__last_name',
                     'student_id__registration_number')

    def get_queryset(self, request):
        qs = super(AttendanceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(student_id__school_id__school_admin=request.user)
