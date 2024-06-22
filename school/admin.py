from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.utils.translation import ngettext
from django.contrib import admin, messages
from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponseRedirect


# Register your models here.
from .models import Student, Attendance, School, SchoolAdmin, StudentAdmin, AttendanceAdmin, Bracelet, Teacher, TeacherAdmin, Operator, OperatorAdmin, SchoolAdministrator, SchoolAdministratorAdmin, Announcement, AnnouncementAdmin


class BraceletResource(resources.ModelResource):

    school_name = fields.Field(
        column_name='school_name',
        attribute='school',
        widget=ForeignKeyWidget(School, field='name'))

    class Meta:
        model = Bracelet
        fields = ('model_name', 'rfid', 'school_name')
        import_id_fields = ('rfid',)


class BraceletAdmin(ImportExportModelAdmin):
    resource_classes = [BraceletResource]
    list_display = ("rfid", "model_name", "school", "assigned_user", 'status')
    search_fields = ("rfid", "model_name", "school__name")
    autocomplete_fields = ['school']
    list_filter = ('status', 'school')

    def get_list_filter(self, request):
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return ('status', 'school')
        else:
            return ('status',)

    def get_readonly_fields(self, request, obj):
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return super().get_readonly_fields(request, obj)
        else:
            return ['status', 'assigned_user', 'model_name', 'rfid']

    def get_fields(self, request, obj):
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return (('model_name', 'rfid'),
                    ('school', 'status'))
        else:
            return (('model_name', 'rfid'),
                    ('status'))

    def assigned_user(self, obj):
        returnable_value = "Unassigned"
        # Get student who has this bracelet assigned
        try:
            # Get student who has this bracelet
            if obj.student is not None:
                returnable_value = f"{obj.student.first_name} {obj.student.last_name}"
        except:
            try:
                if obj.teacher is not None:
                    returnable_value = f"{obj.teacher.first_name} {obj.teacher.last_name}"
            except:
                returnable_value = "Unassigned"

        return returnable_value

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return super(BraceletAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "school":
            kwargs["queryset"] = School.objects.filter(
                school_admin=request.user)
            return super(BraceletAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(BraceletAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
            return qs
        else:
            return qs.filter(school__school_admin=request.user)


admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Bracelet, BraceletAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(SchoolAdministrator, SchoolAdministratorAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
