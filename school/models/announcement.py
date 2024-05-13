import uuid
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from paywallet.storage_backends import PublicMediaStorage


class Announcement(models.Model):
    def get_image_folder(instance, filename):
        return "announcements/school_{0}/{1}".format(instance.school.id, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(
        storage=PublicMediaStorage(), upload_to=get_image_folder, blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    school = models.ForeignKey(
        'school.School', on_delete=models.RESTRICT, verbose_name=_("School"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False, verbose_name=_("Published"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Announcement")
        verbose_name_plural = _("Announcements")


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'school',
                    'created_at', 'updated_at', 'published')
    list_filter = ('school', 'created_at', 'updated_at', 'published')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('image', 'title', 'description', 'school', 'published')
        }),
        (_('Dates'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school":
            if request.user.is_superuser or request.user.groups.filter(name='Payway Admin').exists():
                return db_field.formfield(**kwargs)
            else:
                kwargs["queryset"] = models.School.objects.filter(
                    school_admin=request.user)
                return db_field.formfield(**kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
