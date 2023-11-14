from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r"students/<str:pk>/checkin",
         views.CheckInView.as_view(), name="checkin"),
    path(r"students/<str:pk>/checkout",
         views.CheckoutView.as_view(), name="checkout"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
