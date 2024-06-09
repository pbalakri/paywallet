from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"generate",
         views.OTPGenerateView.as_view(), name="generate-otp"),
    path(r"validate",
         views.OTPValidateView.as_view(), name="validate-otp"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
