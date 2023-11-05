from django.apps import AppConfig


class SchoolStoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "school_store"
    # Display name for the application
    verbose_name = "School Store"
