from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"<str:school_id>/students/<str:pk>/checkin",
         views.CheckInView.as_view(), name="checkin"),
    path(r"<str:school_id>/students/<str:pk>/checkout",
         views.CheckoutView.as_view(), name="checkout"),
    path(r"",
         views.SchoolView.as_view(), name="school"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
