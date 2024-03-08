import uuid
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from school.models import Bracelet


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bracelet = models.OneToOneField(
        Bracelet, on_delete=models.RESTRICT, default=None, related_name='wallet')
    balance = models.FloatField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.bracelet.rfid

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')


class WalletAdmin(admin.ModelAdmin):
    list_display = ('bracelet', 'assigned_user', 'active')
    fields = ('bracelet', 'balance')
    # readonly_fields = ('bracelet', 'status', 'assigned_user', 'balance')
    search_fields = ('bracelet',)

    def assigned_user(self, obj):
        returnable_value = "Unassigned"
        # Get student record filter by bracelet object
        try:
            student = obj.bracelet.student_set.first()
            teacher = obj.bracelet.teacher_set.first()
            if student:
                returnable_value = f'{student.first_name} {student.last_name}'
            elif teacher:
                returnable_value = f'{teacher.first_name} {teacher.last_name}'
        except:
            returnable_value = "Unassigned"

        return returnable_value

    def get_list_display(self, request):
        if request.user.is_superuser:
            return super().get_list_display(request) + ('balance',)
        else:
            return super().get_list_display(request)
