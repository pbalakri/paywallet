from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"guardian/register",
         views.GuardianRegisterView.as_view(), name="register"),
    path(r"guardian", views.GuardianView.as_view(), name="guardian"),
    path(r"guardian/add/student",
         views.GuardianUpdateView.as_view(), name="add_child"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
