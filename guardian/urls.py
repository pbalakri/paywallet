from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"register",
         views.GuardianRegisterView.as_view(), name="register"),
    path(r"", views.GuardianView.as_view(), name="guardian"),
    path(r"students",
         views.GuardianStudentAddView.as_view(), name="add_child"),
    path(r"students/<int:student_id>/transactions",
         views.GuardianStudentTransactionsView.as_view(), name="transactions"),
    path(r"students/<int:student_id>/restrictions",
         views.GuardianStudentRestrictionsView.as_view(), name="restrictions")
]
urlpatterns = format_suffix_patterns(urlpatterns)
