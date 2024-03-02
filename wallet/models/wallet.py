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
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.bracelet.rfid

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')


class WalletAdmin(admin.ModelAdmin):
    list_display = ('bracelet', 'assigned_user', 'status')
    fields = ('bracelet', 'balance')
    # readonly_fields = ('bracelet', 'status', 'assigned_user', 'balance')
    search_fields = ('bracelet',)

    def assigned_user(self, obj):
        # Get student record filter by bracelet object
        student = obj.bracelet.student_set.first()
        teacher = obj.bracelet.teacher_set.first()
        if student:
            return f'{student.first_name} {student.last_name}'
        elif teacher:
            return f'{teacher.first_name} {teacher.last_name}'
        else:
            return 'Unassigned'

    def get_list_display(self, request):
        if request.user.is_superuser:
            return super().get_list_display(request) + ('balance',)
        else:
            return super().get_list_display(request)
