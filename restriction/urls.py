from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"",
         views.RestrictionView.as_view(), name="restrictions"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
