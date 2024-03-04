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
    list_display = ("rfid", "model_name", "school", "assigned_user", 'status')
    fields = (('model_name', 'rfid'),
              ('school', 'status'))
    search_fields = ("rfid", "model_name", "school__name")
    autocomplete_fields = ['school']
    readonly_fields = ['status', 'assigned_user']

    def assigned_user(self, obj):
        returnable_value = "Unassigned"
        try:
            # Get student who has this bracelet
            if obj.student is not None:
                returnable_value = f"{obj.student.first_name} {obj.student.last_name}"
            elif obj.teacher is not None:
                returnable_value = f"{obj.teacher.first_name} {obj.teacher.last_name}"
        except:
            returnable_value = "Unassigned"
        return returnable_value

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
            return qs.filter(school__school_admin=request.user)

    def save_form(self, request, form, change):
        def remove_bracelet_from_user(bracelet):
            try:
                student = Student.objects.get(bracelet=bracelet)
                student.bracelet = None
                student.save()
            except Student.DoesNotExist:
                pass
            try:
                teacher = Teacher.objects.get(bracelet=bracelet)
                teacher.bracelet = None
                teacher.save()
            except Teacher.DoesNotExist:
                pass
        if request.user.is_superuser:
            if form.instance.status == Bracelet.UNASSIGNED:
                remove_bracelet_from_user(form.instance)
            return super().save_form(request, form, change)
        school = School.objects.get(school_admin=request.user)
        if school is None:
            raise Exception("You are not an admin of any school")
        else:
            form.instance.school = school
            # If bracelet is being unassigned, then set the bracelet field of Student and Teacher to None
            if form.instance.status == Bracelet.UNASSIGNED:
                remove_bracelet_from_user(form.instance)
            return super().save_form(request, form, change)


admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Bracelet, BraceletAdmin)
admin.site.register(Teacher, TeacherAdmin)
