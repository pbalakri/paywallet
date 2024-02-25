from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.
from .models import Student, Attendance, School, SchoolAdmin, StudentAdmin, AttendanceAdmin, Bracelet, Teacher, TeacherAdmin


class BraceletResource(resources.ModelResource):
    class Meta:
        model = Bracelet
        fields = ('model_name', 'rfid', 'school')


class BraceletAdmin(ImportExportModelAdmin):
    resource_classes = [BraceletResource]
    list_display = ('rfid', 'school')
    fields = (('model_name', 'rfid'),
              ('school'))
    search_fields = ('rfid',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(BraceletAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "school":
            kwargs["queryset"] = School.objects.filter(
                school_admin=request.user)
            return super(BraceletAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(BraceletAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(school_id__school_admin=request.user)

    def save_form(self, request, form, change):
        if request.user.is_superuser:
            return super().save_form(request, form, change)
        schools = School.objects.filter(school_admin=request.user)
        if len(schools) == 0:
            raise Exception("You are not an admin of any schools")
        else:
            form.instance.school_id = schools[0]
            return super().save_form(request, form, change)


admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Bracelet, BraceletAdmin)
admin.site.register(Teacher, TeacherAdmin)
