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
    fields = (('model_name', 'rfid', 'status'),
              ('school'))
    search_fields = ("rfid", "model_name", "school__name")
    autocomplete_fields = ['school']

    def assigned_user(self, obj):
        # Get student record filter by bracelet object
        student = obj.student_set.first()
        teacher = obj.teacher_set.first()
        if student:
            return f"{student.first_name} {student.last_name}"
        elif teacher:
            return f"{teacher.first_name} {teacher.last_name}"
        else:
            return "Unassigned"

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
        def remove_bracelet_from_user(form):
            student = form.instance.student_set.first()
            teacher = form.instance.teacher_set.first()
            if student:
                student.bracelet = None
                student.save()
            if teacher:
                teacher.bracelet = None
                teacher.save()
        if request.user.is_superuser:
            if form.instance.status == Bracelet.UNASSIGNED:
                remove_bracelet_from_user(form)
            return super().save_form(request, form, change)
        schools = School.objects.filter(school_admin=request.user)
        if not schools.exists():
            raise Exception("You are not an admin of any school")
        else:
            form.instance.school_id = schools.first()
            # If bracelet is being unassigned, then set the bracelet field of Student and Teacher to None
            if form.instance.status == Bracelet.UNASSIGNED:
                remove_bracelet_from_user(form)
            return super().save_form(request, form, change)


admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Bracelet, BraceletAdmin)
admin.site.register(Teacher, TeacherAdmin)
