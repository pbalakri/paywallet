from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"register",
         views.GuardianRegisterView.as_view(), name="register"),
    path(r"reset-password",
         views.GuardianResetPasswordView.as_view(), name="reset"),
    path(r"", views.GuardianView.as_view(), name="guardian"),
    path(r"students",
         views.GuardianStudentAddView.as_view(), name="add_child"),
    path(r"students/<str:registration_number>/transactions",
         views.GuardianStudentTransactionsView.as_view(), name="transactions"),
    path(r"students/<str:registration_number>/bracelet/activate",
         views.GuardianBraceletActivateView.as_view(), name="activate_bracelet"),
    path(r"students/<str:registration_number>/bracelet/deactivate",
         views.GuardianBraceletDeActivateView.as_view(), name="deactivate_bracelet"),
    path(r"students/<str:registration_number>/topups",
         views.GuardianStudentTopupsView.as_view(), name="topups"),
    path(r"students/<str:registration_number>/orders",
         views.GuardianStudentOrdersView.as_view(), name="studentorders"),
    path(r"orders", views.GuardianOrdersView.as_view(), name="allorders"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
