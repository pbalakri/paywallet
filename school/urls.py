from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"<str:school_id>/students/<str:registration_number>/checkin",
         views.CheckInView.as_view(), name="checkin"),
    path(r"<str:school_id>/students/<str:registration_number>/checkout",
         views.CheckoutView.as_view(), name="checkout"),
    path(r"students/<str:registration_number>/attendance",
         views.AttendanceView.as_view(), name="attendance"),
    path(r"",
         views.SchoolView.as_view(), name="school"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
