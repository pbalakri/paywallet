from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from school.models import Student


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    rfid = models.CharField(max_length=100, unique=True)
    student_id = models.ForeignKey(
        Student, on_delete=models.RESTRICT)
    balance = models.FloatField(default=0)
    restrictions = models.ManyToManyField(
        'product.DietaryRestriction', blank=True)

    def __str__(self):
        return self.rfid

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')


class WalletAdmin(admin.ModelAdmin):
    list_display = ('rfid', 'student_id', 'all_restrictions', )
    fields = ('rfid', 'student_id', 'restrictions')
    search_fields = ('rfid', 'student_id__first_name',
                     'student_id__last_name', 'student_id__registration_number')

    def all_restrictions(self, obj):
        return ", ".join([p.name for p in obj.restrictions.all()])

    def get_list_display(self, request):
        if request.user.is_superuser:
            return super().get_list_display(request) + ('balance',)
        else:
            return super().get_list_display(request)

    def get_fields(self, request, obj):
        if request.user.is_superuser:
            return super().get_fields(request, obj) + ('balance',)
        else:
            return super().get_fields(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(WalletAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        elif db_field.name == "student_id":
            kwargs["queryset"] = Student.objects.filter(
                school_id__school_admin=request.user)
            return super(WalletAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(WalletAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(student_id__school_id__school_admin=request.user)
