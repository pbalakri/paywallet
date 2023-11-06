from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SchoolStoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "school_store"
    # Display name for the application
    verbose_name = _("School Store")
