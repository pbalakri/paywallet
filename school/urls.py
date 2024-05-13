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
    path(r"students/<str:registration_number>/attendance/month/<str:month>",
         views.AttendanceMonthView.as_view(), name="attendance"),
    path(r"students/<str:registration_number>/balance",
         views.StudentBalanceView.as_view(), name="student_balance"),
    path(r"",
         views.SchoolView.as_view(), name="school"),
    path(r"<str:school_id>/announcements",
         views.AllAnnouncementsView.as_view(), name="school"),
    path(r"<str:school_id>/announcements/<str:announcement_id>",
         views.AnnouncementView.as_view(), name="school"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
