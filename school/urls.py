from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


# router = routers.DefaultRouter()
# # router.register(r"students", views.StudentViewSet)
# router.register(r"students/<int:pk>/checkin",
# views.check_in)
# router.register(r"students/<int:pk>/checkout",
urlpatterns = [
    path(r"students/<int:pk>/checkin", views.check_in),
    path(r"students/<int:pk>/checkout", views.check_out)
]
urlpatterns = format_suffix_patterns(urlpatterns)
